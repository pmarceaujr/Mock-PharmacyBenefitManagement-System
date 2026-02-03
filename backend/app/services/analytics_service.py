from app import db
from app.models import Claim, Drug, Member
from sqlalchemy import func, text
from datetime import datetime, timedelta


class AnalyticsService:
    """Service for complex analytics queries"""
    
    @staticmethod
    def get_cost_trends_with_window_functions(days=90):
        """
        Use PostgreSQL window functions to calculate running totals and ranks
        """
        start_date = datetime.utcnow().date() - timedelta(days=days)
        
        # Raw SQL with window functions
        query = text("""
            SELECT 
                fill_date,
                COUNT(*) as daily_claims,
                SUM(total_cost) as daily_cost,
                SUM(SUM(total_cost)) OVER (
                    ORDER BY fill_date 
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                ) as running_total,
                AVG(SUM(total_cost)) OVER (
                    ORDER BY fill_date 
                    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
                ) as moving_avg_7day,
                RANK() OVER (ORDER BY SUM(total_cost) DESC) as cost_rank
            FROM claims
            WHERE fill_date >= :start_date
            GROUP BY fill_date
            ORDER BY fill_date
        """)
        
        result = db.session.execute(query, {'start_date': start_date})
        
        return [
            {
                'date': row.fill_date.isoformat(),
                'daily_claims': row.daily_claims,
                'daily_cost': float(row.daily_cost),
                'running_total': float(row.running_total),
                'moving_avg_7day': float(row.moving_avg_7day),
                'cost_rank': row.cost_rank
            }
            for row in result
        ]
    
    @staticmethod
    def find_duplicate_claims():
        """
        Find potential duplicate claims using CTE pattern
        """
        query = text("""
            WITH claim_groups AS (
                SELECT 
                    member_id,
                    drug_id,
                    fill_date,
                    COUNT(*) as claim_count,
                    ARRAY_AGG(claim_number) as claim_numbers,
                    SUM(total_cost) as total_cost
                FROM claims
                WHERE fill_date >= CURRENT_DATE - INTERVAL '90 days'
                GROUP BY member_id, drug_id, fill_date
                HAVING COUNT(*) > 1
            )
            SELECT 
                cg.member_id,
                m.first_name || ' ' || m.last_name as member_name,
                d.name as drug_name,
                cg.fill_date,
                cg.claim_count,
                cg.claim_numbers,
                cg.total_cost
            FROM claim_groups cg
            JOIN members m ON cg.member_id = m.id
            JOIN drugs d ON cg.drug_id = d.id
            ORDER BY cg.total_cost DESC
        """)
        
        result = db.session.execute(query)
        
        return [
            {
                'member_id': row.member_id,
                'member_name': row.member_name,
                'drug_name': row.drug_name,
                'fill_date': row.fill_date.isoformat(),
                'duplicate_count': row.claim_count,
                'claim_numbers': row.claim_numbers,
                'total_cost': float(row.total_cost)
            }
            for row in result
        ]
    
    @staticmethod
    def calculate_member_risk_score():
        """
        Calculate risk scores for members based on utilization patterns
        """
        query = text("""
            WITH member_stats AS (
                SELECT 
                    member_id,
                    COUNT(*) as claim_count,
                    SUM(total_cost) as total_cost,
                    COUNT(DISTINCT drug_id) as unique_drugs,
                    AVG(days_supply) as avg_days_supply
                FROM claims
                WHERE fill_date >= CURRENT_DATE - INTERVAL '180 days'
                GROUP BY member_id
            ),
            percentiles AS (
                SELECT 
                    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY claim_count) as p75_claims,
                    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY total_cost) as p75_cost,
                    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY unique_drugs) as p75_drugs
                FROM member_stats
            )
            SELECT 
                ms.member_id,
                m.first_name || ' ' || m.last_name as member_name,
                ms.claim_count,
                ms.total_cost,
                ms.unique_drugs,
                ms.avg_days_supply,
                CASE 
                    WHEN ms.claim_count > p.p75_claims THEN 2
                    WHEN ms.claim_count > (p.p75_claims * 0.5) THEN 1
                    ELSE 0
                END +
                CASE 
                    WHEN ms.total_cost > p.p75_cost THEN 2
                    WHEN ms.total_cost > (p.p75_cost * 0.5) THEN 1
                    ELSE 0
                END +
                CASE 
                    WHEN ms.unique_drugs > p.p75_drugs THEN 2
                    WHEN ms.unique_drugs > (p.p75_drugs * 0.5) THEN 1
                    ELSE 0
                END as risk_score
            FROM member_stats ms
            JOIN members m ON ms.member_id = m.id
            CROSS JOIN percentiles p
            WHERE m.is_active = true
            ORDER BY risk_score DESC, ms.total_cost DESC
            LIMIT 50
        """)
        
        result = db.session.execute(query)
        
        return [
            {
                'member_id': row.member_id,
                'member_name': row.member_name,
                'claim_count': row.claim_count,
                'total_cost': float(row.total_cost),
                'unique_drugs': row.unique_drugs,
                'avg_days_supply': float(row.avg_days_supply),
                'risk_score': row.risk_score,
                'risk_level': 'High' if row.risk_score >= 4 else 'Medium' if row.risk_score >= 2 else 'Low'
            }
            for row in result
        ]

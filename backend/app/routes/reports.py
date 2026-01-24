from flask import Blueprint, request, jsonify
from app import db
from app.models import Claim, Drug, Member
from sqlalchemy import func, and_, case
from datetime import datetime, timedelta

bp = Blueprint('reports', __name__, url_prefix='/api/reports')


@bp.route('/generic-savings', methods=['GET'])
def generic_savings_opportunity():
    """Calculate potential savings from generic substitution"""
    days = request.args.get('days', 90, type=int)
    start_date = datetime.utcnow().date() - timedelta(days=days)
    
    # Find brand claims where generic alternative exists
    brand_claims = db.session.query(
        Drug.name.label('brand_name'),
        Drug.generic_name,
        func.count(Claim.id).label('brand_claims'),
        func.sum(Claim.total_cost).label('brand_cost'),
        func.avg(Claim.total_cost).label('avg_brand_cost')
    ).join(Drug).filter(
        Claim.fill_date >= start_date,
        Drug.is_generic == False,
        Drug.generic_name.isnot(None)
    ).group_by(Drug.name, Drug.generic_name).all()
    
    savings_opportunities = []
    
    for brand in brand_claims:
        # Find average cost of generic equivalent
        generic_avg = db.session.query(
            func.avg(Claim.total_cost)
        ).join(Drug).filter(
            Drug.generic_name == brand.generic_name,
            Drug.is_generic == True,
            Claim.fill_date >= start_date
        ).scalar()
        
        if generic_avg:
            potential_savings = (float(brand.avg_brand_cost) - float(generic_avg)) * brand.brand_claims
            
            if potential_savings > 0:
                savings_opportunities.append({
                    'brand_name': brand.brand_name,
                    'generic_name': brand.generic_name,
                    'brand_claims': brand.brand_claims,
                    'avg_brand_cost': float(brand.avg_brand_cost),
                    'avg_generic_cost': float(generic_avg),
                    'potential_savings': round(potential_savings, 2),
                    'savings_per_claim': round(float(brand.avg_brand_cost) - float(generic_avg), 2)
                })
    
    # Sort by potential savings
    savings_opportunities.sort(key=lambda x: x['potential_savings'], reverse=True)
    
    total_potential_savings = sum(opp['potential_savings'] for opp in savings_opportunities)
    
    return jsonify({
        'period_days': days,
        'total_potential_savings': round(total_potential_savings, 2),
        'opportunities': savings_opportunities[:20]  # Top 20
    }), 200


@bp.route('/cost-summary', methods=['GET'])
def cost_summary_report():
    """Comprehensive cost summary report"""
    start_date_str = request.args.get('start_date', '')
    end_date_str = request.args.get('end_date', '')
    
    if not start_date_str or not end_date_str:
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=90)
    else:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    
    # Overall statistics
    overall = db.session.query(
        func.count(Claim.id).label('total_claims'),
        func.sum(Claim.total_cost).label('total_cost'),
        func.sum(Claim.plan_paid_amount).label('plan_paid'),
        func.sum(Claim.member_copay).label('member_paid'),
        func.avg(Claim.total_cost).label('avg_cost')
    ).filter(
        and_(Claim.fill_date >= start_date, Claim.fill_date <= end_date)
    ).first()
    
    # By status
    by_status = db.session.query(
        Claim.status,
        func.count(Claim.id).label('count'),
        func.sum(Claim.total_cost).label('cost')
    ).filter(
        and_(Claim.fill_date >= start_date, Claim.fill_date <= end_date)
    ).group_by(Claim.status).all()
    
    # Monthly breakdown
    monthly = db.session.query(
        extract('year', Claim.fill_date).label('year'),
        extract('month', Claim.fill_date).label('month'),
        func.count(Claim.id).label('claims'),
        func.sum(Claim.total_cost).label('cost')
    ).filter(
        and_(Claim.fill_date >= start_date, Claim.fill_date <= end_date)
    ).group_by('year', 'month').order_by('year', 'month').all()
    
    return jsonify({
        'report_period': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        },
        'overall_summary': {
            'total_claims': overall.total_claims or 0,
            'total_cost': float(overall.total_cost) if overall.total_cost else 0,
            'plan_paid': float(overall.plan_paid) if overall.plan_paid else 0,
            'member_paid': float(overall.member_paid) if overall.member_paid else 0,
            'average_cost': float(overall.avg_cost) if overall.avg_cost else 0
        },
        'by_status': [
            {
                'status': row.status,
                'claims': row.count,
                'cost': float(row.cost) if row.cost else 0
            } for row in by_status
        ],
        'monthly_breakdown': [
            {
                'year': int(row.year),
                'month': int(row.month),
                'claims': row.claims,
                'cost': float(row.cost)
            } for row in monthly
        ]
    }), 200


@bp.route('/member-summary/<int:member_id>', methods=['GET'])
def member_summary_report(member_id):
    """Detailed report for a specific member"""
    member = Member.query.get_or_404(member_id)
    days = request.args.get('days', 365, type=int)
    start_date = datetime.utcnow().date() - timedelta(days=days)
    
    # Member's claims
    claims_stats = db.session.query(
        func.count(Claim.id).label('total_claims'),
        func.sum(Claim.total_cost).label('total_cost'),
        func.sum(Claim.member_copay).label('total_copay'),
        func.avg(Claim.total_cost).label('avg_cost')
    ).filter(
        Claim.member_id == member_id,
        Claim.fill_date >= start_date
    ).first()
    
    # Most used drugs
    top_drugs = db.session.query(
        Drug.name,
        Drug.is_generic,
        func.count(Claim.id).label('fills'),
        func.sum(Claim.total_cost).label('total_cost')
    ).join(Drug).filter(
        Claim.member_id == member_id,
        Claim.fill_date >= start_date
    ).group_by(Drug.id, Drug.name, Drug.is_generic).order_by(
        func.count(Claim.id).desc()
    ).limit(10).all()
    
    # Recent claims
    recent_claims = Claim.query.filter(
        Claim.member_id == member_id,
        Claim.fill_date >= start_date
    ).order_by(Claim.fill_date.desc()).limit(10).all()
    
    return jsonify({
        'member': member.to_dict(),
        'period_days': days,
        'summary': {
            'total_claims': claims_stats.total_claims or 0,
            'total_cost': float(claims_stats.total_cost) if claims_stats.total_cost else 0,
            'total_copay': float(claims_stats.total_copay) if claims_stats.total_copay else 0,
            'avg_cost_per_claim': float(claims_stats.avg_cost) if claims_stats.avg_cost else 0
        },
        'most_used_drugs': [
            {
                'name': row.name,
                'is_generic': row.is_generic,
                'fills': row.fills,
                'total_cost': float(row.total_cost)
            } for row in top_drugs
        ],
        'recent_claims': [claim.to_dict() for claim in recent_claims]
    }), 200

from flask import Blueprint, request, jsonify
from app import db
from app.models import Claim, Drug, Member, Pharmacy
from sqlalchemy import func, extract, case, and_
from datetime import datetime, timedelta

bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')


@bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Get dashboard overview statistics"""
    days = request.args.get('days', 30, type=int)
    start_date = datetime.utcnow().date() - timedelta(days=days)
    
    # Total claims and cost
    total_stats = db.session.query(
        func.count(Claim.id).label('total_claims'),
        func.sum(Claim.total_cost).label('total_cost'),
        func.avg(Claim.total_cost).label('avg_cost')
    ).filter(Claim.fill_date >= start_date).first()
    
    # Generic vs Brand utilization
    generic_stats = db.session.query(
        Drug.is_generic,
        func.count(Claim.id).label('claim_count'),
        func.sum(Claim.total_cost).label('total_cost')
    ).join(Drug).filter(Claim.fill_date >= start_date).group_by(Drug.is_generic).all()
    
    # Top drugs by cost
    top_drugs = db.session.query(
        Drug.name,
        Drug.is_generic,
        func.count(Claim.id).label('claim_count'),
        func.sum(Claim.total_cost).label('total_cost')
    ).join(Drug).filter(
        Claim.fill_date >= start_date
    ).group_by(Drug.id, Drug.name, Drug.is_generic).order_by(
        func.sum(Claim.total_cost).desc()
    ).limit(10).all()
    
    # Claims by status
    status_breakdown = db.session.query(
        Claim.status,
        func.count(Claim.id).label('count')
    ).filter(Claim.fill_date >= start_date).group_by(Claim.status).all()
    
    return jsonify({
        'period_days': days,
        'start_date': start_date.isoformat(),
        'summary': {
            'total_claims': total_stats.total_claims or 0,
            'total_cost': float(total_stats.total_cost) if total_stats.total_cost else 0,
            'average_cost': float(total_stats.avg_cost) if total_stats.avg_cost else 0
        },
        'generic_vs_brand': [
            {
                'type': 'Generic' if row.is_generic else 'Brand',
                'claims': row.claim_count,
                'cost': float(row.total_cost)
            } for row in generic_stats
        ],
        'top_drugs': [
            {
                'name': row.name,
                'is_generic': row.is_generic,
                'claims': row.claim_count,
                'total_cost': float(row.total_cost)
            } for row in top_drugs
        ],
        'status_breakdown': [
            {'status': row.status, 'count': row.count} 
            for row in status_breakdown
        ]
    }), 200


@bp.route('/trends', methods=['GET'])
def get_trends():
    """Get cost trends over time using window functions"""
    days = request.args.get('days', 90, type=int)
    start_date = datetime.utcnow().date() - timedelta(days=days)
    
    # Daily aggregation with running total
    daily_stats = db.session.query(
        Claim.fill_date,
        func.count(Claim.id).label('daily_claims'),
        func.sum(Claim.total_cost).label('daily_cost')
    ).filter(
        Claim.fill_date >= start_date
    ).group_by(Claim.fill_date).order_by(Claim.fill_date).all()
    
    # Calculate 7-day moving average
    trends = []
    for i, row in enumerate(daily_stats):
        window_start = max(0, i - 6)
        window_data = daily_stats[window_start:i+1]
        
        avg_claims = sum(r.daily_claims for r in window_data) / len(window_data)
        avg_cost = sum(float(r.daily_cost or 0) for r in window_data) / len(window_data)
        
        trends.append({
            'date': row.fill_date.isoformat(),
            'claims': row.daily_claims,
            'cost': float(row.daily_cost or 0),
            'moving_avg_claims': round(avg_claims, 2),
            'moving_avg_cost': round(avg_cost, 2)
        })
    
    return jsonify({
        'period_days': days,
        'trends': trends
    }), 200


@bp.route('/high-utilizers', methods=['GET'])
def get_high_utilizers():
    """Find members with high utilization using CTEs concept"""
    days = request.args.get('days', 90, type=int)
    min_claims = request.args.get('min_claims', 5, type=int)
    start_date = datetime.utcnow().date() - timedelta(days=days)
    
    # Aggregate by member
    high_utilizers = db.session.query(
        Member.id,
        Member.member_id,
        Member.first_name,
        Member.last_name,
        func.count(Claim.id).label('claim_count'),
        func.sum(Claim.total_cost).label('total_cost'),
        func.avg(Claim.total_cost).label('avg_cost_per_claim')
    ).join(Claim).filter(
        Claim.fill_date >= start_date
    ).group_by(
        Member.id, Member.member_id, Member.first_name, Member.last_name
    ).having(
        func.count(Claim.id) >= min_claims
    ).order_by(
        func.sum(Claim.total_cost).desc()
    ).limit(20).all()
    
    return jsonify({
        'period_days': days,
        'min_claims': min_claims,
        'high_utilizers': [
            {
                'member_id': row.member_id,
                'name': f"{row.first_name} {row.last_name}",
                'claim_count': row.claim_count,
                'total_cost': float(row.total_cost),
                'avg_cost_per_claim': float(row.avg_cost_per_claim)
            } for row in high_utilizers
        ]
    }), 200


@bp.route('/pharmacy-performance', methods=['GET'])
def get_pharmacy_performance():
    """Analyze pharmacy network performance"""
    days = request.args.get('days', 90, type=int)
    start_date = datetime.utcnow().date() - timedelta(days=days)
    
    pharmacy_stats = db.session.query(
        Pharmacy.name,
        Pharmacy.chain_name,
        Pharmacy.network_tier,
        func.count(Claim.id).label('claim_count'),
        func.sum(Claim.total_cost).label('total_cost'),
        func.avg(Claim.total_cost).label('avg_cost'),
        func.count(case((Claim.status == 'denied', 1))).label('denied_count')
    ).join(Claim).filter(
        Claim.fill_date >= start_date
    ).group_by(
        Pharmacy.id, Pharmacy.name, Pharmacy.chain_name, Pharmacy.network_tier
    ).order_by(
        func.count(Claim.id).desc()
    ).limit(20).all()
    
    return jsonify({
        'period_days': days,
        'pharmacies': [
            {
                'name': row.name,
                'chain': row.chain_name,
                'network_tier': row.network_tier,
                'claims': row.claim_count,
                'total_cost': float(row.total_cost),
                'avg_cost': float(row.avg_cost),
                'denied_claims': row.denied_count,
                'denial_rate': round((row.denied_count / row.claim_count * 100), 2) if row.claim_count > 0 else 0
            } for row in pharmacy_stats
        ]
    }), 200


@bp.route('/therapeutic-class', methods=['GET'])
def get_therapeutic_class_breakdown():
    """Breakdown by therapeutic class"""
    days = request.args.get('days', 90, type=int)
    start_date = datetime.utcnow().date() - timedelta(days=days)
    
    class_stats = db.session.query(
        Drug.therapeutic_class,
        func.count(Claim.id).label('claim_count'),
        func.sum(Claim.total_cost).label('total_cost'),
        func.count(func.distinct(Claim.member_id)).label('unique_members')
    ).join(Drug).filter(
        Claim.fill_date >= start_date,
        Drug.therapeutic_class.isnot(None)
    ).group_by(Drug.therapeutic_class).order_by(
        func.sum(Claim.total_cost).desc()
    ).all()
    
    return jsonify({
        'period_days': days,
        'therapeutic_classes': [
            {
                'class': row.therapeutic_class,
                'claims': row.claim_count,
                'total_cost': float(row.total_cost),
                'unique_members': row.unique_members,
                'avg_cost_per_claim': float(row.total_cost / row.claim_count) if row.claim_count > 0 else 0
            } for row in class_stats
        ]
    }), 200

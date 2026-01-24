from flask import Blueprint, request, jsonify
from app import db
from app.models import Claim, Member, Drug, Pharmacy
from datetime import datetime
from sqlalchemy import or_, and_, func

bp = Blueprint('claims', __name__, url_prefix='/api/claims')


@bp.route('', methods=['GET'])
def get_claims():
    """Get all claims with filtering and pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', '')
    member_id = request.args.get('member_id', type=int)
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    
    query = Claim.query
    
    if status:
        query = query.filter(Claim.status == status)
    
    if member_id:
        query = query.filter(Claim.member_id == member_id)
    
    if start_date:
        query = query.filter(Claim.fill_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    
    if end_date:
        query = query.filter(Claim.fill_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    query = query.order_by(Claim.fill_date.desc())
    
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'claims': [claim.to_dict() for claim in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page
    }), 200


@bp.route('/<int:claim_id>', methods=['GET'])
def get_claim(claim_id):
    """Get a specific claim by ID"""
    claim = Claim.query.get_or_404(claim_id)
    
    # Include related data
    result = claim.to_dict()
    result['member'] = claim.member.to_dict() if claim.member else None
    result['drug'] = claim.drug.to_dict() if claim.drug else None
    result['pharmacy'] = claim.pharmacy.to_dict() if claim.pharmacy else None
    
    return jsonify(result), 200


@bp.route('', methods=['POST'])
def create_claim():
    """Create a new claim"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['claim_number', 'member_id', 'drug_id', 'pharmacy_id', 
                       'fill_date', 'quantity', 'days_supply', 'total_cost']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Verify foreign keys exist
    member = Member.query.get(data['member_id'])
    if not member:
        return jsonify({'error': 'Member not found'}), 404
    
    drug = Drug.query.get(data['drug_id'])
    if not drug:
        return jsonify({'error': 'Drug not found'}), 404
    
    pharmacy = Pharmacy.query.get(data['pharmacy_id'])
    if not pharmacy:
        return jsonify({'error': 'Pharmacy not found'}), 404
    
    if Claim.query.filter_by(claim_number=data['claim_number']).first():
        return jsonify({'error': 'Claim number already exists'}), 409
    
    try:
        claim = Claim(
            claim_number=data['claim_number'],
            rx_number=data.get('rx_number'),
            member_id=data['member_id'],
            drug_id=data['drug_id'],
            pharmacy_id=data['pharmacy_id'],
            fill_date=datetime.strptime(data['fill_date'], '%Y-%m-%d').date(),
            service_date=datetime.strptime(data['service_date'], '%Y-%m-%d').date() if data.get('service_date') else None,
            quantity=data['quantity'],
            days_supply=data['days_supply'],
            refills_authorized=data.get('refills_authorized'),
            refill_number=data.get('refill_number', 0),
            prescriber_npi=data.get('prescriber_npi'),
            prescriber_name=data.get('prescriber_name'),
            submitted_amount=data.get('submitted_amount', data['total_cost']),
            ingredient_cost=data.get('ingredient_cost'),
            dispensing_fee=data.get('dispensing_fee'),
            sales_tax=data.get('sales_tax'),
            plan_paid_amount=data.get('plan_paid_amount'),
            member_copay=data.get('member_copay'),
            member_coinsurance=data.get('member_coinsurance'),
            deductible_applied=data.get('deductible_applied'),
            total_cost=data['total_cost'],
            status=data.get('status', 'pending'),
            is_generic_substitution=data.get('is_generic_substitution', False),
            requires_prior_auth=data.get('requires_prior_auth', False),
            is_compound=data.get('is_compound', False),
            is_specialty=data.get('is_specialty', False)
        )
        
        db.session.add(claim)
        db.session.commit()
        
        return jsonify(claim.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:claim_id>', methods=['PUT'])
def update_claim(claim_id):
    """Update an existing claim"""
    claim = Claim.query.get_or_404(claim_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # Update status and timestamps
        if 'status' in data:
            claim.status = data['status']
            if data['status'] == 'approved' and not claim.processed_at:
                claim.processed_at = datetime.utcnow()
            elif data['status'] == 'paid' and not claim.paid_at:
                claim.paid_at = datetime.utcnow()
        
        # Update other fields
        updatable_fields = [
            'rx_number', 'quantity', 'days_supply', 'refills_authorized',
            'refill_number', 'prescriber_npi', 'prescriber_name',
            'submitted_amount', 'ingredient_cost', 'dispensing_fee', 'sales_tax',
            'plan_paid_amount', 'member_copay', 'member_coinsurance',
            'deductible_applied', 'total_cost', 'rejection_code', 'rejection_reason',
            'is_generic_substitution', 'requires_prior_auth', 'is_compound', 'is_specialty'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(claim, field, data[field])
        
        db.session.commit()
        return jsonify(claim.to_dict()), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:claim_id>', methods=['DELETE'])
def delete_claim(claim_id):
    """Delete a claim (reverse it)"""
    claim = Claim.query.get_or_404(claim_id)
    
    try:
        claim.status = 'reversed'
        db.session.commit()
        return jsonify({'message': 'Claim reversed successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

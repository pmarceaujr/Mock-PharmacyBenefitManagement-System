from flask import Blueprint, request, jsonify
from app import db
from app.models import Member
from datetime import datetime
from sqlalchemy import or_

bp = Blueprint('members', __name__, url_prefix='/api/members')


@bp.route('', methods=['GET'])
def get_members():
    """Get all members with optional filtering and pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    is_active = request.args.get('is_active', type=lambda v: v.lower() == 'true')
    
    query = Member.query
    
    if search:
        search_filter = f'%{search}%'
        query = query.filter(
            or_(
                Member.first_name.ilike(search_filter),
                Member.last_name.ilike(search_filter),
                Member.member_id.ilike(search_filter),
                Member.email.ilike(search_filter)
            )
        )
    
    if is_active is not None:
        query = query.filter(Member.is_active == is_active)
    
    query = query.order_by(Member.last_name, Member.first_name)
    
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'members': [member.to_dict() for member in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page
    }), 200


@bp.route('/<int:member_id>', methods=['GET'])
def get_member(member_id):
    """Get a specific member by ID"""
    member = Member.query.get_or_404(member_id)
    return jsonify(member.to_dict()), 200


@bp.route('', methods=['POST'])
def create_member():
    """Create a new member"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['member_id', 'first_name', 'last_name', 'date_of_birth']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    if Member.query.filter_by(member_id=data['member_id']).first():
        return jsonify({'error': 'Member ID already exists'}), 409
    
    try:
        member = Member(
            member_id=data['member_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date(),
            gender=data.get('gender'),
            email=data.get('email'),
            phone=data.get('phone'),
            address_line1=data.get('address_line1'),
            address_line2=data.get('address_line2'),
            city=data.get('city'),
            state=data.get('state'),
            zip_code=data.get('zip_code'),
            plan_type=data.get('plan_type'),
            group_id=data.get('group_id'),
            effective_date=datetime.strptime(data['effective_date'], '%Y-%m-%d').date() if data.get('effective_date') else None,
            termination_date=datetime.strptime(data['termination_date'], '%Y-%m-%d').date() if data.get('termination_date') else None,
            is_active=data.get('is_active', True)
        )
        
        db.session.add(member)
        db.session.commit()
        
        return jsonify(member.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    """Update an existing member"""
    member = Member.query.get_or_404(member_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        if 'first_name' in data:
            member.first_name = data['first_name']
        if 'last_name' in data:
            member.last_name = data['last_name']
        if 'date_of_birth' in data:
            member.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        if 'gender' in data:
            member.gender = data['gender']
        if 'email' in data:
            member.email = data['email']
        if 'phone' in data:
            member.phone = data['phone']
        if 'address_line1' in data:
            member.address_line1 = data['address_line1']
        if 'address_line2' in data:
            member.address_line2 = data['address_line2']
        if 'city' in data:
            member.city = data['city']
        if 'state' in data:
            member.state = data['state']
        if 'zip_code' in data:
            member.zip_code = data['zip_code']
        if 'plan_type' in data:
            member.plan_type = data['plan_type']
        if 'group_id' in data:
            member.group_id = data['group_id']
        if 'is_active' in data:
            member.is_active = data['is_active']
        
        db.session.commit()
        return jsonify(member.to_dict()), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    """Delete a member"""
    member = Member.query.get_or_404(member_id)
    
    try:
        db.session.delete(member)
        db.session.commit()
        return jsonify({'message': 'Member deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:member_id>/claims', methods=['GET'])
def get_member_claims(member_id):
    """Get all claims for a specific member"""
    member = Member.query.get_or_404(member_id)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    paginated = member.claims.order_by('fill_date DESC').paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'member_id': member.id,
        'claims': [claim.to_dict() for claim in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page
    }), 200

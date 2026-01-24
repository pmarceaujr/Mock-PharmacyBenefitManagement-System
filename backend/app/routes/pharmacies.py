from flask import Blueprint, request, jsonify
from app import db
from app.models import Pharmacy
from sqlalchemy import or_, func

bp = Blueprint('pharmacies', __name__, url_prefix='/api/pharmacies')


@bp.route('', methods=['GET'])
def get_pharmacies():
    """Get all pharmacies with optional filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    city = request.args.get('city', '')
    state = request.args.get('state', '')
    in_network = request.args.get('in_network', type=lambda v: v.lower() == 'true')
    
    query = Pharmacy.query
    
    if search:
        search_filter = f'%{search}%'
        query = query.filter(
            or_(
                Pharmacy.name.ilike(search_filter),
                Pharmacy.chain_name.ilike(search_filter),
                Pharmacy.ncpdp_id.ilike(search_filter)
            )
        )
    
    if city:
        query = query.filter(Pharmacy.city.ilike(f'%{city}%'))
    
    if state:
        query = query.filter(Pharmacy.state == state.upper())
    
    if in_network is not None:
        query = query.filter(Pharmacy.in_network == in_network)
    
    query = query.filter(Pharmacy.is_active == True).order_by(Pharmacy.name)
    
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'pharmacies': [pharmacy.to_dict() for pharmacy in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page
    }), 200


@bp.route('/<int:pharmacy_id>', methods=['GET'])
def get_pharmacy(pharmacy_id):
    """Get a specific pharmacy by ID"""
    pharmacy = Pharmacy.query.get_or_404(pharmacy_id)
    return jsonify(pharmacy.to_dict()), 200


@bp.route('', methods=['POST'])
def create_pharmacy():
    """Create a new pharmacy"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['ncpdp_id', 'name', 'address_line1', 'city', 'state', 'zip_code']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    if Pharmacy.query.filter_by(ncpdp_id=data['ncpdp_id']).first():
        return jsonify({'error': 'NCPDP ID already exists'}), 409
    
    try:
        pharmacy = Pharmacy(
            ncpdp_id=data['ncpdp_id'],
            npi=data.get('npi'),
            name=data['name'],
            chain_name=data.get('chain_name'),
            phone=data.get('phone'),
            fax=data.get('fax'),
            email=data.get('email'),
            address_line1=data['address_line1'],
            address_line2=data.get('address_line2'),
            city=data['city'],
            state=data['state'],
            zip_code=data['zip_code'],
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            pharmacy_type=data.get('pharmacy_type'),
            is_24_hours=data.get('is_24_hours', False),
            accepts_new_patients=data.get('accepts_new_patients', True),
            in_network=data.get('in_network', True),
            network_tier=data.get('network_tier'),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(pharmacy)
        db.session.commit()
        
        return jsonify(pharmacy.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:pharmacy_id>', methods=['PUT'])
def update_pharmacy(pharmacy_id):
    """Update an existing pharmacy"""
    pharmacy = Pharmacy.query.get_or_404(pharmacy_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        updatable_fields = [
            'name', 'chain_name', 'phone', 'fax', 'email',
            'address_line1', 'address_line2', 'city', 'state', 'zip_code',
            'latitude', 'longitude', 'pharmacy_type', 'is_24_hours',
            'accepts_new_patients', 'in_network', 'network_tier', 'is_active'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(pharmacy, field, data[field])
        
        db.session.commit()
        return jsonify(pharmacy.to_dict()), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

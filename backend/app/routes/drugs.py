from flask import Blueprint, request, jsonify
from app import db
from app.models import Drug
from sqlalchemy import or_, func

bp = Blueprint('drugs', __name__, url_prefix='/api/drugs')


@bp.route('', methods=['GET'])
def get_drugs():
    """Get all drugs with optional filtering and pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    is_generic = request.args.get('is_generic', type=lambda v: v.lower() == 'true')
    therapeutic_class = request.args.get('therapeutic_class', '')
    
    query = Drug.query
    
    if search:
        search_filter = f'%{search}%'
        query = query.filter(
            or_(
                Drug.name.ilike(search_filter),
                Drug.generic_name.ilike(search_filter),
                Drug.brand_name.ilike(search_filter),
                Drug.ndc.ilike(search_filter)
            )
        )
    
    if is_generic is not None:
        query = query.filter(Drug.is_generic == is_generic)
    
    if therapeutic_class:
        query = query.filter(Drug.therapeutic_class.ilike(f'%{therapeutic_class}%'))
    
    query = query.filter(Drug.is_active == True).order_by(Drug.name)
    
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'drugs': [drug.to_dict() for drug in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page
    }), 200


@bp.route('/<int:drug_id>', methods=['GET'])
def get_drug(drug_id):
    """Get a specific drug by ID"""
    drug = Drug.query.get_or_404(drug_id)
    return jsonify(drug.to_dict()), 200


@bp.route('/search', methods=['GET'])
def search_drugs():
    """Full-text search for drugs"""
    query_text = request.args.get('q', '')
    limit = request.args.get('limit', 10, type=int)
    
    if not query_text:
        return jsonify({'error': 'Search query required'}), 400
    
    # Simple ILIKE search (full-text search would use search_vector)
    search_filter = f'%{query_text}%'
    drugs = Drug.query.filter(
        or_(
            Drug.name.ilike(search_filter),
            Drug.generic_name.ilike(search_filter),
            Drug.brand_name.ilike(search_filter)
        ),
        Drug.is_active == True
    ).limit(limit).all()
    
    return jsonify({
        'query': query_text,
        'results': [drug.to_dict() for drug in drugs]
    }), 200


@bp.route('', methods=['POST'])
def create_drug():
    """Create a new drug"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['ndc', 'name']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    if Drug.query.filter_by(ndc=data['ndc']).first():
        return jsonify({'error': 'NDC already exists'}), 409
    
    try:
        drug = Drug(
            ndc=data['ndc'],
            name=data['name'],
            generic_name=data.get('generic_name'),
            brand_name=data.get('brand_name'),
            is_generic=data.get('is_generic', True),
            therapeutic_class=data.get('therapeutic_class'),
            drug_class=data.get('drug_class'),
            strength=data.get('strength'),
            dosage_form=data.get('dosage_form'),
            route=data.get('route'),
            manufacturer=data.get('manufacturer'),
            awp=data.get('awp'),
            package_size=data.get('package_size'),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(drug)
        db.session.commit()
        
        return jsonify(drug.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:drug_id>', methods=['PUT'])
def update_drug(drug_id):
    """Update an existing drug"""
    drug = Drug.query.get_or_404(drug_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        updatable_fields = [
            'name', 'generic_name', 'brand_name', 'is_generic',
            'therapeutic_class', 'drug_class', 'strength', 'dosage_form',
            'route', 'manufacturer', 'awp', 'package_size', 'is_active'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(drug, field, data[field])
        
        db.session.commit()
        return jsonify(drug.to_dict()), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:drug_id>', methods=['DELETE'])
def delete_drug(drug_id):
    """Soft delete a drug (mark as inactive)"""
    drug = Drug.query.get_or_404(drug_id)
    
    try:
        drug.is_active = False
        db.session.commit()
        return jsonify({'message': 'Drug deactivated successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

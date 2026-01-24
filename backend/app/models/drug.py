from app import db
from datetime import datetime
from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import TSVECTOR


class Drug(db.Model):
    __tablename__ = 'drugs'
    
    id = db.Column(db.Integer, primary_key=True)
    ndc = db.Column(db.String(11), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    generic_name = db.Column(db.String(255))
    brand_name = db.Column(db.String(255))
    
    is_generic = db.Column(db.Boolean, default=True, nullable=False)
    therapeutic_class = db.Column(db.String(100))
    drug_class = db.Column(db.String(100))
    
    strength = db.Column(db.String(50))
    dosage_form = db.Column(db.String(50))
    route = db.Column(db.String(50))
    manufacturer = db.Column(db.String(255))
    
    awp = db.Column(db.Numeric(10, 2))
    package_size = db.Column(db.Integer)
    
    search_vector = db.Column(TSVECTOR)
    
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    claims = db.relationship('Claim', back_populates='drug', lazy='dynamic')
    formulary_entries = db.relationship('Formulary', back_populates='drug', lazy='dynamic')
    
    __table_args__ = (
        Index('idx_drug_generic', 'is_generic'),
        Index('idx_drug_class', 'therapeutic_class'),
        Index('idx_drug_active', 'is_active'),
        Index('idx_drug_search', 'search_vector', postgresql_using='gin'),
    )
    
    def __repr__(self):
        return f'<Drug {self.ndc}: {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'ndc': self.ndc,
            'name': self.name,
            'generic_name': self.generic_name,
            'brand_name': self.brand_name,
            'is_generic': self.is_generic,
            'therapeutic_class': self.therapeutic_class,
            'drug_class': self.drug_class,
            'strength': self.strength,
            'dosage_form': self.dosage_form,
            'route': self.route,
            'manufacturer': self.manufacturer,
            'awp': float(self.awp) if self.awp else None,
            'package_size': self.package_size,
            'is_active': self.is_active
        }

from app import db
from datetime import datetime
from sqlalchemy import Index


class Pharmacy(db.Model):
    __tablename__ = 'pharmacies'
    
    id = db.Column(db.Integer, primary_key=True)
    ncpdp_id = db.Column(db.String(7), unique=True, nullable=False, index=True)
    npi = db.Column(db.String(10), unique=True, index=True)
    name = db.Column(db.String(255), nullable=False)
    chain_name = db.Column(db.String(255))
    
    phone = db.Column(db.String(20))
    fax = db.Column(db.String(20))
    email = db.Column(db.String(255))
    
    address_line1 = db.Column(db.String(255), nullable=False)
    address_line2 = db.Column(db.String(255))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    
    latitude = db.Column(db.Numeric(10, 8))
    longitude = db.Column(db.Numeric(11, 8))
    
    pharmacy_type = db.Column(db.String(50))
    is_24_hours = db.Column(db.Boolean, default=False)
    accepts_new_patients = db.Column(db.Boolean, default=True)
    
    in_network = db.Column(db.Boolean, default=True, nullable=False)
    network_tier = db.Column(db.String(20))
    
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    claims = db.relationship('Claim', back_populates='pharmacy', lazy='dynamic')
    
    __table_args__ = (
        Index('idx_pharmacy_location', 'city', 'state', 'zip_code'),
        Index('idx_pharmacy_network', 'in_network', 'network_tier'),
        Index('idx_pharmacy_type', 'pharmacy_type'),
        Index('idx_pharmacy_coords', 'latitude', 'longitude'),
    )
    
    def __repr__(self):
        return f'<Pharmacy {self.ncpdp_id}: {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'ncpdp_id': self.ncpdp_id,
            'npi': self.npi,
            'name': self.name,
            'chain_name': self.chain_name,
            'phone': self.phone,
            'address': {
                'line1': self.address_line1,
                'line2': self.address_line2,
                'city': self.city,
                'state': self.state,
                'zip_code': self.zip_code
            },
            'location': {
                'latitude': float(self.latitude) if self.latitude else None,
                'longitude': float(self.longitude) if self.longitude else None
            },
            'pharmacy_type': self.pharmacy_type,
            'is_24_hours': self.is_24_hours,
            'in_network': self.in_network,
            'network_tier': self.network_tier,
            'is_active': self.is_active
        }

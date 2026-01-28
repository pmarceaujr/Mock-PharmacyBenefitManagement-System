from app import db
from datetime import datetime
from sqlalchemy import Index, CheckConstraint


class Claim(db.Model):
    __tablename__ = 'claims'
    
    id = db.Column(db.Integer, primary_key=True)
    claim_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    rx_number = db.Column(db.String(50))
    
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False, index=True)
    drug_id = db.Column(db.Integer, db.ForeignKey('drugs.id'), nullable=False, index=True)
    pharmacy_id = db.Column(db.Integer, db.ForeignKey('pharmacies.id'), nullable=False, index=True)
    
    fill_date = db.Column(db.Date, nullable=False, index=True)
    service_date = db.Column(db.Date)
    
    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    days_supply = db.Column(db.Integer, nullable=False)
    refills_authorized = db.Column(db.Integer)
    refill_number = db.Column(db.Integer, default=0)
    
    prescriber_npi = db.Column(db.String(10))
    prescriber_name = db.Column(db.String(255))
    
    submitted_amount = db.Column(db.Numeric(10, 2), nullable=False)
    ingredient_cost = db.Column(db.Numeric(10, 2))
    dispensing_fee = db.Column(db.Numeric(10, 2))
    sales_tax = db.Column(db.Numeric(10, 2))
    
    plan_paid_amount = db.Column(db.Numeric(10, 2))
    member_copay = db.Column(db.Numeric(10, 2))
    member_coinsurance = db.Column(db.Numeric(10, 2))
    deductible_applied = db.Column(db.Numeric(10, 2))
    
    total_cost = db.Column(db.Numeric(10, 2), nullable=False)
    
    status = db.Column(db.String(20), nullable=False, default='pending', index=True)
    rejection_code = db.Column(db.String(10))
    rejection_reason = db.Column(db.Text)
    
    is_generic_substitution = db.Column(db.Boolean, default=False)
    requires_prior_auth = db.Column(db.Boolean, default=False)
    is_compound = db.Column(db.Boolean, default=False)
    is_specialty = db.Column(db.Boolean, default=False)
    
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    processed_at = db.Column(db.DateTime)
    paid_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    member = db.relationship('Member', back_populates='claims')
    drug = db.relationship('Drug', back_populates='claims')
    pharmacy = db.relationship('Pharmacy', back_populates='claims')
    
    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
        CheckConstraint('days_supply > 0', name='check_days_supply_positive'),
        CheckConstraint('total_cost >= 0', name='check_total_cost_non_negative'),
        CheckConstraint("status IN ('pending', 'approved', 'paid', 'denied', 'reversed')", name='check_status_valid'),
        Index('idx_claim_dates', 'fill_date', 'status'),
        Index('idx_claim_member_date', 'member_id', 'fill_date'),
        Index('idx_claim_drug_date', 'drug_id', 'fill_date'),
        Index('idx_claim_status_date', 'status', 'fill_date'),
    )
    
    def __repr__(self):
        return f'<Claim {self.claim_number}: ${self.total_cost}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'claim_number': self.claim_number,
            'rx_number': self.rx_number,
            'member_id': self.member_id,
            # Add member info
            'member_name': f"{self.member.first_name} {self.member.last_name}" if self.member else None,
            'member_first_name': self.member.first_name if self.member else None,
            'member_last_name': self.member.last_name if self.member else None,            
            'drug_id': self.drug_id,
            # Add drug info
            'drug_name': self.drug.name if self.drug else None,
            'drug_generic_name': self.drug.generic_name if self.drug else None,
            'is_generic': self.drug.is_generic if self.drug else None,            
            'pharmacy_id': self.pharmacy_id,
            'fill_date': self.fill_date.isoformat() if self.fill_date else None,
            'quantity': float(self.quantity) if self.quantity else None,
            'days_supply': self.days_supply,
            'refills_authorized': self.refills_authorized,
            'refill_number': self.refill_number,
            'prescriber': {
                'npi': self.prescriber_npi,
                'name': self.prescriber_name
            },
            'pricing': {
                'submitted_amount': float(self.submitted_amount) if self.submitted_amount else None,
                'ingredient_cost': float(self.ingredient_cost) if self.ingredient_cost else None,
                'dispensing_fee': float(self.dispensing_fee) if self.dispensing_fee else None,
                'sales_tax': float(self.sales_tax) if self.sales_tax else None,
                'plan_paid_amount': float(self.plan_paid_amount) if self.plan_paid_amount else None,
                'member_copay': float(self.member_copay) if self.member_copay else None,
                'member_coinsurance': float(self.member_coinsurance) if self.member_coinsurance else None,
                'deductible_applied': float(self.deductible_applied) if self.deductible_applied else None,
                'total_cost': float(self.total_cost) if self.total_cost else None
            },
            'status': self.status,
            'rejection_code': self.rejection_code,
            'rejection_reason': self.rejection_reason,
            'flags': {
                'is_generic_substitution': self.is_generic_substitution,
                'requires_prior_auth': self.requires_prior_auth,
                'is_compound': self.is_compound,
                'is_specialty': self.is_specialty
            },
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None
        }

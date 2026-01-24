from app import db
from datetime import datetime
from sqlalchemy import Index, CheckConstraint


class Formulary(db.Model):
    __tablename__ = 'formulary'
    
    id = db.Column(db.Integer, primary_key=True)
    drug_id = db.Column(db.Integer, db.ForeignKey('drugs.id'), nullable=False, index=True)
    
    tier = db.Column(db.Integer, nullable=False)
    tier_name = db.Column(db.String(50))
    
    is_covered = db.Column(db.Boolean, default=True, nullable=False)
    requires_prior_auth = db.Column(db.Boolean, default=False)
    requires_step_therapy = db.Column(db.Boolean, default=False)
    quantity_limit = db.Column(db.Integer)
    
    copay_retail = db.Column(db.Numeric(10, 2))
    copay_mail_order = db.Column(db.Numeric(10, 2))
    coinsurance_rate = db.Column(db.Numeric(5, 4))
    
    effective_date = db.Column(db.Date, nullable=False)
    termination_date = db.Column(db.Date)
    
    coverage_notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    drug = db.relationship('Drug', back_populates='formulary_entries')
    
    __table_args__ = (
        CheckConstraint('tier BETWEEN 1 AND 5', name='check_tier_range'),
        CheckConstraint('coinsurance_rate IS NULL OR (coinsurance_rate >= 0 AND coinsurance_rate <= 1)', 
                       name='check_coinsurance_rate'),
        Index('idx_formulary_tier', 'tier'),
        Index('idx_formulary_coverage', 'is_covered'),
        Index('idx_formulary_dates', 'effective_date', 'termination_date'),
        Index('idx_formulary_drug_effective', 'drug_id', 'effective_date'),
    )
    
    def __repr__(self):
        return f'<Formulary Drug ID {self.drug_id}: Tier {self.tier}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'drug_id': self.drug_id,
            'tier': self.tier,
            'tier_name': self.tier_name,
            'is_covered': self.is_covered,
            'requires_prior_auth': self.requires_prior_auth,
            'requires_step_therapy': self.requires_step_therapy,
            'quantity_limit': self.quantity_limit,
            'cost_sharing': {
                'copay_retail': float(self.copay_retail) if self.copay_retail else None,
                'copay_mail_order': float(self.copay_mail_order) if self.copay_mail_order else None,
                'coinsurance_rate': float(self.coinsurance_rate) if self.coinsurance_rate else None
            },
            'effective_date': self.effective_date.isoformat() if self.effective_date else None,
            'termination_date': self.termination_date.isoformat() if self.termination_date else None,
            'coverage_notes': self.coverage_notes
        }

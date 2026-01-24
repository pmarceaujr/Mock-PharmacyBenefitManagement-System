from app import db
from datetime import datetime
from sqlalchemy import Index


class Member(db.Model):
    __tablename__ = 'members'
    
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20))
    email = db.Column(db.String(255), unique=True, index=True)
    phone = db.Column(db.String(20))
    
    address_line1 = db.Column(db.String(255))
    address_line2 = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(10))
    
    plan_type = db.Column(db.String(50))
    group_id = db.Column(db.String(50))
    effective_date = db.Column(db.Date)
    termination_date = db.Column(db.Date)
    
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    claims = db.relationship('Claim', back_populates='member', lazy='dynamic', cascade='all, delete-orphan')
    
    __table_args__ = (
        Index('idx_member_name', 'last_name', 'first_name'),
        Index('idx_member_dob', 'date_of_birth'),
        Index('idx_member_active', 'is_active'),
    )
    
    def __repr__(self):
        return f'<Member {self.member_id}: {self.first_name} {self.last_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'member_id': self.member_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'email': self.email,
            'phone': self.phone,
            'address': {
                'line1': self.address_line1,
                'line2': self.address_line2,
                'city': self.city,
                'state': self.state,
                'zip_code': self.zip_code
            },
            'plan_type': self.plan_type,
            'group_id': self.group_id,
            'effective_date': self.effective_date.isoformat() if self.effective_date else None,
            'termination_date': self.termination_date.isoformat() if self.termination_date else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

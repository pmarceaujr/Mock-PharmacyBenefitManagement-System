"""
Pytest configuration and fixtures
"""

import pytest
from app import create_app, db
from app.models import Member, Drug, Pharmacy, Claim
from datetime import datetime, date
from decimal import Decimal


@pytest.fixture(scope='session')
def app():
    """Create application for testing"""
    app = create_app('testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://prescriptiontrack_user:dev_password_123@localhost:5432/prescriptiontrack_test'
    app.config['TESTING'] = True
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Test client"""
    return app.test_client()


@pytest.fixture(scope='function')
def session(app):
    """Database session for tests"""
    with app.app_context():
        yield db.session
        db.session.rollback()
        # Clean up all tables
        db.session.query(Claim).delete()
        db.session.query(Member).delete()
        db.session.query(Drug).delete()
        db.session.query(Pharmacy).delete()
        db.session.commit()


@pytest.fixture
def sample_member(session):
    """Create a sample member"""
    member = Member(
        member_id='MBR000001',
        first_name='John',
        last_name='Doe',
        date_of_birth=date(1980, 1, 1),
        gender='Male',
        email='john.doe@example.com',
        phone='555-0100',
        address_line1='123 Main St',
        city='Boston',
        state='MA',
        zip_code='02101',
        plan_type='PPO',
        group_id='GRP1000',
        effective_date=date(2024, 1, 1),
        is_active=True
    )
    session.add(member)
    session.commit()
    return member


@pytest.fixture
def sample_drug(session):
    """Create a sample drug"""
    drug = Drug(
        ndc='12345-678-90',
        name='Atorvastatin',
        generic_name='Atorvastatin',
        brand_name=None,
        is_generic=True,
        therapeutic_class='Lipid-Lowering',
        drug_class='Statin',
        strength='20mg',
        dosage_form='Tablet',
        route='Oral',
        manufacturer='Generic Manufacturer',
        awp=Decimal('50.00'),
        package_size=30,
        is_active=True
    )
    session.add(drug)
    session.commit()
    return drug


@pytest.fixture
def sample_pharmacy(session):
    """Create a sample pharmacy"""
    pharmacy = Pharmacy(
        ncpdp_id='1234567',
        npi='1234567890',
        name='Test Pharmacy',
        chain_name='CVS',
        phone='555-0200',
        address_line1='456 Elm St',
        city='Boston',
        state='MA',
        zip_code='02102',
        latitude=Decimal('42.3601'),
        longitude=Decimal('-71.0589'),
        pharmacy_type='Retail',
        is_24_hours=False,
        in_network=True,
        network_tier='Preferred',
        is_active=True
    )
    session.add(pharmacy)
    session.commit()
    return pharmacy


@pytest.fixture
def sample_claim(session, sample_member, sample_drug, sample_pharmacy):
    """Create a sample claim"""
    claim = Claim(
        claim_number='CLM00000001',
        rx_number='RX123456',
        member_id=sample_member.id,
        drug_id=sample_drug.id,
        pharmacy_id=sample_pharmacy.id,
        fill_date=date.today(),
        quantity=Decimal('30'),
        days_supply=30,
        refills_authorized=3,
        refill_number=0,
        prescriber_npi='9876543210',
        prescriber_name='Dr. Smith',
        submitted_amount=Decimal('55.00'),
        ingredient_cost=Decimal('50.00'),
        dispensing_fee=Decimal('2.50'),
        sales_tax=Decimal('2.50'),
        plan_paid_amount=Decimal('45.00'),
        member_copay=Decimal('10.00'),
        total_cost=Decimal('55.00'),
        status='paid',
        is_generic_substitution=False,
        requires_prior_auth=False,
        is_compound=False,
        is_specialty=False
    )
    session.add(claim)
    session.commit()
    return claim

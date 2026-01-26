"""
Unit tests for database models
"""

import pytest
from datetime import date
from decimal import Decimal
from app.models import Member, Drug, Pharmacy, Claim


def test_member_creation(sample_member):
    """Test member model creation"""
    assert sample_member.id is not None
    assert sample_member.member_id == 'MBR000001'
    assert sample_member.first_name == 'John'
    assert sample_member.last_name == 'Doe'
    assert sample_member.is_active == True


def test_member_to_dict(sample_member):
    """Test member to_dict method"""
    member_dict = sample_member.to_dict()
    assert member_dict['member_id'] == 'MBR000001'
    assert member_dict['first_name'] == 'John'
    assert member_dict['email'] == 'john.doe@example.com'
    assert 'address' in member_dict


def test_drug_creation(sample_drug):
    """Test drug model creation"""
    assert sample_drug.id is not None
    assert sample_drug.ndc == '12345-678-90'
    assert sample_drug.name == 'Atorvastatin'
    assert sample_drug.is_generic == True
    assert sample_drug.awp == Decimal('50.00')


def test_drug_to_dict(sample_drug):
    """Test drug to_dict method"""
    drug_dict = sample_drug.to_dict()
    assert drug_dict['ndc'] == '12345-678-90'
    assert drug_dict['is_generic'] == True
    assert drug_dict['awp'] == 50.00


def test_pharmacy_creation(sample_pharmacy):
    """Test pharmacy model creation"""
    assert sample_pharmacy.id is not None
    assert sample_pharmacy.ncpdp_id == '1234567'
    assert sample_pharmacy.name == 'Test Pharmacy'
    assert sample_pharmacy.in_network == True


def test_pharmacy_to_dict(sample_pharmacy):
    """Test pharmacy to_dict method"""
    pharmacy_dict = sample_pharmacy.to_dict()
    assert pharmacy_dict['ncpdp_id'] == '1234567'
    assert 'address' in pharmacy_dict
    assert 'location' in pharmacy_dict


def test_claim_creation(sample_claim):
    """Test claim model creation"""
    assert sample_claim.id is not None
    assert sample_claim.claim_number == 'CLM00000001'
    assert sample_claim.status == 'paid'
    assert sample_claim.total_cost == Decimal('55.00')


def test_claim_to_dict(sample_claim):
    """Test claim to_dict method"""
    claim_dict = sample_claim.to_dict()
    assert claim_dict['claim_number'] == 'CLM00000001'
    assert 'pricing' in claim_dict
    assert 'flags' in claim_dict
    assert claim_dict['status'] == 'paid'


def test_claim_relationships(sample_claim):
    """Test claim relationships"""
    assert sample_claim.member is not None
    assert sample_claim.drug is not None
    assert sample_claim.pharmacy is not None
    assert sample_claim.member.first_name == 'John'
    assert sample_claim.drug.name == 'Atorvastatin'
    assert sample_claim.pharmacy.name == 'Test Pharmacy'

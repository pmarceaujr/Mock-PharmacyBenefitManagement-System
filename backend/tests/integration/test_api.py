"""
Integration tests for API endpoints
"""

import pytest
import json
from datetime import date


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'endpoints' in data


def test_get_members(client, sample_member):
    """Test GET /api/members"""
    response = client.get('/api/members')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'members' in data
    assert len(data['members']) == 1
    assert data['members'][0]['member_id'] == 'MBR000001'


def test_get_member_by_id(client, sample_member):
    """Test GET /api/members/<id>"""
    response = client.get(f'/api/members/{sample_member.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['member_id'] == 'MBR000001'
    assert data['first_name'] == 'John'


def test_create_member(client):
    """Test POST /api/members"""
    new_member = {
        'member_id': 'MBR000002',
        'first_name': 'Jane',
        'last_name': 'Smith',
        'date_of_birth': '1985-06-15',
        'email': 'jane.smith@example.com',
        'plan_type': 'HMO',
        'is_active': True
    }
    response = client.post('/api/members',
                          data=json.dumps(new_member),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['member_id'] == 'MBR000002'
    assert data['first_name'] == 'Jane'


def test_update_member(client, sample_member):
    """Test PUT /api/members/<id>"""
    update_data = {
        'phone': '555-9999',
        'city': 'Cambridge'
    }
    response = client.put(f'/api/members/{sample_member.id}',
                         data=json.dumps(update_data),
                         content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['phone'] == '555-9999'
    assert data['address']['city'] == 'Cambridge'


def test_get_drugs(client, sample_drug):
    """Test GET /api/drugs"""
    response = client.get('/api/drugs')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'drugs' in data
    assert len(data['drugs']) == 1


def test_search_drugs(client, sample_drug):
    """Test GET /api/drugs/search"""
    response = client.get('/api/drugs/search?q=Ator')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'results' in data
    assert len(data['results']) > 0


def test_get_claims(client, sample_claim):
    """Test GET /api/claims"""
    response = client.get('/api/claims')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'claims' in data
    assert len(data['claims']) == 1


def test_get_claim_with_details(client, sample_claim):
    """Test GET /api/claims/<id> with related data"""
    response = client.get(f'/api/claims/{sample_claim.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'member' in data
    assert 'drug' in data
    assert 'pharmacy' in data
    assert data['claim_number'] == 'CLM00000001'


def test_update_claim_status(client, sample_claim):
    """Test PUT /api/claims/<id> to update status"""
    update_data = {'status': 'approved'}
    response = client.put(f'/api/claims/{sample_claim.id}',
                         data=json.dumps(update_data),
                         content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'approved'
    assert data['processed_at'] is not None


def test_analytics_dashboard(client, sample_claim):
    """Test GET /api/analytics/dashboard"""
    response = client.get('/api/analytics/dashboard?days=30')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'summary' in data
    assert 'generic_vs_brand' in data
    assert 'top_drugs' in data


def test_analytics_trends(client, sample_claim):
    """Test GET /api/analytics/trends"""
    response = client.get('/api/analytics/trends?days=30')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'trends' in data


def test_generic_savings_report(client, sample_claim):
    """Test GET /api/reports/generic-savings"""
    response = client.get('/api/reports/generic-savings?days=90')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'total_potential_savings' in data
    assert 'opportunities' in data


def test_cost_summary_report(client, sample_claim):
    """Test GET /api/reports/cost-summary"""
    response = client.get('/api/reports/cost-summary')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'overall_summary' in data
    assert 'by_status' in data


def test_member_summary_report(client, sample_member, sample_claim):
    """Test GET /api/reports/member-summary/<id>"""
    response = client.get(f'/api/reports/member-summary/{sample_member.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'member' in data
    assert 'summary' in data
    assert 'most_used_drugs' in data

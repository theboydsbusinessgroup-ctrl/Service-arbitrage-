from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)

def test_offer_is_fixed_scope():
    d=client.get('/offer').json(); assert d['sale_price']==99; assert d['fulfillment_ceiling']==35; assert d['minimum_contribution']==40; assert d['revisions']==1

def test_preflight_accepts_profitable_order():
    r=client.post('/orders/preflight',json={'customer_email':'buyer@example.com','business_name':'Acme','headline':'Grand Opening','body_copy':'Visit us this weekend.','call_to_action':'Call today','fulfillment_cost_estimate':35})
    assert r.status_code==200; d=r.json(); assert d['accepted'] is True; assert d['state']=='PAYMENT_READY'; assert d['projected_contribution']==60; assert d['scope_locked'] is True

def test_preflight_rejects_cost_above_ceiling():
    r=client.post('/orders/preflight',json={'customer_email':'buyer@example.com','business_name':'Acme','headline':'Sale','body_copy':'Details','call_to_action':'Call','fulfillment_cost_estimate':40})
    assert r.status_code==409

def test_provider_rank_excludes_expensive_provider():
    r=client.post('/providers/rank',json=[{'provider_id':'a','name':'Good','cost':30,'quality_score':90,'reliability_score':90,'sla_hours':48},{'provider_id':'b','name':'Too Expensive','cost':45,'quality_score':100,'reliability_score':100,'sla_hours':24}])
    assert r.status_code==200; assert r.json()['eligible_count']==1; assert r.json()['providers'][0]['provider_id']=='a'

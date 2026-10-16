import runpy
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_legacy_entrypoint_uses_the_same_application():
    entrypoint = Path(__file__).resolve().parents[1] / 'app.py'
    assert runpy.run_path(str(entrypoint))['app'] is app


def test_rank_requires_documented_quality_reliability_and_sla():
    baseline = {'provider_id': 'approved', 'name': 'Provider', 'cost': 35,
                'quality_score': 85, 'reliability_score': 85, 'sla_hours': 72}
    providers = [baseline,
                 {**baseline, 'provider_id': 'poor_quality', 'quality_score': 84},
                 {**baseline, 'provider_id': 'unreliable', 'reliability_score': 84},
                 {**baseline, 'provider_id': 'late', 'sla_hours': 73}]
    response = client.post('/providers/rank', json=providers)
    assert response.status_code == 200
    assert [p['provider_id'] for p in response.json()['providers']] == ['approved']

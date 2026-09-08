from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_margin_accepts_profitable_job():
    response = client.post("/margin/check", json={
        "sale_price": 99,
        "fulfillment_cost": 35,
        "payment_fees": 4,
        "other_costs": 0,
        "minimum_contribution": 40,
    })
    assert response.status_code == 200
    assert response.json()["accepted"] is True
    assert response.json()["contribution"] == 60

def test_margin_rejects_low_contribution():
    response = client.post("/margin/check", json={
        "sale_price": 50,
        "fulfillment_cost": 35,
        "payment_fees": 3,
        "other_costs": 0,
        "minimum_contribution": 40,
    })
    assert response.status_code == 200
    assert response.json()["accepted"] is False

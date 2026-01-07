from fastapi.testclient import TestClient
from emprunt.app import app

client = TestClient(app)

def test_index_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Emprunt" in response.text

def test_simulate_endpoint():
    data = {
        "home_cost": "1,000,000",
        "annual_rate": "3.5",
        "years": "25",
        "savings": "500,000",
        "investment_rate": "5.0",
        "monthly_cash": "6,000",
        "s1_down_payment": "200,000",
        "s2_down_payment": "400,000"
    }
    response = client.post("/simulate", data=data)
    assert response.status_code == 200
    assert "Scenario Comparison" in response.text
    # Check if the results are present
    assert "Down Payment: €200,000" in response.text
    assert "Down Payment: €400,000" in response.text

def test_api_simulate_endpoint():
    payload = {
        "home_cost": 1000000,
        "down_payment": 200000,
        "annual_rate": 3.5,
        "years": 25,
        "savings": 500000,
        "investment_rate": 5.0,
        "monthly_cash": 6000
    }
    response = client.post("/api/simulate", json=payload)
    assert response.status_code == 200
    assert "payment" in response.json()

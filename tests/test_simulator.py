import pytest
from emprunt.simulator import simulate_mortgage


def test_simulator_basic():
    # home_cost, down_payment, annual_rate, years, savings, investment_rate, monthly_cash
    res = simulate_mortgage(100000, 20000, 3.5, 20, 30000, 5.0, 1000)
    assert "payment" in res
    assert "schedule" in res
    assert len(res["schedule"]) == 20 * 12
    assert res["payment"] > 0

def test_simulator_zero_rate():
    res = simulate_mortgage(100000, 0, 0, 10, 0, 0, 1000)
    assert res["payment"] == round(100000 / 120, 2)

def test_simulator_invalid_inputs():
    with pytest.raises(ValueError, match="Down payment cannot exceed home cost"):
        simulate_mortgage(100000, 120000, 3.5, 20, 30000, 5.0, 1000)
    
    with pytest.raises(ValueError, match="Years and payments_per_year must be positive"):
        simulate_mortgage(100000, 20000, 3.5, 0, 30000, 5.0, 1000)

def test_simulator_comparison():
    # Common parameters
    home_cost = 500000
    annual_rate = 3.0
    years = 20
    savings = 600000
    investment_rate = 4.0
    monthly_cash = 3000
    
    # Scenario A: Low down payment
    res_a = simulate_mortgage(home_cost, 100000, annual_rate, years, savings, investment_rate, monthly_cash)
    
    # Scenario B: High down payment
    res_b = simulate_mortgage(home_cost, 400000, annual_rate, years, savings, investment_rate, monthly_cash)
    
    assert res_a["payment"] > res_b["payment"]
    assert res_a["schedule"][-1]["combined_wealth"] != res_b["schedule"][-1]["combined_wealth"]

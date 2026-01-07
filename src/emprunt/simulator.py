"""Mortgage simulator utilities (simple initial implementation).

This is intentionally simple for the scaffold. We'll expand later.
"""
from typing import Dict, List
import pandas as pd
import numpy as np


def simulate_mortgage(
    home_cost: float,
    down_payment: float,
    annual_rate: float,
    years: int,
    savings: float,
    investment_rate: float,
    monthly_cash: float,
    home_appreciation_rate: float = 0.0,
    payments_per_year: int = 12
) -> Dict:
    """Return an amortization schedule and investment summary.

    Returns:
        dict with keys: monthly_payment, schedule (list of rows), ...
    """
    principal = home_cost - down_payment
    if principal < 0:
        raise ValueError("Down payment cannot exceed home cost")
    if years <= 0 or payments_per_year <= 0:
        raise ValueError("Years and payments_per_year must be positive")

    r = annual_rate / 100.0 / payments_per_year
    n = years * payments_per_year
    inv_r = investment_rate / 100.0 / payments_per_year
    app_r = home_appreciation_rate / 100.0 / payments_per_year

    if r == 0:
        payment = principal / n
    else:
        payment = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)

    if payment > monthly_cash:
        raise ValueError(f"Monthly payment (€{payment:,.0f}) exceeds disposable monthly cash (€{monthly_cash:,.0f})")
    
    if savings < down_payment:
        raise ValueError(f"Savings (€{savings:,.0f}) cannot be less than down payment (€{down_payment:,.0f})") 

    # Initial state
    investment_portfolio = savings - down_payment
    portfolio_capital = investment_portfolio
    balance = principal
    cumulative_interest = 0.0
    current_home_value = home_cost
    schedule = []

    for period in range(1, n + 1):
        # Home appreciation
        current_home_value *= (1 + app_r)
        appreciation_gain = current_home_value - home_cost

        # Mortgage calculation
        interest = balance * r
        cumulative_interest += interest
        principal_paid = min(balance, payment - interest)
        balance = max(0.0, balance - principal_paid)
        
        # Investment calculation
        investment_return = investment_portfolio * inv_r
        leftover_cash = monthly_cash - payment
        investment_portfolio += investment_return + leftover_cash
        portfolio_capital += leftover_cash
        
        home_equity = current_home_value - balance
        combined_wealth = home_equity + investment_portfolio
        
        # Breakdown
        # Wealth = (Initial Cost + Appreciation - Balance) + (Portfolio Capital + Portfolio Gains)
        # Wealth = (Initial Cost - Balance) + Appreciation + Portfolio Capital + Portfolio Gains
        # But we want "Invested Cash" as a component.
        # Total Cash Injected = savings + monthly_cash * period
        total_cash_injected = savings + monthly_cash * period
        
        investment_gains = investment_portfolio - portfolio_capital
        
        # Combined Wealth = (Total Cash Injected - Cumulative Interest) + Investment Gains + Appreciation Gain
        # Let's verify:
        # Equity = Initial Cost - Balance + Appreciation
        # Portfolio = Portfolio Capital + Investment Gains
        # Equity + Portfolio = (Initial Cost - Balance) + Appreciation + Portfolio Capital + Investment Gains
        # We know: Initial Cost - Balance = Cumulative Principal Paid
        # Total Cash Injected = Down Payment + Portfolio Capital(initial) + period * monthly_cash
        # period * monthly_cash = period * (payment + leftover_cash)
        # period * monthly_cash = Cumulative Interest + Cumulative Principal Paid + Cumulative Leftover Cash
        # So Total Cash Injected = Down Payment + Portfolio Capital(initial) + Cumulative Interest + Cumulative Principal Paid + Cumulative Leftover Cash
        # Portfolio Capital = Portfolio Capital(initial) + Cumulative Leftover Cash
        # Total Cash Injected = Down Payment + Cumulative Interest + Cumulative Principal Paid + Portfolio Capital
        # So: (Total Cash Injected - Cumulative Interest) = Down Payment + Cumulative Principal Paid + Portfolio Capital
        # Which is exactly: (Initial Cost - Balance) + Portfolio Capital
        
        schedule.append({
            "period": period,
            "payment": round(payment, 2),
            "principal_paid": round(principal_paid, 2),
            "interest_paid": round(interest, 2),
            "cumulative_interest": round(cumulative_interest, 2),
            "balance": round(balance, 2),
            "current_home_value": round(current_home_value, 2),
            "home_equity": round(home_equity, 2),
            "home_appreciation": round(appreciation_gain, 2),
            "investment_portfolio": round(investment_portfolio, 2),
            "investment_gains": round(investment_gains, 2),
            "portfolio_capital": round(portfolio_capital, 2),
            "total_cash_injected": round(total_cash_injected, 2),
            "invested_cash_net": round(total_cash_injected - cumulative_interest, 2),
            "combined_wealth": round(combined_wealth, 2),
        })

    df = pd.DataFrame(schedule)

    return {
        "home_cost": float(home_cost),
        "down_payment": float(down_payment),
        "principal": float(principal),
        "annual_rate": float(annual_rate),
        "years": int(years),
        "savings": float(savings),
        "investment_rate": float(investment_rate),
        "monthly_cash": float(monthly_cash),
        "home_appreciation_rate": float(home_appreciation_rate),
        "payment": round(float(payment), 2),
        "total_interest": round(float(cumulative_interest), 2),
        "schedule": df.to_dict(orient="records"),
    }

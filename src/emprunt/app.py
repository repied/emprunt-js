import os
from pathlib import Path
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from .simulator import simulate_mortgage

app = FastAPI(title="Emprunt Mortgage Simulator")

# Determine the base directory for the package
BASE_DIR = Path(__file__).resolve().parent

# Mount static and templates directories using absolute paths relative to this file
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


class SimRequest(BaseModel):
    home_cost: float
    down_payment: float
    annual_rate: float
    years: int
    savings: float
    investment_rate: float
    monthly_cash: float
    home_appreciation_rate: float = 0.0
    payments_per_year: int = 12


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {
        "result1": None,
        "result2": None,
        "error": None
    })


@app.post("/simulate", response_class=HTMLResponse)
async def simulate(
    request: Request,
    # Common Parameters
    home_cost: str = Form(...),
    annual_rate: float = Form(...),
    years: int = Form(...),
    savings: str = Form(...),
    investment_rate: float = Form(...),
    monthly_cash: str = Form(...),
    home_appreciation_rate: float = Form(0.0),
    # Scenario Specific
    s1_down_payment: str = Form(...),
    s2_down_payment: str = Form(...),
):
    def clean_money(val: str) -> float:
        if not val:
            return 0.0
        import re
        # Keep only digits and decimal separator
        cleaned = re.sub(r'[^\d.]', '', val)
        try:
            return float(cleaned)
        except ValueError:
            return 0.0

    try:
        c_home_cost = clean_money(home_cost)
        c_savings = clean_money(savings)
        c_monthly_cash = clean_money(monthly_cash)

        # Run Scenario 1
        res1 = simulate_mortgage(
            c_home_cost,
            clean_money(s1_down_payment),
            annual_rate,
            years,
            c_savings,
            investment_rate,
            c_monthly_cash,
            home_appreciation_rate
        )

        # Run Scenario 2
        res2 = simulate_mortgage(
            c_home_cost,
            clean_money(s2_down_payment),
            annual_rate,
            years,
            c_savings,
            investment_rate,
            c_monthly_cash,
            home_appreciation_rate
        )

        return templates.TemplateResponse(request, "index.html", {
            "result1": res1,
            "result2": res2,
            "error": None
        })
    except Exception as e:
        # Create a dummy result object to preserve form values
        dummy1 = {
            "home_cost": c_home_cost if 'c_home_cost' in locals() else 0,
            "savings": c_savings if 'c_savings' in locals() else 0,
            "annual_rate": annual_rate,
            "years": years,
            "investment_rate": investment_rate,
            "monthly_cash": c_monthly_cash if 'c_monthly_cash' in locals() else 0,
            "home_appreciation_rate": home_appreciation_rate,
            "down_payment": clean_money(s1_down_payment)
        }
        dummy2 = {
            "down_payment": clean_money(s2_down_payment)
        }
        return templates.TemplateResponse(request, "index.html", {
            "result1": dummy1,
            "result2": dummy2,
            "error": str(e)
        })


@app.post("/api/simulate")
def api_simulate(req: SimRequest):
    result = simulate_mortgage(
        req.home_cost,
        req.down_payment,
        req.annual_rate,
        req.years,
        req.savings,
        req.investment_rate,
        req.monthly_cash,
        req.home_appreciation_rate,
        req.payments_per_year
    )
    return JSONResponse(content=result)

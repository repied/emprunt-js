function simulateMortgage(homeCost, downPayment, annualRate, years, savings, investmentRate, monthlyCash, homeAppreciationRate, paymentsPerYear = 12) {
    const principal = homeCost - downPayment;
    if (principal < 0) {
        throw new Error("Down payment cannot exceed home cost");
    }
    if (years <= 0 || paymentsPerYear <= 0) {
        throw new Error("Years and payments_per_year must be positive");
    }

    const r = annualRate / 100.0 / paymentsPerYear;
    const n = years * paymentsPerYear;
    const invR = investmentRate / 100.0 / paymentsPerYear;
    const appR = homeAppreciationRate / 100.0 / paymentsPerYear;

    let payment;
    if (r === 0) {
        payment = principal / n;
    } else {
        payment = principal * r * Math.pow(1 + r, n) / (Math.pow(1 + r, n) - 1);
    }

    if (payment > monthlyCash) {
        throw new Error(`Monthly payment (€${payment.toLocaleString(undefined, { maximumFractionDigits: 0 })}) exceeds monthly cash (€${monthlyCash.toLocaleString(undefined, { maximumFractionDigits: 0 })})`);
    }

    if (savings < downPayment) {
        throw new Error(`Savings (€${savings.toLocaleString(undefined, { maximumFractionDigits: 0 })}) cannot be less than down payment (€${downPayment.toLocaleString(undefined, { maximumFractionDigits: 0 })})`);
    }

    let investmentPortfolio = savings - downPayment;
    let portfolioCapital = investmentPortfolio;
    let balance = principal;
    let cumulativeInterest = 0.0;
    let currentHomeValue = homeCost;
    const schedule = [];

    for (let period = 1; period <= n; period++) {
        currentHomeValue *= (1 + appR);
        const appreciationGain = currentHomeValue - homeCost;

        const interest = balance * r;
        cumulativeInterest += interest;
        const principalPaid = Math.min(balance, payment - interest);
        balance = Math.max(0.0, balance - principalPaid);

        const investmentReturn = investmentPortfolio * invR;
        const leftoverCash = monthlyCash - payment;
        investmentPortfolio += investmentReturn + leftoverCash;
        portfolioCapital += leftoverCash;

        const homeEquity = currentHomeValue - balance;
        const combinedWealth = homeEquity + investmentPortfolio;

        const totalCashInjected = savings + monthlyCash * period;
        const investmentGains = investmentPortfolio - portfolioCapital;

        schedule.push({
            period: period,
            payment: parseFloat(payment.toFixed(2)),
            principal_paid: parseFloat(principalPaid.toFixed(2)),
            interest_paid: parseFloat(interest.toFixed(2)),
            cumulative_interest: parseFloat(cumulativeInterest.toFixed(2)),
            balance: parseFloat(balance.toFixed(2)),
            current_home_value: parseFloat(currentHomeValue.toFixed(2)),
            home_equity: parseFloat(homeEquity.toFixed(2)),
            home_appreciation: parseFloat(appreciationGain.toFixed(2)),
            investment_portfolio: parseFloat(investmentPortfolio.toFixed(2)),
            investment_gains: parseFloat(investmentGains.toFixed(2)),
            portfolio_capital: parseFloat(portfolioCapital.toFixed(2)),
            total_cash_injected: parseFloat(totalCashInjected.toFixed(2)),
            invested_cash_net: parseFloat((totalCashInjected - cumulativeInterest).toFixed(2)),
            combined_wealth: parseFloat(combinedWealth.toFixed(2)),
        });
    }

    return {
        home_cost: homeCost,
        down_payment: downPayment,
        principal: principal,
        annual_rate: annualRate,
        years: years,
        savings: savings,
        investment_rate: investmentRate,
        monthly_cash: monthlyCash,
        home_appreciation_rate: homeAppreciationRate,
        payment: parseFloat(payment.toFixed(2)),
        total_interest: parseFloat(cumulativeInterest.toFixed(2)),
        schedule: schedule,
    };
}

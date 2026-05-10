from loguru import logger
from app.schemas.analyze import StockAnalysis
from app.workflows.steps.fetch_financials import fetch_financials
from app.workflows.steps.analyze_fundamentals import analyze_fundamentals
from app.workflows.steps.identify_risks import identify_risks
from app.workflows.steps.generate_recommendation import generate_recommendation


def run_stock_workflow(ticker: str, analysis_type: str, risk_tolerance: str) -> StockAnalysis:
    """
    Orchestrates the full 4-step stock analysis workflow:
    1. Fetch real financial data
    2. Analyze fundamentals with Claude
    3. Identify risks and technical signals with Claude
    4. Generate final recommendation with Claude
    """
    logger.info(f"Starting stock workflow for: {ticker}")

    # Step 1 — real data, no Claude yet
    financial_data = fetch_financials(ticker)

    # Step 2 — Claude analyzes fundamentals
    step2 = analyze_fundamentals(financial_data, risk_tolerance)
    company_summary = step2["company_summary"]
    financial_health = step2["financial_health"]

    # Step 3 — Claude identifies risks
    step3 = identify_risks(financial_data, company_summary, risk_tolerance)
    technical_signals = step3["technical_signals"]
    risk_factors = step3["risk_factors"]

    # Step 4 — Claude generates recommendation
    step4 = generate_recommendation(
        financial_data,
        company_summary,
        financial_health,
        technical_signals,
        risk_factors,
        analysis_type,
        risk_tolerance,
    )

    plan = StockAnalysis(
        ticker=ticker.upper(),
        company_summary=company_summary,
        financial_health=financial_health,
        technical_signals=technical_signals,
        risk_factors=risk_factors,
        recommendation=step4["recommendation"],
    )

    logger.info(f"Workflow complete for: {ticker}")
    return plan
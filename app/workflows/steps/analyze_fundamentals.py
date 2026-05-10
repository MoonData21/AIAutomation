from loguru import logger
from app.services.llm_service import call_claude


def analyze_fundamentals(financial_data: dict, risk_tolerance: str) -> dict:
    """Step 2: Claude analyzes the financial health of the stock."""
    logger.info(f"[Step 2] Analyzing fundamentals for: {financial_data['ticker']}")

    prompt = f"""Analyze the financial health of this stock based on the data below.

Company: {financial_data['company_name']} ({financial_data['ticker']})
Sector: {financial_data['sector']}
Current Price: {financial_data['current_price']}
PE Ratio: {financial_data['pe_ratio']}
Forward PE: {financial_data['forward_pe']}
EPS: {financial_data['eps']}
Revenue: {financial_data['revenue']}
Profit Margin: {financial_data['profit_margin']}
Debt to Equity: {financial_data['debt_to_equity']}
Return on Equity: {financial_data['return_on_equity']}
52 Week High: {financial_data['52_week_high']}
52 Week Low: {financial_data['52_week_low']}
Investor Risk Tolerance: {risk_tolerance}
Business Summary: {financial_data['business_summary']}

Return ONLY this JSON:
{{
  "company_summary": "2-3 sentence overview of the company and its financial position",
  "financial_health": "2-3 sentence assessment of financial health based on the metrics"
}}"""

    result = call_claude(prompt)
    logger.info(f"[Step 2] Complete — fundamentals analyzed")
    return result
from loguru import logger
from app.services.llm_service import call_claude


def identify_risks(financial_data: dict, company_summary: str, risk_tolerance: str) -> dict:
    """Step 3: Claude identifies risk factors."""
    logger.info(f"[Step 3] Identifying risks for: {financial_data['ticker']}")

    prompt = f"""Identify the key risk factors for investing in this stock.

Company: {financial_data['company_name']} ({financial_data['ticker']})
Sector: {financial_data['sector']}
PE Ratio: {financial_data['pe_ratio']}
Debt to Equity: {financial_data['debt_to_equity']}
52 Week High: {financial_data['52_week_high']}
52 Week Low: {financial_data['52_week_low']}
Recent 5-day Prices: {financial_data['recent_prices_5d']}
Analyst Target Price: {financial_data['analyst_target_price']}
Company Summary: {company_summary}
Investor Risk Tolerance: {risk_tolerance}

Return ONLY this JSON:
{{
  "technical_signals": [
    "Signal 1: description",
    "Signal 2: description",
    "Signal 3: description"
  ],
  "risk_factors": [
    "Risk 1: description",
    "Risk 2: description",
    "Risk 3: description"
  ]
}}"""

    result = call_claude(prompt)
    logger.info(f"[Step 3] Complete — {len(result.get('risk_factors', []))} risks identified")
    return result
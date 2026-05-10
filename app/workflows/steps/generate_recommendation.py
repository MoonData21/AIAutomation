from loguru import logger
from app.services.llm_service import call_claude


def generate_recommendation(
    financial_data: dict,
    company_summary: str,
    financial_health: str,
    technical_signals: list[str],
    risk_factors: list[str],
    analysis_type: str,
    risk_tolerance: str,
) -> dict:
    """Step 4: Claude synthesizes everything into a final recommendation."""
    logger.info(f"[Step 4] Generating recommendation for: {financial_data['ticker']}")

    prompt = f"""Based on the full analysis below, generate a final investment recommendation.

Company: {financial_data['company_name']} ({financial_data['ticker']})
Current Price: {financial_data['current_price']}
Analyst Target: {financial_data['analyst_target_price']}
Analyst Consensus: {financial_data['recommendation']}
Analysis Type: {analysis_type}
Risk Tolerance: {risk_tolerance}

Summary: {company_summary}
Financial Health: {financial_health}
Technical Signals: {technical_signals}
Risk Factors: {risk_factors}

Return ONLY this JSON:
{{
  "recommendation": "A clear 3-4 sentence investment recommendation that considers the analysis type ({analysis_type}) and risk tolerance ({risk_tolerance}). Be specific about what the data suggests."
}}"""

    result = call_claude(prompt)
    logger.info(f"[Step 4] Complete — recommendation generated")
    return result
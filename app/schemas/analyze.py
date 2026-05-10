from pydantic import BaseModel
from typing import Optional


class StockRequest(BaseModel):
    ticker: str
    analysis_type: str = "general"  # general, short_term, long_term
    risk_tolerance: str = "moderate"  # low, moderate, high


class StockAnalysis(BaseModel):
    ticker: str
    company_summary: str
    financial_health: str
    technical_signals: list[str]
    risk_factors: list[str]
    recommendation: str
    disclaimer: str = "This is AI-generated analysis for educational purposes only. Not financial advice."


class AnalyzeResponse(BaseModel):
    id: str
    status: str
    message: str
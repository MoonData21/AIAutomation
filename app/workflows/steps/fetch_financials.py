from loguru import logger
from app.services.financial_service import fetch_stock_data


def fetch_financials(ticker: str) -> dict:
    """Step 1: Fetch real financial data from Yahoo Finance."""
    logger.info(f"[Step 1] Fetching financials for: {ticker}")
    data = fetch_stock_data(ticker)
    logger.info(f"[Step 1] Complete — data fetched for {data['company_name']}")
    return data
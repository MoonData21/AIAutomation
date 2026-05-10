import yfinance as yf
from loguru import logger


def fetch_stock_data(ticker: str) -> dict:
    """Fetch real financial data from Yahoo Finance."""
    logger.info(f"Fetching financial data for: {ticker}")

    stock = yf.Ticker(ticker)
    info = stock.info

    # Grab last 5 days of price history
    history = stock.history(period="5d")
    recent_prices = history["Close"].tolist()
    recent_prices = [round(p, 2) for p in recent_prices]

    data = {
        "ticker": ticker.upper(),
        "company_name": info.get("longName", ticker),
        "sector": info.get("sector", "Unknown"),
        "industry": info.get("industry", "Unknown"),
        "current_price": info.get("currentPrice") or info.get("regularMarketPrice"),
        "previous_close": info.get("previousClose"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "eps": info.get("trailingEps"),
        "revenue": info.get("totalRevenue"),
        "profit_margin": info.get("profitMargins"),
        "debt_to_equity": info.get("debtToEquity"),
        "return_on_equity": info.get("returnOnEquity"),
        "52_week_high": info.get("fiftyTwoWeekHigh"),
        "52_week_low": info.get("fiftyTwoWeekLow"),
        "analyst_target_price": info.get("targetMeanPrice"),
        "recommendation": info.get("recommendationKey"),
        "recent_prices_5d": recent_prices,
        "business_summary": info.get("longBusinessSummary", "")[:500],
    }

    logger.info(f"Financial data fetched for {ticker}: {data['company_name']}")
    return data
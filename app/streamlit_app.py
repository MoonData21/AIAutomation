import streamlit as st
import requests
import yfinance as yf
import time
import pandas as pd
import plotly.graph_objects as go
 
# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Stock Analyst",
    page_icon="📈",
    layout="wide",
)
 
# ── Styling ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;600&display=swap');
 
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0f;
    color: #e8e8f0;
}
 
.stApp { background-color: #0a0a0f; }
 
h1, h2, h3 { font-family: 'DM Mono', monospace; }
 
.metric-card {
    background: #12121a;
    border: 1px solid #1e1e2e;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
 
.metric-label {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #555570;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 4px;
}
 
.metric-value {
    font-family: 'DM Mono', monospace;
    font-size: 22px;
    font-weight: 500;
    color: #e8e8f0;
}
 
.tag {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    padding: 4px 10px;
    border-radius: 4px;
    margin: 3px;
    border: 1px solid;
}
 
.tag-green  { background: #0d2b1a; border-color: #1a5c38; color: #4ade80; }
.tag-red    { background: #2b0d0d; border-color: #5c1a1a; color: #f87171; }
.tag-yellow { background: #2b240d; border-color: #5c4a1a; color: #fbbf24; }
.tag-blue   { background: #0d1a2b; border-color: #1a3a5c; color: #60a5fa; }
 
.section-header {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #555570;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    border-bottom: 1px solid #1e1e2e;
    padding-bottom: 8px;
    margin: 24px 0 12px 0;
}
 
.recommendation-box {
    background: #0d1f0d;
    border: 1px solid #1a4a1a;
    border-left: 3px solid #4ade80;
    border-radius: 8px;
    padding: 20px;
    font-size: 15px;
    line-height: 1.7;
    color: #c8f0c8;
}
 
.disclaimer {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #333350;
    text-align: center;
    margin-top: 40px;
    padding: 12px;
    border-top: 1px solid #1e1e2e;
}
 
.stTextInput > div > div > input,
.stSelectbox > div > div {
    background-color: #12121a !important;
    border-color: #1e1e2e !important;
    color: #e8e8f0 !important;
    font-family: 'DM Mono', monospace !important;
}
 
div[data-testid="stButton"] button {
    background: #1a3a5c;
    color: #60a5fa;
    border: 1px solid #1a3a5c;
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    letter-spacing: 0.05em;
    padding: 10px 32px;
    border-radius: 6px;
    width: 100%;
    transition: all 0.2s;
}
 
div[data-testid="stButton"] button:hover {
    background: #60a5fa;
    color: #0a0a0f;
    border-color: #60a5fa;
}
</style>
""", unsafe_allow_html=True)
 
API_BASE = "https://soothing-liberation.railway.app"
 
# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("# 📈 AI Stock Analyst")
st.markdown("<p style='color:#555570; font-family: DM Mono, monospace; font-size:13px;'>Powered by Claude + Yahoo Finance</p>", unsafe_allow_html=True)
st.markdown("---")
 
# ── Sidebar inputs ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Analysis Settings")
 
    ticker = st.text_input(
        "Stock Ticker",
        value="AAPL",
        placeholder="e.g. AAPL, TSLA, MSFT",
    ).upper().strip()
 
    analysis_type = st.selectbox(
        "Analysis Type",
        options=["general", "short_term", "long_term"],
        index=0,
    )
 
    risk_tolerance = st.selectbox(
        "Risk Tolerance",
        options=["low", "moderate", "high"],
        index=1,
    )
 
    run_button = st.button("Run Analysis")
 
    st.markdown("---")
    st.markdown("<p style='font-family: DM Mono, monospace; font-size: 11px; color: #333350;'>Make sure your FastAPI server is running at localhost:8000</p>", unsafe_allow_html=True)
 
 
# ── Helper: price chart ────────────────────────────────────────────────────────
def render_price_chart(ticker: str):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="3mo")
 
    if hist.empty:
        st.warning("Could not load price history.")
        return
 
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hist.index,
        y=hist["Close"],
        mode="lines",
        line=dict(color="#60a5fa", width=2),
        fill="tozeroy",
        fillcolor="rgba(96, 165, 250, 0.05)",
        name="Close Price",
    ))
    fig.update_layout(
        paper_bgcolor="#0a0a0f",
        plot_bgcolor="#0a0a0f",
        font=dict(family="DM Mono", color="#555570", size=11),
        xaxis=dict(gridcolor="#1e1e2e", showgrid=True),
        yaxis=dict(gridcolor="#1e1e2e", showgrid=True),
        margin=dict(l=0, r=0, t=8, b=0),
        height=220,
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)
 
 
# ── Helper: recommendation color ───────────────────────────────────────────────
def rec_color(rec: str) -> str:
    rec = rec.lower()
    if any(w in rec for w in ["buy", "strong buy", "bullish"]):
        return "tag-green"
    if any(w in rec for w in ["sell", "bearish", "avoid"]):
        return "tag-red"
    return "tag-yellow"
 
 
# ── Main logic ─────────────────────────────────────────────────────────────────
if run_button and ticker:
    # 1. Submit to API
    with st.spinner(f"Submitting analysis for **{ticker}**..."):
        try:
            resp = requests.post(f"{API_BASE}/analyze", json={
                "ticker": ticker,
                "analysis_type": analysis_type,
                "risk_tolerance": risk_tolerance,
            })
            resp.raise_for_status()
            job = resp.json()
            run_id = job["id"]
        except Exception as e:
            st.error(f"Could not reach the API. Is `uvicorn app.main:app --reload` running?\n\n{e}")
            st.stop()
 
    # 2. Poll for results
    status_placeholder = st.empty()
    result = None
 
    for attempt in range(30):
        time.sleep(2)
        try:
            poll = requests.get(f"{API_BASE}/results/{run_id}")
            data = poll.json()
            status = data.get("status")
 
            status_placeholder.markdown(
                f"<p style='font-family: DM Mono, monospace; font-size: 12px; color: #555570;'>"
                f"Status: <span style='color:#60a5fa'>{status}</span> — checking in {2*(attempt+1)}s...</p>",
                unsafe_allow_html=True,
            )
 
            if status == "complete":
                result = data.get("result")
                status_placeholder.empty()
                break
            elif status == "failed":
                status_placeholder.empty()
                st.error(f"Workflow failed: {data.get('error')}")
                st.stop()
        except Exception as e:
            st.error(f"Polling error: {e}")
            st.stop()
 
    if not result:
        st.error("Timed out waiting for results. Try again.")
        st.stop()
 
    # ── Render results ──────────────────────────────────────────────────────────
    st.markdown(f"## {result['ticker']}")
 
    # Price chart
    render_price_chart(ticker)
 
    # Quick metrics row
    stock_info = yf.Ticker(ticker).info
    col1, col2, col3, col4 = st.columns(4)
 
    with col1:
        price = stock_info.get("currentPrice") or stock_info.get("regularMarketPrice", "N/A")
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Current Price</div>
            <div class='metric-value'>${price}</div>
        </div>""", unsafe_allow_html=True)
 
    with col2:
        pe = stock_info.get("trailingPE", "N/A")
        pe_display = f"{pe:.1f}" if isinstance(pe, float) else pe
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>P/E Ratio</div>
            <div class='metric-value'>{pe_display}</div>
        </div>""", unsafe_allow_html=True)
 
    with col3:
        high = stock_info.get("fiftyTwoWeekHigh", "N/A")
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>52W High</div>
            <div class='metric-value'>${high}</div>
        </div>""", unsafe_allow_html=True)
 
    with col4:
        low = stock_info.get("fiftyTwoWeekLow", "N/A")
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>52W Low</div>
            <div class='metric-value'>${low}</div>
        </div>""", unsafe_allow_html=True)
 
    # Company summary
    st.markdown("<div class='section-header'>Company Summary</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#a0a0b8; line-height:1.7'>{result['company_summary']}</p>", unsafe_allow_html=True)
 
    # Financial health
    st.markdown("<div class='section-header'>Financial Health</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#a0a0b8; line-height:1.7'>{result['financial_health']}</p>", unsafe_allow_html=True)
 
    # Two columns: signals + risks
    col_left, col_right = st.columns(2)
 
    with col_left:
        st.markdown("<div class='section-header'>Technical Signals</div>", unsafe_allow_html=True)
        for signal in result["technical_signals"]:
            st.markdown(f"<span class='tag tag-blue'>↗ {signal}</span>", unsafe_allow_html=True)
 
    with col_right:
        st.markdown("<div class='section-header'>Risk Factors</div>", unsafe_allow_html=True)
        for risk in result["risk_factors"]:
            st.markdown(f"<span class='tag tag-red'>⚠ {risk}</span>", unsafe_allow_html=True)
 
    # Recommendation
    st.markdown("<div class='section-header'>AI Recommendation</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='recommendation-box'>
        {result['recommendation']}
    </div>""", unsafe_allow_html=True)
 
    # Disclaimer
    st.markdown(f"<div class='disclaimer'>{result['disclaimer']}</div>", unsafe_allow_html=True)
 
elif not run_button:
    # Empty state
    st.markdown("""
    <div style='text-align:center; padding: 80px 0; color: #333350;'>
        <p style='font-family: DM Mono, monospace; font-size: 13px;'>
            Enter a ticker and click Run Analysis to get started.
        </p>
    </div>
    """, unsafe_allow_html=True)

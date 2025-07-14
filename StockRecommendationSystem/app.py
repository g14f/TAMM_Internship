import yfinance as yf
import pandas as pd
import streamlit as st
import os
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.runnables.retry import RunnableRetry
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

google_api_key = st.secrets['GOOGLE_API_KEY']
finhub_api_key = st.secrets['FINNHUB_API_KEY']

os.environ["GOOGLE_API_KEY"] = google_api_key
FINNHUB_API_KEY = finhub_api_key



class Stock(BaseModel):
    ticker: str
    company_name: str
    sector: Optional[str] = None
    market_cap: Optional[float] = Field(None, description="Market capitalization in USD")
    avg_entry_price: Optional[float] = Field(None, description="Average entry price")
    bid: Optional[float] = Field(None,description="Bid Price")
    ask: Optional[float] = Field(None,description="Ask Price")
    pe_ratio: Optional[float] = Field(None, description="Trailing P/E ratio")
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
    recent_close_prices: List[float] = Field(..., description="Recent closing prices")
    recent_news: Optional[List[str]] = Field(None, description="Recent news headlines")
    financial_summary: Optional[Dict[str, float]] = Field(None, description="Summary of financials (revenue, net income, etc.)")
    analyst_recommendations: Optional[List[str]] = Field(None, description="Recent analyst recommendations")

class Response(BaseModel):
    company_name: str
    ticker: str
    news_analysis: str
    financial_analysis: str
    bid: float
    ask: float
    average_entry_price: float
    recommendation: str
    justification: str

class MultiCompanyResponse(BaseModel):
    results: List[Response]


def get_stock_data(ticker_symbol: str) -> Stock:
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    company_name = info.get('longName') or info.get('shortName') or ticker_symbol
    sector = info.get('sector')
    market_cap = info.get('marketCap')
    pe_ratio = info.get('trailingPE')
    fifty_two_week_high = info.get('fiftyTwoWeekHigh')
    fifty_two_week_low = info.get('fiftyTwoWeekLow')
    avg_entry_price = float([position.avg_entry_price for position in st.session_state.portfolio if position.symbol == ticker_symbol][0])
    price_hist = ticker.history(period="15d", interval="1d")
    recent_close_prices = price_hist['Close'].dropna().tolist()[-10:] if not price_hist.empty else []
    url = f'https://finnhub.io/api/v1/company-news?symbol={ticker_symbol}&from=2024-06-01&to=2025-06-29&token={FINNHUB_API_KEY}'
    resp = requests.get(url)
    recent_news = None
    if resp.status_code == 200:
        news = resp.json()
        recent_news = [item['headline'] for item in news[:5] if 'headline' in item]
    financial_summary = None
    if hasattr(ticker, "financials") and not ticker.financials.empty:
        fs = ticker.financials
        financial_summary = {
            "total_revenue": float(fs.loc['Total Revenue'].iloc[0]) if 'Total Revenue' in fs.index else None,
            "net_income": float(fs.loc['Net Income'].iloc[0]) if 'Net Income' in fs.index else None
        }
    analyst_recs = None
    try:
        recs_df = ticker.recommendations
        if recs_df is not None and not recs_df.empty:
            analyst_recs = recs_df['To Grade'].dropna().tail(5).tolist()
    except Exception:
        analyst_recs = None
    bid = info.get('bid')
    ask = info.get('ask')
    return Stock(
        ticker=ticker_symbol,
        company_name=company_name,
        sector=sector,
        market_cap=market_cap,
        avg_entry_price=avg_entry_price,
        pe_ratio=pe_ratio,
        fifty_two_week_high=fifty_two_week_high,
        fifty_two_week_low=fifty_two_week_low,
        recent_close_prices=recent_close_prices,
        recent_news=recent_news,
        financial_summary=financial_summary,
        analyst_recommendations=analyst_recs,
        bid=bid,
        ask=ask
    )
def check_keys():
    if st.session_state.api_key and st.session_state.secret_key:
        st.session_state.keys_entered = True
        st.session_state.fetching_portfolio = True  # Start first step
        st.session_state.failed = False
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "secret_key" not in st.session_state:
    st.session_state.secret_key = ""
if "portfolio" not in st.session_state:
    st.session_state.portfolio = []
if "stocks" not in st.session_state:
    st.session_state.stocks = []
if "result" not in st.session_state:
    st.session_state.result = None
if "all_stocks_data" not in st.session_state:
    st.session_state.all_stocks_data = ""
if "keys_entered" not in st.session_state:
    st.session_state.keys_entered = False
if "fetching_portfolio" not in st.session_state:
    st.session_state.fetching_portfolio = False
if "gathering_data" not in st.session_state:
    st.session_state.gathering_data = False
if "analyzing_data" not in st.session_state:
    st.session_state.analyzing_data = False
if "results_ready" not in st.session_state:
    st.session_state.results_ready = False
if "failed" not in st.session_state:
    st.session_state.failed = False
st.title("Portfolio Stock Analysis and Recommendation")
if st.session_state.failed:
  st.error("Invalid API Key or Secret Key. Please try again.")
  st.session_state.keys_entered = False
  st.session_state.failed = False
elif not st.session_state.keys_entered:
    st.text_input("Enter your API Key", key="api_key", on_change=check_keys)
    st.text_input("Enter your Secret Key", key="secret_key", type="password", on_change=check_keys)
elif st.session_state.fetching_portfolio:
    st.info("Fetching your portfolio...")
    try:
        trading_client = TradingClient(st.session_state.api_key, st.session_state.secret_key, paper=True)
        alpaca_url = "https://paper-api.alpaca.markets/v2/account"
        headers = {
            "accept": "application/json",
            "APCA-API-KEY-ID": st.session_state.api_key,
            "APCA-API-SECRET-KEY": st.session_state.secret_key
        }
        response = requests.get(alpaca_url, headers=headers)
        if response.status_code != 200:
            raise Exception("Invalid API credentials")
        st.session_state.portfolio = trading_client.get_all_positions()
        st.session_state.stocks = list(set([order.symbol for order in st.session_state.portfolio]))
        st.session_state.fetching_portfolio = False
        st.session_state.gathering_data = True
        st.rerun()
    except Exception as e:
        st.session_state.failed = True
        st.session_state.keys_entered = False
        st.session_state.fetching_portfolio = False
        st.rerun()
elif st.session_state.gathering_data:
    st.info("Gathering data about your stocks...")
    st.session_state.stocks = [get_stock_data(ticker) for ticker in st.session_state.stocks]
    stock_blocks = []
    for stock in st.session_state.stocks:
      block = f"""
      Ticker: {stock.ticker}
      Company Name: {stock.company_name}
      Sector: {stock.sector}
      Market Cap: {stock.market_cap}
      Average Entry Price: {stock.avg_entry_price}
      Bid: {stock.bid}
      Ask: {stock.ask}
      P/E Ratio: {stock.pe_ratio}
      52-Week High: {stock.fifty_two_week_high}
      52-Week Low: {stock.fifty_two_week_low}
      Recent Close Prices: {stock.recent_close_prices}
      Recent News Headlines: {stock.recent_news}
      Financial Summary: {stock.financial_summary}
      Analyst Recommendations: {stock.analyst_recommendations}
      """
      stock_blocks.append(block)
    st.session_state.all_stocks_data = "\n---\n".join(stock_blocks)
    st.session_state.gathering_data = False
    st.session_state.analyzing_data = True
    st.rerun()
elif st.session_state.analyzing_data:
    st.info("Analyzing data...")
    prompt = PromptTemplate.from_template("""
You are a professional financial analyst. Based on the stock portfolio for an investor, analyze the companies and provide a buy/hold/sell recommendation for each company with clear reasons, considering the average entry price and all other relevant factors that may affect the recommendation. Include company names instead of ticker name in your recommendation.

Use only the data provided. Do not make up information not present in the input. If a particular field is missing or empty, briefly mention that in your analysis (e.g., "No recent news was provided."). Use 2nd person point of view instead of 3rd person point of view. For example, instead of saying "the investor's average entry price is low" say "Your average entry price is low". Keep in mind that the investor will read your response

For clarity, structure your answer with these sections:
1. News Analysis
2. Financial Analysis
3. Final Recommendation (buy/hold/sell), with justification
4. bid (Use the same bid price given in the stock data below)
5. ask (Use the same ask price given in the stock data below)
6. average entry price (Use the same average entry price given in the stock data below)
Here is the stock data:

{stocks_data}

Your answer should be factual, concise, detailed, and not more than 250 words. Include many stastics and numbers as much as possible to strengthen your analysis and your recommendation.

{format_instructions}

[Begin your analysis below.]
""")

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.7)

    parser = PydanticOutputParser(pydantic_object=MultiCompanyResponse)

    chain = (prompt | llm | parser).with_retry(stop_after_attempt=3,wait_exponential_jitter=True)
    format_instructions = parser.get_format_instructions()
    try:
      st.session_state.result = chain.invoke({
        "stocks_data":st.session_state.all_stocks_data,
        "format_instructions": format_instructions
      })
    except Exception as e:
      st.write("All retries failed:", e)
    st.session_state.analyzing_data = False
    st.session_state.results_ready = True
    st.rerun()
elif st.session_state.results_ready:
    st.success("Analysis Complete! Here are your results:")
    st.markdown("# News Analysis")
    for company in st.session_state.result.results:
      st.markdown("### "+company.company_name)
      st.write("\t"+company.news_analysis)
    st.markdown("# Financial Analysis")
    for company in st.session_state.result.results:
      st.markdown("### "+company.company_name)
      st.write("\t"+company.financial_analysis)
    st.markdown("# Recommendation")
    for company in st.session_state.result.results:
      st.markdown("### "+company.company_name)
      st.write("\tRecommendation: "+company.recommendation)
      st.write("\tReason: "+company.justification)
    st.markdown("# Conclusion")
    df = pd.DataFrame([r.dict() for r in st.session_state.result.results])
    st.dataframe(df[["company_name", "ticker", "bid", "ask", "average_entry_price", "recommendation"]], use_container_width=True)

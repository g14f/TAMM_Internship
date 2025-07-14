# 🏦 Stock Portfolio AI Recommendation System

**[Live Demo](https://stocks-g14f.streamlit.app/)**

This web app helps investors analyze their stock portfolio and get **personalized, AI-powered buy/hold/sell recommendations**.  
The analysis is powered by **Google Gemini**, and uses live financial data and news from Yahoo Finance and Finnhub.  
You only need a free Alpaca account for paper trading—**no real money required!**

---

## 🚀 Features

- **Connect your Alpaca Paper Trading account** (no risk, no real money needed!)
- **Fetches your current stock portfolio automatically**
- **Gathers financial data and news** for each stock
- **AI-generated, tailored recommendations** for each stock, with justification
- Clear, structured report including:
  - News analysis
  - Financial analysis
  - Bid/ask/entry prices
  - Final recommendation (buy/hold/sell)

---

## 🧐 What is Alpaca?

[**Alpaca**](https://alpaca.markets/) is a commission-free API platform for stock trading and investing.  
For this app, you use a **paper trading account**—meaning you get a virtual portfolio and can trade stocks without spending real money.

- **Paper trading** is a simulation of real trading, perfect for testing strategies risk-free.
- All you need is a free Alpaca account.

---

## 📝 How to Get Your Alpaca API Key & Secret Key

1. **Sign Up or Log In to Alpaca:**  
   Go to [https://alpaca.markets/](https://alpaca.markets/) and create a free account.

2. **Switch to Paper Trading:**  
   After logging in, click your avatar (top right) > **Paper Trading**.

3. **Get Your API Keys:**  
   - Go to the **API Keys** section (found in the left sidebar).
   - Click **Generate New Key** (or use the existing ones).
   - Copy both your **API Key** and **Secret Key**—you’ll use them in the app.

> **Note:**  
> These keys only allow simulated trades and read your virtual portfolio.  
> You never risk real money or touch your real assets.

---

## 📈 How to Use the App

1. **Open the app:**  
   [https://stocks-g14f.streamlit.app/](https://stocks-g14f.streamlit.app/)

2. **Enter your Alpaca API Key and Secret Key**  
   - Your keys are kept private and only used to access your simulated portfolio.

3. **App will fetch your portfolio stocks**  
   - Gathers symbols and your average entry price for each holding.

4. **App collects news and financial data automatically**  
   - From Yahoo Finance and Finnhub APIs.

5. **AI generates analysis and recommendations**
   - Per stock: news & financial analysis, bid/ask/entry price, and buy/hold/sell suggestion with reasoning.

6. **Review your custom report**
   - See recommendations and download results for your review.

---

## 💬 Example Output

- **News Analysis:** Latest headlines and news trends for each company
- **Financial Analysis:** Key financial ratios, price stats, and recent performance
- **Final Recommendation:** Buy/Hold/Sell, with a clear, factual justification
- **Summary Table:** Easy-to-read table with all key numbers and recommendations

---

## 🛡️ Privacy & Security

- Your keys and portfolio are **never stored**; only used in your browser session.
- You can use the app **risk-free** thanks to Alpaca's paper trading.

---

## ❓ FAQ

**Q: Do I need to use real money or have a funded brokerage account?**  
A: No! This app is for Alpaca paper trading—just sign up, get your keys, and simulate investing.

**Q: Where do I get my API Key and Secret Key?**  
A: From your Alpaca dashboard, under "API Keys" in paper trading mode. See the instructions above.

**Q: Is this financial advice?**  
A: No, this is for educational and informational purposes only.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Financial Data:** Yahoo Finance, Finnhub
- **Brokerage API:** Alpaca (Paper Trading)
- **AI Analysis:** Google Gemini via LangChain

---

**Empower your portfolio with AI! 🚀**

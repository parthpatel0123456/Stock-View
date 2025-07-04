import os
import json
import requests
import matplotlib.pyplot as plt
import datetime
import yfinance

from website import create_app
from flask import Flask, send_from_directory, jsonify, request
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

finnhub_api_key = os.getenv("FINNHUB_API_KEY")
marketaux_api_key = os.getenv("MARKETAUX_API_KEY")
alpha_vantage_api_key = os.getenv("ALPHAVTANGE_API_KEY")
polygon_api_key = os.getenv("POLYGON_API_KEY")

STATIC_DIR = os.path.join(os.getcwd(), "react-frontend", "build")
app = Flask(__name__, static_folder = STATIC_DIR, static_url_path='')

@app.route('/')
def home():
    return send_from_directory(STATIC_DIR, "index.html")

@app.route('/<path:path>')
def serve_react(path):
    
    if os.path.exists(os.path.join(STATIC_DIR, path)):
        return send_from_directory(STATIC_DIR, path)
    else:
        return send_from_directory(STATIC_DIR, "index.html")

@app.route('/api/stocks/<symbol>/news')
def get_stock_news(symbol):
    today = datetime.date.today()
    latest_range = today.strftime("%Y-%m-%d")
    earliest_range = (today - datetime.timedelta(days=30)).strftime("%Y-%m-%d")

    news_url = f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from={earliest_range}&to={latest_range}&token={finnhub_api_key}"
    finnhub_news_response = requests.get(news_url)


    news_url = f"https://api.marketaux.com/v1/news/all?symbols={symbol}&filter_entities=true&language=en&api_token={marketaux_api_key}&limit=50&page=1"
    marketaux_news_response = requests.get(news_url)
    marketaux_news_data = marketaux_news_response.json().get("data", [])

    return jsonify({
        "symbol": symbol.upper(),
        "marketauxNews": marketaux_news_data,
        "finnhubNews": finnhub_news_response.json(),
        "lastUpdated": latest_range,
        })

@app.route('/api/stocks/<symbol>/earnings')
def get_stock_earnings(symbol):
    today = datetime.date.today()
    latest_range = today.strftime("%Y-%m-%d")
    earliest_range = (today - datetime.timedelta(days=1000)).strftime("%Y-%m-%d")

    return jsonify({
        "earningsCalender": 0
    })

@app.route('/api/stocks/<symbol>/financials')
def get_stock_financials(symbol):
    financial_url = f"https://api.polygon.io/vX/reference/financials?ticker={symbol}&limit=10&order=desc&sort=filing_date&apiKey={polygon_api_key}"
    financial_response = requests.get(financial_url).json()
    financial_data = financial_response['results']

    def format_money(value):
        if value is None:
            return "N/A"
        return f"${int(value):,}"

    quarters, years = [], []
    assets, liabilities, equities = [], [], []
    revenues, gross_profits, net_incomes, operating_incomes = [], [], [], []
    operating_cash_flows, investing_cash_flows, financing_cash_flows = [], [], []

    for filing in financial_data:
        try:
            quarters.append(filing.get('fiscal_period', 'N/A'))
            years.append(filing.get('fiscal_year', 'N/A'))

            asset_value = (
                filing.get('financials', {}).get('balance_sheet', {}).get('assets', {}).get('value') or 0
            )
            liability_value = (
                filing.get('financials', {}).get('balance_sheet', {}).get('liabilities', {}).get('value') or 0
            )
            equity_value = (
                filing.get('financials', {}).get('balance_sheet', {}).get('equity', {}).get('value') or 0
            )
            assets.append(asset_value)
            liabilities.append(liability_value)
            equities.append(equity_value)

            revenue_value = (
                filing.get('financials', {}).get('income_statement', {}).get('revenues', {}).get('value') or 0
            )
            gross_profit_value = (
                filing.get('financials', {}).get('income_statement', {}).get('gross_profit', {}).get('value') or 0
            )
            operating_income_value = (
                filing.get('financials', {}).get('income_statement', {}).get('operating_income_loss', {}).get('value') or 0
            )
            net_income_value = (
                filing.get('financials', {}).get('income_statement', {}).get('net_income_loss', {}).get('value') or 0
            )
            revenues.append(revenue_value)
            gross_profits.append(gross_profit_value)
            net_incomes.append(net_income_value)
            operating_incomes.append(operating_income_value)

            operating_cash_flow_value = (
                filing.get('financials', {}).get('cash_flow_statement', {}).get('net_cash_flow_from_operating_activities', {}).get('value') or 0
            )
            investing_cash_flow_value = (
                filing.get('financials', {}).get('cash_flow_statement', {}).get('net_cash_flow_from_investing_activities', {}).get('value') or 0
            )
            financing_cash_flow_value = (
                filing.get('financials', {}).get('cash_flow_statement', {}).get('net_cash_flow_from_financing_activities', {}).get('value') or 0
            )
            operating_cash_flows.append(operating_cash_flow_value)
            investing_cash_flows.append(investing_cash_flow_value)
            financing_cash_flows.append(financing_cash_flow_value)

        except Exception:
            pass  # Handles unexpected non-KeyError issues if any
    
    for i, quarter in enumerate(quarters):
        if quarter == 'FY':
            quarters[i] = 'FY (Q4)'

    combined = []
    try:
        for i in range(len(years)):
            combined.append({
                "year": years[i],
                "quarter": quarters[i],
                "assets": assets[i],
                "equity": equities[i],
                "liabilities": liabilities[i],
                "revenue": revenues[i],
                "net_income": net_incomes[i],
                "operating_cash_flow": operating_cash_flows[i],
                "investing_cash_flow": investing_cash_flows[i],
                "financing_cash_flow": financing_cash_flows[i],
                "gross_profit": gross_profits[i],
                "operating_income": operating_incomes[i]
            })
    except IndexError:
        pass

    return jsonify({
        "financial_data": combined
    })

@app.route('/api/stocks/<symbol>/dividends')
def get_stock_dividends(symbol):
    dividends_url = f"https://api.polygon.io/v3/reference/dividends?ticker={symbol}&limit=10&apiKey={polygon_api_key}"
    dividends_res = requests.get(dividends_url).json()
    
    dividends_data = dividends_res['results']

    cash_amount = []
    ex_dividend_date = []
    pay_date = []
    frequency = []
    declaration_date = []

    for entry in dividends_data:
        cash_amount.append(entry.get('cash_amount'))
        ex_dividend_date.append(entry.get('ex_dividend_date'))
        declaration_date.append(entry.get('declartion_date'))
        pay_date.append(entry.get('pay_date'))
        frequency.append(entry.get('frequency'))

    combined = []
    try:
        for i in range(len(dividends_data)):
            combined.append({
                "cash_amount": cash_amount[i],
                "ex_dividend_date": ex_dividend_date[i],
                "declaration_date": declaration_date[i],
                "pay_date": pay_date[i],
                "frequency": frequency[i]
            })
    except IndexError:
        pass

    return jsonify({
        "dividends_data": combined,
        "dividends": dividends_data
    })

base_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol='
base_earnings_url = 'https://www.alphavantage.co/query?function=EARNINGS&symbol='
base_news_url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers='

if __name__ == '__main__':
    symbol = "TSLA"
    app.run(debug=True, port=5001)
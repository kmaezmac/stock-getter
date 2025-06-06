import json
import os
from dotenv import load_dotenv
import yfinance as yf

load_dotenv()

def get_fx_rate():
    return yf.Ticker("USDJPY=X").history(period="1d").Close[0]

def get_stock_prices(symbols, fx_rate):
    results = []
    for symbol in symbols:
        symbol = symbol.strip()
        try:
            ticker = yf.Ticker(symbol)
            dollar_price = ticker.info['currentPrice']
            title = ticker.info['longName']
            yen_price = round(dollar_price * fx_rate, 2)
            results.append({
                "symbol": symbol,
                "title": title,
                "dollar_price": dollar_price,
                "yen_price": yen_price
            })
        except Exception as e:
            results.append({
                "symbol": symbol,
                "error": str(e)
            })
    return results

def handler(request, response):
    try:
        body = request.get_json()
        symbols = body.get("symbols", [])
        fx_rate = get_fx_rate()
        prices = get_stock_prices(symbols, fx_rate)
        response.status_code = 200
        response.headers["Content-Type"] = "application/json"
        response.body = json.dumps({
            "fx_rate": fx_rate,
            "results": prices
        })
    except Exception as e:
        response.status_code = 500
        response.body = json.dumps({"error": str(e)})
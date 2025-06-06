from http.server import BaseHTTPRequestHandler
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

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        try:
            data = json.loads(body)
            symbols = data.get("symbols", [])
            fx_rate = get_fx_rate()
            prices = get_stock_prices(symbols, fx_rate)
            response = {
                "fx_rate": fx_rate,
                "results": prices
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
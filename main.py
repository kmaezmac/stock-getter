import os
from dotenv import load_dotenv
load_dotenv()

import yfinance as yf

fx_rate = yf.Ticker("USDJPY=X").history(period="1d").Close[0]
print(f"USD/JPY: {fx_rate}")
print("\n------------\n")

def print_stock_prices(symbols, fx_rate):
    for symbol in symbols:
        symbol = symbol.strip()
        try:
            dollar_price = yf.Ticker(symbol).info['currentPrice']
            title = yf.Ticker(symbol).info['longName']
            print(f"{symbol}({title}): {dollar_price}ドル = {round(dollar_price * fx_rate, 2)}円")
        except Exception as e:
            print(f"{symbol}: 取得失敗 ({e})")

symbols_us = os.getenv("STOCK_SYMBOLS_US").split(",")

print_stock_prices(symbols_us, fx_rate)

print("\n------------\n")

symbols_jp = os.getenv("STOCK_SYMBOLS_JP").split(",")
print_stock_prices(symbols_jp, fx_rate)
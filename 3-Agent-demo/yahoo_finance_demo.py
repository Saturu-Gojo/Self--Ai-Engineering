import yfinance as yf
import warnings
warnings.filterwarnings("ignore")
import json

def get_stock_price(ticker_symbol:str)->str:
    try:
        stock = yf.Ticker(ticker_symbol.upper())
        price = stock.fast_info.last_price
        currency = stock.fast_info.currency
        return json.dumps({
            "ticker": ticker_symbol.upper(),
            "price": price,
            "currency": currency
        })
    except Exception as e:
        return json.dumps({
            "error": str(e)
        })

if __name__=="__main__":
    get_stock_price("AAPL")
from stock_data import get_historical_stock_data

data = get_historical_stock_data("INFY.NS", "1mo")

if data is not None:
    print(data)
else:
    print("No stock data found")
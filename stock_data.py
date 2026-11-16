import yfinance as yf
import pandas as pd


def get_historical_stock_data(ticker: str, period: str):

    stock = yf.Ticker(ticker)

    data = stock.history(
        period=period,
        interval="1d",
        auto_adjust=False
    )

    if data.empty:
        return None

    data = data.reset_index()

    data = data[
        ["Date", "Open", "High", "Low", "Close", "Volume"]
    ]

    data = data.dropna()

    data["Date"] = data["Date"].dt.strftime("%Y-%m-%d")

    return data
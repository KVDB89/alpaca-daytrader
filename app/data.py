import os
import pandas as pd
from datetime import datetime, timedelta, timezone
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

KEY = os.getenv("ALPACA_KEY_ID")
SECRET = os.getenv("ALPACA_SECRET_KEY")
FEED = os.getenv("DATA_FEED", "iex")

data_client = StockHistoricalDataClient(KEY, SECRET)

def get_minute_bars(symbols, lookback_minutes=100):
    # Pull last ~lookback_minutes for a list of tickers in a single request
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=lookback_minutes + 30)
    req = StockBarsRequest(
        symbol_or_symbols=symbols,
        timeframe=TimeFrame.Minute,
        start=start,
        end=end,
        feed=FEED  # 'iex' for paper accounts
    )
    bars = data_client.get_stock_bars(req)
    df = bars.df  # MultiIndex (symbol, timestamp)
    # keep last lookback_minutes rows per symbol
    if df.empty:
        return {}
    out = {}
    for sym in df.index.get_level_values(0).unique():
        sdf = df.xs(sym).sort_index().tail(lookback_minutes)
        out[sym] = sdf
    return out

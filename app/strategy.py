import pandas as pd

def sma_crossover_signal(df: pd.DataFrame, fast=5, slow=20):
    # df has columns: open, high, low, close, volume
    if df is None or df.empty:
        return "HOLD"
    s = df.copy()
    s["sma_fast"] = s["close"].rolling(fast).mean()
    s["sma_slow"] = s["close"].rolling(slow).mean()
    if len(s) < slow + 1:
        return "HOLD"
    # Check last two bars for a cross
    prev = s.iloc[-2]
    curr = s.iloc[-1]
    crossed_up = prev["sma_fast"] <= prev["sma_slow"] and curr["sma_fast"] > curr["sma_slow"]
    crossed_dn = prev["sma_fast"] >= prev["sma_slow"] and curr["sma_fast"] < curr["sma_slow"]
    if crossed_up:
        return "BUY"
    if crossed_dn:
        return "SELL"
    return "HOLD"

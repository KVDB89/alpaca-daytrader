import os, time, math
from app.data import get_minute_bars
from app.strategy import sma_crossover_signal
from app.broker import submit_market_buy, submit_market_sell, open_positions, buying_power
from app.utils import is_regular_market_hours_now

# Start with a manageable universe to respect rate limits
UNIVERSE = os.getenv("SYMBOLS", "AAPL,MSFT,NVDA,AMZN,GOOGL,META,TSLA").split(",")
DOLLARS_PER_TRADE = float(os.getenv("DOLLARS_PER_TRADE", "500"))
MAX_CONCURRENT = int(os.getenv("MAX_CONCURRENT", "5"))
SLEEP_SECONDS = int(os.getenv("LOOP_SLEEP_SECONDS", "55"))

def run_once():
    if not is_regular_market_hours_now():
        print("Market closed; sleeping…")
        return

    positions = open_positions()
    held = set(positions.keys())

    bars_map = get_minute_bars(UNIVERSE, lookback_minutes=100)
    bp = buying_power()

    # entries
    for sym in UNIVERSE:
        df = bars_map.get(sym)
        sig = sma_crossover_signal(df)
        if sig == "BUY" and len(held) < MAX_CONCURRENT and DOLLARS_PER_TRADE < bp:
            print(f"[{sym}] BUY signal")
            submit_market_buy(sym, DOLLARS_PER_TRADE)
            held.add(sym)

    # exits
    # (We recompute signals using the same bars; if SELL and we hold -> exit)
    for sym in list(held):
        df = bars_map.get(sym)
        if sma_crossover_signal(df) == "SELL":
            print(f"[{sym}] SELL signal")
            # Market sell full position (qty resolved in broker.close_position if you want)
            # Here we simplify by sending a 'close' request:
            from app.broker import close_position
            close_position(sym)
            held.remove(sym)

if __name__ == "__main__":
    while True:
        try:
            run_once()
        except Exception as e:
            print("Error:", e)
        time.sleep(SLEEP_SECONDS)

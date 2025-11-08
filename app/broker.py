import os
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

KEY = os.getenv("ALPACA_KEY_ID")
SECRET = os.getenv("ALPACA_SECRET_KEY")
PAPER = True

trading = TradingClient(KEY, SECRET, paper=PAPER)

def buying_power():
    return float(trading.get_account().buying_power)

def submit_market_buy(symbol: str, notional_usd: float):
    order = MarketOrderRequest(
        symbol=symbol, side=OrderSide.BUY, notional=notional_usd,
        time_in_force=TimeInForce.DAY
    )
    return trading.submit_order(order)

def submit_market_sell(symbol: str, qty: float):
    order = MarketOrderRequest(
        symbol=symbol, side=OrderSide.SELL, qty=qty,
        time_in_force=TimeInForce.DAY
    )
    return trading.submit_order(order)

def open_positions():
    # returns dict symbol -> qty
    return {p.symbol: float(p.qty) for p in trading.get_all_positions()}

def close_position(symbol: str):
    try:
        trading.close_position(symbol)
    except Exception:
        pass

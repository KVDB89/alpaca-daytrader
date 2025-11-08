from datetime import datetime
import pytz

NY = pytz.timezone("America/New_York")

def is_regular_market_hours_now():
    now = datetime.now(NY)
    # Mon-Fri, 9:30-16:00 ET (basic check; holidays not handled)
    if now.weekday() > 4:
        return False
    open_ = now.replace(hour=9, minute=30, second=0, microsecond=0)
    close = now.replace(hour=16, minute=0, second=0, microsecond=0)
    return open_ <= now <= close

import datetime
from butler_offline.core import time
from typing import Callable
from datetime import date
from datetime import datetime


TODAY: Callable[[], date] = lambda: datetime.now().date()
NOW: Callable[[], datetime] = lambda: datetime.now()


def today() -> date:
    return TODAY()


def now() -> datetime:
    return NOW()


def stub_today_with(new_today):
    time.NOW = lambda: datetime(new_today.year, new_today.month, new_today.day)
    time.TODAY = lambda: new_today


def reset_viewcore_stubs():
    time.TODAY = lambda: datetime.now().date()
    time.NOW = lambda: datetime.now()

import datetime

from butler_offline.core import time

TODAY = lambda: now().date()
NOW = lambda: datetime.datetime.now()


def today():
    return TODAY()


def now():
    return NOW()


def stub_today_with(new_today):
    time.NOW = lambda: datetime.datetime(new_today.year, new_today.month, new_today.day)
    time.TODAY = lambda: new_today


def reset_viewcore_stubs():
    time.TODAY = lambda: datetime.datetime.now().date()
    time.NOW = lambda: datetime.datetime.now()

from datetime import date


def _add_month(datum):
    if datum.month < 12:
        datum = date(day=datum.day, month=(datum.month + 1), year=datum.year)
    else:
        datum = date(day=datum.day, month=1, year=datum.year + 1)
    return datum


FREQUENCY_MONATLICH_NAME = 'monatlich'
ALL_FREQUENCY_NAMES = [FREQUENCY_MONATLICH_NAME]

FREQUENCY_MAP = {
    FREQUENCY_MONATLICH_NAME: _add_month
}


def get_function_for_name(name):
    return FREQUENCY_MAP[name]

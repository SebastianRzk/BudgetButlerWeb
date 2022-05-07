from dateutil.relativedelta import relativedelta


def monthly(iteration):
    return relativedelta(months=iteration)


def quarterly(iteration):
    return relativedelta(months=3 * iteration)


def half_yearly(iteration):
    return relativedelta(months=6 * iteration)


def yearly(iteration):
    return relativedelta(years=iteration)


FREQUENCY_MONATLICH_NAME = 'monatlich'
FREQUENCY_VIERTELJAEHRLICH_NAME = 'vierteljaehrlich'
FREQUENCY_HALBJAEHRLICH_NAME = 'halbjaehrlich'
FREQUENCY_JAEHRLICH_NAME = 'jaehrlich'

ALL_FREQUENCY_NAMES = [FREQUENCY_MONATLICH_NAME,
                       FREQUENCY_VIERTELJAEHRLICH_NAME,
                       FREQUENCY_HALBJAEHRLICH_NAME,
                       FREQUENCY_JAEHRLICH_NAME]

FREQUENCY_MAP = {
    FREQUENCY_MONATLICH_NAME: monthly,
    FREQUENCY_VIERTELJAEHRLICH_NAME: quarterly,
    FREQUENCY_HALBJAEHRLICH_NAME: half_yearly,
    FREQUENCY_JAEHRLICH_NAME: yearly
}


def get_function_for_name(name):
    return FREQUENCY_MAP[name]

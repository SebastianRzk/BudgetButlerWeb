from dateutil.relativedelta import relativedelta


def monthly(iteration):
    return relativedelta(months=iteration)


FREQUENCY_MONATLICH_NAME = 'monatlich'
ALL_FREQUENCY_NAMES = [FREQUENCY_MONATLICH_NAME]

FREQUENCY_MAP = {
    FREQUENCY_MONATLICH_NAME: monthly
}


def get_function_for_name(name):
    return FREQUENCY_MAP[name]

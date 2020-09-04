import datetime


def int_default(val, default=0):
    return val if str(val).isdigit() else default


def bool_default(val):
    return val is True


def date_default(val, default=datetime.date(1980, 1, 1)):
    try:
        return datetime.datetime.strptime(str(val), '%Y-%m-%d')
    except ValueError:
        return default

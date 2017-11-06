#
# Copyright Cameron Curry (c) 2017
#

from datetime import datetime


def cast(value, to_type):
    try:
        return to_type(value)
    except ValueError:
        return None


def cast_datetime(value):
    """
    Convert Questrade datetime string to datetime object.
    Questrade datetime format: 2011-02-16T00:00:00.000000-05:00
    
    :param value: The String to be cast
    :return: datetime
    """
    return datetime.strptime(value[:-3] + value[-2:], '%Y-%m-%dT%H:%M:%S.%f%z')

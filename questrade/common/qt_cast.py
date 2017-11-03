#
# Copyright Cameron Curry (c) 2017
#


def cast(value, to_type):
    try:
        return to_type(value)
    except ValueError:
        return None

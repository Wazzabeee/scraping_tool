""" This module regroups different functions used for the GUI """

from datetime import datetime, timedelta


def get_dict_key(dictionnary, value):
    """ Returns the first key associated to value in dictionnary """
    for key, val in dictionnary.items():
        if val == value:
            return key
    return None


def separate_int_string(string):
    """ Returns separated int and string from geocode """

    if len(string) >= 3:

        for i, char in enumerate(string):

            if char.isnumeric():
                pass
            else:
                return string[:i], string[i:]

        return string, ""

    return "0", ""


def validate_date_format(string):
    """ Returns true if date is empty or less than 7 days ago """

    if string is None or string == "":
        return True

    try:
        datetime.strptime(string, "%Y-%m-%d")

        if datetime.strptime(string, "%Y-%m-%d") <= (
                datetime.today() - timedelta(days=8)
        ):
            return False

        return True

    except ValueError:
        return False

from datetime import datetime, timedelta


def get_dict_key(dictionnary, value):
    for key, val in dictionnary.items():
        if val == value:
            return key


def separate_int_string(string):
    if len(string) >= 3:
        for i, char in enumerate(string):
            if char.isnumeric():
                pass
            else:
                return string[:i], string[i:]
        return string, ""
    else:
        return "0", ""


def validate_date_format(string):
    if string is None or string == "":
        return True
    else:
        try:
            datetime.strptime(string, '%Y-%m-%d')

            if datetime.strptime(string, '%Y-%m-%d') <= (datetime.today() -
                                                         timedelta(days=8)):
                return False
            else:
                return True

        except ValueError:
            return False


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

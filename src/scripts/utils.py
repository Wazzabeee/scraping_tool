
def get_dict_key(self, dictionnary, value):
    for key, val in dictionnary.items():
        if val == value:
            return key


def get_result_type(self, val):
    if val == 1:
        return "mixed"
    elif val == 2:
        return "recent"
    else:
        return "popular"
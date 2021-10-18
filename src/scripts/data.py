""" This module saves the last search settings from the GUI

If the search is a success this module will save the filters values to JSON file.
So that on GUI opening we can fill last working settings.

"""

from json import dump


def save_search_settings(query=None, save_path=None, geo_code=None, num=None, date=None, lan=None,
                         res_type=None):
    """ Saves last settings from 7 days search (Search tab) """

    research_data = {'query_research': []}
    research_data['query_research'].append({
        'query': query,
        'save_path': save_path,
        'geocode': geo_code,
        'number': num,
        'until': date,
        'language': lan,
        'research_type': res_type
    })

    with open('../settings/search_settings.json', 'w') as file:
        dump(research_data, file, indent=4)

    print('settings saved')


def save_user_settings(users_lists=None, save_path=None, include_rts=None, exclude_replies=None,
                       trim_user_info=None, since="", until="", res_per_page=None):
    """ Saves last settings from users search (User tab) """

    research_data = {'user_research': []}
    research_data['user_research'].append({
        'users_lists': users_lists,
        'save_path': save_path,
        'since': since,
        'until': until,
        'res_per_page': res_per_page,
        'include_rts': include_rts,
        'exclude_replies': exclude_replies,
        'trim_user_info': trim_user_info
    })

    with open('../settings/user_settings.json', 'w') as file:
        dump(research_data, file, indent=4)

    print('settings saved')

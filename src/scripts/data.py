from json import dump


def save_search_settings(query=None, save_path=None, geo_code=None, num=None, date=None, lan=None,
                         res_type=None):

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

    with open('../settings/search_settings.json', 'w') as f:
        dump(research_data, f, indent=4)

    print('settings saved')


def save_user_settings(users_lists=None, save_path=None, include_rts=None, exclude_replies=None,
                       trim_user_info=None, since="", until="", res_per_page=None):

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

    with open('../settings/user_settings.json', 'w') as f:
        dump(research_data, f, indent=4)

    print('settings saved')

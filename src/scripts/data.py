from json import dump


def save_search_settings(query, save_path, geo_code, num, date, lan, res_type):
    research_data = {'last_research': []}
    research_data['last_research'].append({
        'query': query,
        'save_path': save_path,
        'geocode': geo_code,
        'number': num,
        'until': date,
        'language': lan,
        'research_type': res_type
    })

    with open('../settings/data.json', 'w') as f:
        dump(research_data, f, indent=4)

    print('settings saved')

#!/usr/bin/env python
""" This module retrieves tweet given a search query

Via the Tweepy library, user can retrieve tweets from the last 7 days.
Details about filters available can be found in Twitter's API documentation.
Twitter's API credentials must be filled in constants.py file before
running the script.
To modify search settings see cron_search.json

"""

import json
import sys
from datetime import date, datetime, timedelta
from os import path
import tweepy as tw
from constants import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


def auth(consumer_key, consumer_secret, access_token, access_token_secret):
    """ Authentificates the user with Twitter's API """

    authentification = tw.OAuthHandler(consumer_key, consumer_secret)
    authentification.set_access_token(access_token, access_token_secret)
    # If rate limit is reached, user will be notified and cursor will wait to continue
    return tw.API(authentification, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_search_filename(tweet_num, tweet_lan, res_type):
    """ Returns the results filename for the current search """

    return datetime.now().strftime("%Y%m%d_%H%M%S") + '_' + str(tweet_num) + '_' + tweet_lan \
        + '_' + res_type


def save_to_json(tweets, save_path, filename):
    """ Saves the tweets to the specified path with specified filename """

    print('results saved in :' + save_path + '/' + filename + '.json')
    with open(path + '/' + filename + '.json', 'w') as outfile:
        json.dump(tweets, outfile, indent=4)


def api_search(search_query, save_directory, geocode="", number=2600, until_date="", language="en",
               res_type="recent"):
    """ Calls Twitter's GET 7 days search API function  """

    api = auth(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    dict_tweets = {'tweets': []}

    tweets_count = 0
    for tweet in tw.Cursor(api.search, q=search_query, geocode=geocode, lang=language,
                           until=until_date,
                           result_type=res_type, tweet_mode="extended").items(number):
        dict_tweets['tweets'].append(tweet._json)
        tweets_count += 1

    filename = get_search_filename(tweets_count, language, res_type)
    save_to_json(dict_tweets, save_directory, filename)


if __name__ == '__main__':

    if path.exists('../settings/cron_search.json'):
        query, path, geo, num, until, result_type, lan = None, None, None, None, \
                                                         None, None, None
        with open('../settings/cron_search.json') as f:
            data = json.load(f)

            for item in data['settings']:
                if item['query'] != "":
                    query = item['query']
                if item['save_path'] != "":
                    path = item['save_path']
                if item['geocode'] != "":
                    geo = item['geocode']
                if item['number'] != 0:
                    num = item['number']
                if item['until'] != "":
                    until = item['until']
                else:
                    until = date.today() - timedelta(days=7)

                if item['research_type'] != "":
                    result_type = item['research_type']
                if item['language'] != "":
                    lan = item['language']
        print(query, path, geo, num, until, lan, result_type)
        api_search(query, path, geo, num, until, lan, result_type)

    sys.exit()

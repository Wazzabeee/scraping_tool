import json
from datetime import date, datetime, timedelta
from os import path
from sys import exit
import tweepy as tw
from constants import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


def auth(consumer_key, consumer_secret, access_token, access_token_secret):
    authentification = tw.OAuthHandler(consumer_key, consumer_secret)
    authentification.set_access_token(access_token, access_token_secret)
    return tw.API(authentification, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_search_filename(number, language, res_type):
    return datetime.now().strftime("%Y%m%d_%H%M%S") + '_' + str(number) + '_' + language \
           + '_' + res_type


def save_to_json(tweets, path, filename):
    print('results saved in :' + path + '/' + filename + '.json')
    with open(path + '/' + filename + '.json', 'w') as outfile:
        json.dump(tweets, outfile, indent=4)


def api_search(query, save_directory, geocode="", number=3200, until="", language="en",
               res_type="recent"):
    api = auth(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    dict_tweets = {'tweets': []}

    tweets_count = 0
    for tweet in tw.Cursor(api.search, q=query, geocode=geocode, lang=language, until=until,
                           result_type=res_type, tweet_mode="extended").items(number):
        dict_tweets['tweets'].append(tweet._json)
        tweets_count += 1

    filename = get_search_filename(tweets_count, language, res_type)
    save_to_json(dict_tweets, save_directory, filename)


if __name__ == '__main__':

    if path.exists('../settings/cron_search.json'):
        query, path, geocode, number, until, result_type, language = None, None, None, None, \
                                                                     None, None, None
        with open('../settings/cron_search.json') as f:
            data = json.load(f)

            for item in data['settings']:
                if item['query'] != "":
                    query = item['query']
                if item['save_path'] != "":
                    path = item['save_path']
                if item['geocode'] != "":
                    geocode = item['geocode']
                if item['number'] != 0:
                    number = item['number']
                if item['until'] != "":
                    until = item['until']
                else:
                    until = date.today() - timedelta(days=7)

                if item['research_type'] != "":
                    result_type = item['research_type']
                if item['language'] != "":
                    language = item['language']
        print(query, path, geocode, number, until, language, result_type)
        api_search(query, path, geocode, number, until, language, result_type)

    exit()

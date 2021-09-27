from constants import CONSUMER_SECRET, CONSUMER_KEY, ACCESS_TOKEN_SECRET, ACCESS_TOKEN
from datetime import date
import tweepy as tw
import json


def auth(consumer_key, consumer_secret, access_token, access_token_secret):
    authentification = tw.OAuthHandler(consumer_key, consumer_secret)
    authentification.set_access_token(access_token, access_token_secret)
    return tw.API(authentification, wait_on_rate_limit=True)


def format_file_name(number, language, res_type):

    return date.today().strftime("%b-%d-%Y") + '_' + str(number) + '_' + language + '_' + res_type


def json_dump(tweets, path, filename):

    print('results saved in :' + path + '/' + filename + '.json')
    with open(path + '/' + filename + '.json', 'w') as outfile:
        json.dump(tweets, outfile, indent=4)


def test_api(query, save_directory, geocode="", number=10, language="en", res_type="recent"):

    api = auth(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    tweets = tw.Cursor(api.search, q=query, geocode=geocode, lang=language,
                       result_type=res_type).items(
        number)

    dict_tweets = {'tweets': []}

    for tweet in tweets:
        dict_tweets['tweets'].append(tweet._json)

    filename = format_file_name(number, language, res_type)
    json_dump(dict_tweets, save_directory, filename)

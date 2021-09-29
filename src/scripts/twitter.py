from constants import CONSUMER_SECRET, CONSUMER_KEY, ACCESS_TOKEN_SECRET, ACCESS_TOKEN
import tweepy as tw
import json
from datetime import datetime, timedelta, date

def auth(consumer_key, consumer_secret, access_token, access_token_secret):
    authentification = tw.OAuthHandler(consumer_key, consumer_secret)
    authentification.set_access_token(access_token, access_token_secret)
    return tw.API(authentification, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def format_file_name(number, language, res_type):

    return date.today().strftime("%b-%d-%Y") + '_' + str(number) + '_' + language + '_' + res_type


def json_dump(tweets, path, filename):

    print('results saved in :' + path + '/' + filename + '.json')
    with open(path + '/' + filename + '.json', 'w') as outfile:
        json.dump(tweets, outfile, indent=4)


def test_api(query, save_directory, geocode="", number=10, until="", language="en",
             res_type="recent"):

    api = auth(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    tweets = tw.Cursor(api.search, q=query, geocode=geocode, lang=language, until=until,
                       result_type=res_type).items(
        number)

    dict_tweets = {'tweets': []}

    for tweet in tweets:
        dict_tweets['tweets'].append(tweet._json)

    filename = format_file_name(number, language, res_type)
    json_dump(dict_tweets, save_directory, filename)
    return True


def retrieve_tweets_from_users_list(users_list, date, count):

    api = auth(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    for user in users_list:
        all_tweets = []
        tweet_count = 0
        end_date = datetime.utcnow() - timedelta(days=365)
        for status in tw.Cursor(api.user_timeline, id=user).items():
            print(status)
            tweet_count += 1
            all_tweets.append(status)
            if status.created_at < end_date:
                break
        print('' + str(tweet_count) + ' tweets retrieved')
        dict_tweets = {'tweets': []}
        for tweet in all_tweets:
            dict_tweets['tweets'].append(tweet._json)

        save_directory = "C:\\Users\\Clément\\Documents\\GitHub\\scraping_tool\\output"
        filename = 'test2'
        json_dump(dict_tweets, save_directory, filename)

from constants import CONSUMER_SECRET, CONSUMER_KEY, ACCESS_TOKEN_SECRET, ACCESS_TOKEN
import tweepy as tw
import json


def auth(consumer_key, consumer_secret, access_token, access_token_secret):
    authentification = tw.OAuthHandler(consumer_key, consumer_secret)
    authentification.set_access_token(access_token, access_token_secret)
    return tw.API(authentification, wait_on_rate_limit=True)


def json_dump(tweets, path):
    # path = "C:\\Users\\Clément\\PycharmProjects\\twitter_api\\output"

    with open('data.json', 'w') as outfile:
        json.dump(tweets, outfile, indent=4)

    print("done")


def hello_world():
    print("hello world")


def test_api(query, number, language, type, save_directory):
    api = auth(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    tweets = tw.Cursor(api.search, q=query, lang='fr', result_type=type).items(number)
    # search_words = "#boruto -filter:retweets"
    # tweets = tw.Cursor(api.search,
                       # q=search_words).items(5)

    dict_tweets = {}
    dict_tweets['tweets'] = []

    for tweet in tweets:
        dict_tweets['tweets'].append(tweet._json)

    json_dump(dict_tweets, save_directory)
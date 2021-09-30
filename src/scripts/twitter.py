from constants import CONSUMER_SECRET, CONSUMER_KEY, ACCESS_TOKEN_SECRET, ACCESS_TOKEN
import tweepy as tw
import json
from datetime import datetime


def auth(consumer_key, consumer_secret, access_token, access_token_secret):
    authentification = tw.OAuthHandler(consumer_key, consumer_secret)
    authentification.set_access_token(access_token, access_token_secret)
    return tw.API(authentification, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def save_to_json(tweets, path, filename):
    print('results saved in :' + path + '/' + filename + '.json')
    with open(path + '/' + filename + '.json', 'w') as outfile:
        json.dump(tweets, outfile, indent=4)


def get_user_filename(user, count):
    return datetime.now().strftime("%b-%d-%Y_%H%M%S") + '_' + user + '_' + str(count)


def get_search_filename(number, language, res_type):
    return datetime.now().strftime("%b-%d-%Y_%H%M%S") + '_' + str(number) + '_' + language \
           + '_' + res_type


def api_search(query, save_directory, geocode="", number=10, until="", language="en",
               res_type="recent"):
    api = auth(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    dict_tweets = {'tweets': []}

    for tweet in tw.Cursor(api.search, q=query, geocode=geocode, lang=language, until=until,
                           result_type=res_type).items(number):
        dict_tweets['tweets'].append(tweet._json)

    filename = get_search_filename(number, language, res_type)
    save_to_json(dict_tweets, save_directory, filename)
    return True


def retrieve_tweets_from_users_list(users_list, path, since_id=None, count=None,
                                    max_id=None, trim_user=False, exclude_replies=False,
                                    include_rts=False):

    api = auth(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    user_count = 0
    for user in users_list:
        print(users_list, path, since_id, count, max_id, trim_user, exclude_replies, include_rts)
        dict_tweets = {'tweets': []}
        tweet_count = 0
        user_count += 1
        # end_date = datetime.utcnow() - timedelta(days=365)
        print("" + str(user_count - 1) + " user done out of " + str(len(users_list)) + " users")
        print("Looking for tweets of " + user + ". Please wait...")

        for status in tw.Cursor(api.user_timeline, id=user, since_id=since_id, count=count,
                                max_id=max_id, trim_user=trim_user,
                                exclude_replies=exclude_replies, include_rts=include_rts).items():
            tweet_count += 1
            dict_tweets['tweets'].append(status._json)
            # if status.created_at < end_date:
            # break

        print('' + str(tweet_count) + ' tweets retrieved fron ' + user)

        filename = get_user_filename(user, tweet_count)
        save_to_json(dict_tweets, path, filename)

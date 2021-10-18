import json
from datetime import datetime

import tweepy as tw

from constants import CONSUMER_SECRET, CONSUMER_KEY, ACCESS_TOKEN_SECRET, ACCESS_TOKEN


def auth(consumer_key, consumer_secret, access_token, access_token_secret):
    """ This function authentificates the user with Twitter's API """

    authentification = tw.OAuthHandler(consumer_key, consumer_secret)
    authentification.set_access_token(access_token, access_token_secret)
    return tw.API(authentification, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def save_to_json(tweets, path, filename):
    """ This function save the tweets to the specified path with specified filename """
    print('results saved in :' + path + '/' + filename + '.json')
    with open(path + '/' + filename + '.json', 'w') as outfile:
        json.dump(tweets, outfile, indent=4)


def get_user_filename(user, count):
    """ This function returns the results filename for the user search """

    return datetime.now().strftime("%Y%m%d_%H%M%S") + '_' + user + '_' + str(count)


def get_search_filename(number, language, res_type):
    """ This function returns the results filename for the general search """

    return datetime.now().strftime("%Y%m%d_%H%M%S") + '_' + str(number) + '_' + language \
        + '_' + res_type


def api_search(query, save_directory, geocode="", number=10, until="", language="en",
               res_type="recent"):
    """ This function communicates with Twitter's GET search API endpoint """

    api = auth(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    dict_tweets = {'tweets': []}
    print("Starting research. . .")
    tweets_count = 0
    for tweet in tw.Cursor(api.search, q=query, geocode=geocode, lang=language, until=until,
                           result_type=res_type, tweet_mode="extended").items(number):
        dict_tweets['tweets'].append(tweet._json)
        tweets_count += 1

    print(str(tweets_count) + " tweets retrieved out of " + str(number) + " wanted")
    filename = get_search_filename(tweets_count, language, res_type)
    save_to_json(dict_tweets, save_directory, filename)
    return True


def retrieve_tweets_from_users_list(users_list, path, since=None, count=None,
                                    until=None, trim_user=False, exclude_replies=False,
                                    include_rts=False):
    """ This function communicates with Twitter's GET statuses/user_timeline API endpoint """

    api = auth(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    user_count = 0
    for user in users_list:
        dict_tweets = {'tweets': []}
        tweet_count = 0
        user_count += 1
        print("" + str(user_count - 1) + " user done out of " + str(len(users_list)) + " users")
        print("Looking for tweets of " + user + ". Please wait...")

        for status in tw.Cursor(api.user_timeline, id=user, count=count,
                                trim_user=trim_user,
                                exclude_replies=exclude_replies, include_rts=include_rts).items():
            if since is not None and until is not None:
                if since != "" and until != "":
                    since_for = datetime.strptime(since, '%Y-%m-%d')
                    until_for = datetime.strptime(until, "%Y-%m-%d")

                    if since_for > status.created_at > until_for:
                        tweet_count += 1
                        dict_tweets['tweets'].append(status._json)
                    elif since_for > status.created_at and until_for > status.created_at:
                        break
            else:
                tweet_count += 1
                dict_tweets['tweets'].append(status._json)

        print('' + str(tweet_count) + ' tweets retrieved fron ' + user)

        filename = get_user_filename(user, tweet_count)
        save_to_json(dict_tweets, path, filename)
        return True

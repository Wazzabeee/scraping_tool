import csv
import json
from datetime import datetime
from os import path
from sys import exit

import tweepy as tw

from constants import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


def auth(consumer_key, consumer_secret, access_token, access_token_secret):
    authentification = tw.OAuthHandler(consumer_key, consumer_secret)
    authentification.set_access_token(access_token, access_token_secret)
    return tw.API(authentification, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_user_filename(user, count):
    return datetime.now().strftime("%Y%m%d_%H%M%S") + '_' + user + '_' + str(count)


def save_to_json(tweets, path, filename):
    print('results saved in :' + path + '/' + filename + '.json')
    with open(path + '/' + filename + '.json', 'w') as outfile:
        json.dump(tweets, outfile, indent=4)


def get_users_from_file(path):
    names = []
    with open(path, newline="") as user_file:
        for row in csv.reader(user_file):
            names.append(row[0])

    return names


def api_user(users_list, path, since=None, count=None,
             until=None, trim_user=False, exclude_replies=False,
             include_rts=False):

    api = auth(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    user_count = 0
    for user in users_list:
        print(users_list, path, since, count, until, trim_user, exclude_replies, include_rts)
        dict_tweets = {'tweets': []}
        tweet_count = 0
        user_count += 1
        print("" + str(user_count - 1) + " user done out of " + str(len(users_list)) + " users")
        print("Looking for tweets of " + user + ". Please wait...")

        for status in tw.Cursor(api.user_timeline, id=user, count=count,
                                trim_user=trim_user,
                                exclude_replies=exclude_replies, include_rts=include_rts).items():
            if since is not None and until is not None:
                since_for = datetime.strptime(since, '%Y-%m-%d')
                until_for = datetime.strptime(until, "%Y-%m-%d")

                if since_for > status.created_at > until_for:
                    tweet_count += 1
                    dict_tweets['tweets'].append(status._json)
            else:
                tweet_count += 1
                dict_tweets['tweets'].append(status._json)

        print('' + str(tweet_count) + ' tweets retrieved fron ' + user)

        filename = get_user_filename(user, tweet_count)
        save_to_json(dict_tweets, path, filename)


if __name__ == '__main__':

    if path.exists('../settings/cron_user.json'):
        users, path, since, count, until, trim_user, exclude_replies, include_rts = None, None, \
                                                                                    None, None, \
                                                                                    None, False, \
                                                                                    False, False

        with open('../settings/cron_user.json') as f:
            data = json.load(f)

            for item in data['settings']:
                if item['users'] != "":
                    users_path = item['users']
                if item['save_path'] != "":
                    path = item['save_path']
                if item['since'] != "":
                    since = item['since']
                if item['count'] != 0:
                    count = item['count']
                if item['until'] != "":
                    until = item['until']
                if item['trim_user'] != "":
                    trim_user = item['trim_user']
                if item['exclude_replies'] != "":
                    exclude_replies = item['exclude_replies']
                if item['include_rts'] != "":
                    include_rts = item['include_rts']
        if users_path is not None and path is not None:
            users = get_users_from_file(users_path)

            if len(users) >= 1:
                api_user(users, path, since, count, until, trim_user,
                         exclude_replies, include_rts)

    exit()

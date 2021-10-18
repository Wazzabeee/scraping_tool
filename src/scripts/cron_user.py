#!/usr/bin/env python
""" This module retrieves tweets from a list of users

Via the Tweepy library, user can retrieve tweets from a list of users.
Details about filters available can be found in Twitter's API documentation.
Twitter's API credentials must be filled in constants.py file before
running the script.
To modify search settings see cron_user.json

"""

import csv
import json
import sys
from datetime import datetime
from os import path

import tweepy as tw

from constants import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


def auth(consumer_key, consumer_secret, access_token, access_token_secret):
    """ Authentificates the user with Twitter's API """

    authentification = tw.OAuthHandler(consumer_key, consumer_secret)
    authentification.set_access_token(access_token, access_token_secret)
    return tw.API(authentification, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_user_filename(user, tweets_count):
    """ Returns the results filename for the current user """

    return datetime.now().strftime("%Y%m%d_%H%M%S") + '_' + user + '_' + str(tweets_count)


def save_to_json(tweets, path_to_save, filename):
    """ Saves the tweets to the specified path with specified filename """

    print('results saved in :' + path_to_save + '/' + filename + '.json')
    with open(path_to_save + '/' + filename + '.json', 'w') as outfile:
        json.dump(tweets, outfile, indent=4)


def get_users_from_file(users_file_path):
    """ Extracts users from CSV file to list """

    names = []
    with open(users_file_path, newline="") as user_file:
        for row in csv.reader(user_file):
            names.append(row[0])

    return names


def api_user(list_users, saving_path, since=None, tw_count=None,
             until=None, trim_user=False, exclude_rep=False,
             include_rts=False):
    """ Calls Twitter's GET User/Timeline API function  """

    api = auth(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    user_count = 0
    for user in list_users:
        print(list_users, saving_path, since, tw_count, until, trim_user, exclude_rep,
              include_rts)
        dict_tweets = {'tweets': []}
        tweet_count = 0
        user_count += 1
        print("" + str(user_count - 1) + " user done out of " + str(len(users_list)) + " users")
        print("Looking for tweets of " + user + ". Please wait...")

        for status in tw.Cursor(api.user_timeline, id=user, count=tw_count,
                                trim_user=trim_user,
                                exclude_replies=exclude_rep, include_rts=include_rts).items():
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
        save_to_json(dict_tweets, saving_path, filename)


if __name__ == '__main__':

    if path.exists('../settings/cron_user.json'):
        users_list, save_path, since_date, count, until_date, trim_user_id, exclude_replies, \
        include_rt = None, None, \
                     None, None, \
                     None, False, \
                     False, False

        with open('../settings/cron_user.json') as f:
            data = json.load(f)

            for item in data['settings']:
                if item['users'] != "":
                    users_list = item['users']
                if item['save_path'] != "":
                    save_path = item['save_path']
                if item['since'] != "":
                    since_date = item['since']
                if item['count'] != 0:
                    count = item['count']
                if item['until'] != "":
                    until_date = item['until']
                if item['trim_user'] != "":
                    trim_user_id = item['trim_user']
                if item['exclude_replies'] != "":
                    exclude_replies = item['exclude_replies']
                if item['include_rts'] != "":
                    include_rt = item['include_rts']
        if users_list is not None and save_path is not None:
            users = get_users_from_file(users_list)

            if len(users) >= 1:
                api_user(users, save_path, since_date, count, until_date, trim_user_id,
                         exclude_replies, include_rt)

    sys.exit()

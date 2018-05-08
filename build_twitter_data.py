"""
buid_twitter_data.py

Methods for building our data from twitter:
    friends lists/network,
    user/network tweet tweets,
"""

import json
from twitter_methods import get_friends_ids, get_timeline
import sys
import random


def build_friends_list(screenName):
    """
    For each user used as a source, compile a list
    of their friends and store in a json file.
    """
    friendsList = get_friends_ids(screenName)
    open('data/{}-friends.json'.format(screenName), 'w').write((json.dumps(friendsList)))
    return len(friendsList)

def get_network_tweets(screenName):
    """
    For given user, get the timeline of each of their freinds
    and store in a json file.
    """
    # TODO: figure out why there's an error every time
    friendsIDS = json.loads(open('data/{}-friends.json'.format(screenName), 'r').read())
    allTweets = []
    for id in friendsIDS:
        timeline = get_timeline(id=id)
        print('Retrieved {} Tweets from {}\'s timeline.'.format(len(timeline), id))
        tweets = [
            {
                key: tweet[key] for key in ['created_at',
                                            'id',
                                            'id_str',
                                            'text',
                                            'truncated',
                                            'entities',
                                            'retweet_count',
                                            'favorite_count',
                                            'user']
            }
            for tweet in timeline
        ]
        print(len(tweets))
        allTweets.extend(tweets)

    print(len(allTweets))
    open('data/{}-network-tweets.json'.format(screenName), 'w').write((json.dumps(allTweets)))


def get_user_tweets(screenName):
    """
    Get the timeline of the given user and store in a json file.
    """
    timeline = get_timeline(screenName=screenName)
    print('Retrieved {} Tweets from {}\'s timeline.'.format(len(timeline), screenName))
    tweets = [
        {
            key: tweet[key] for key in ['created_at',
                                        'id',
                                        'id_str',
                                        'text',
                                        'truncated',
                                        'entities',
                                        'retweet_count',
                                        'favorite_count']
        }
        for tweet in timeline
    ]
    print(len(tweets))
    open('data/{}-tweets.json'.format(screenName), 'w').write((json.dumps(tweets)))

def get_random_sample_tweets(numUsers):
    """
    Generate a list of random user ids, fetch tweets
    from each one.
    """
    userIDS = json.loads(open('data/random-users-{}.json'.format(numUsers), 'r').read())
    allTweets = []
    for id in userIDS:
        try:
            timeline = get_timeline(id=id)
            print('Retrieved {} Tweets from {}\'s timeline.'.format(len(timeline), id))
            tweets = [
                {
                    key: tweet[key] for key in ['created_at',
                                                'id',
                                                'id_str',
                                                'text',
                                                'truncated',
                                                'entities',
                                                'retweet_count',
                                                'favorite_count',
                                                'user']
                }
                for tweet in timeline
            ]
            print(len(tweets))
            allTweets.extend(tweets)

        except TwitterHTTPError as e:
            print(e)
            print('Moving on')

    print(len(allTweets))
    open('data/random-sample-tweets-{}.json'.format(181), 'w').write((json.dumps(allTweets)))



if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'build_friends_list':
            build_friends_list()
        elif sys.argv[1] == 'get_network_tweets':
            if len(sys.argv) > 2:
                get_network_tweets(sys.argv[2])
            else:
                raise Exception('No screen name provied.')
        elif sys.argv[1] == 'get_user_tweets':
            if len(sys.argv) > 2:
                get_user_tweets(sys.argv[2])
            else:
                raise Exception('No screen name provied.')
        elif sys.argv[1] == 'get_random_sample_tweets':
            if len(sys.argv) > 2:
                get_random_sample_tweets(sys.argv[2])
            else:
                get_random_sample_tweets(181)
        elif sys.argv[1] == 'get_random_sample_users':
            if len(sys.argv) > 2:
                get_random_sample_users(sys.argv[2])
            else:
                get_random_sample_users(180)
        else:
            raise Exception('Invalid instruction.')
    else:
        raise Exception('No instruction provied.')

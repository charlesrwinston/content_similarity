"""
twitter_methods.py

File containing procedures interacting with the Twitter API
"""

from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
from keys import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET
import time

# Get authorization fro Twitter API
oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter API
twitter = Twitter(auth=oauth)

def get_friends_ids(screenName):
    """
    Return a list of screenName's friends ids
    """
    cursor = -1
    friends = []
    while cursor != 0:
        try:
            result = twitter.friends.ids(screen_name=screenName, cursor=cursor)
            friends.extend(result['ids'])
            cursor = result['next_cursor']
        except TwitterHTTPError as e:
            """
            Rate limit exceeded
            """
            print(e)
            print('Rate Limit Exceeded. Waiting 15 minutes until the next window.')
            time.sleep(15 * 60 + 5)

    return friends

def get_timeline(id=None, screenName=None, count=200):
    """
    Return Tweet timeline from user with specified id
    """
    print(id)
    result = None
    while not result:
        try:
            if id:
                result = twitter.statuses.user_timeline(user_id=id, count=count)
            elif screenName:
                result = twitter.statuses.user_timeline(screen_name=screenName, count=count)
            return result
        except TwitterHTTPError as e:
            """
            Catch Error
            """
            print(e)
            if e.message == 'Rate limit exceeded':
                print('Rate limit exceeded. Waiting 15 minutes until the next window.')
                time.sleep(15 * 60 + 5)
            else:
                return []

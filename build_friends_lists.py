"""
build_friends_list.py

For each user used as a source, compile a list
of their friends and store in a json file.
"""

import json
from twitter_methods import get_friends_ids

# List of screen names used as sources
sourceScreenNames = [
    'realDonaldTrump',

    'katyperry',
    'rihanna',
    'Beyonce',

    'KingJames',
    'StephenCurry30',
    'KDTrey5',

    'jaketapper',
    'megynkelly',
    'maddow',
    'NateSilver538'
]

# Get list of friends for each user
for screenName in sourceScreenNames:
    friendsList = get_friends_ids(screenName)
    open('data/{}-friends.json'.format(screenName), 'w').write((json.dumps(friendsList)))

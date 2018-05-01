"""
entity_analysis.py

Contains methods for computing entity vectors
"""

import json
import operator

screenName = 'KingJames'
tweets = json.loads(open('data/{}-tweets.json'.format(screenName), 'r').read())

entities = {}
for tweet in tweets:
    currEntites = tweet['entities']
    for hashtag in currEntites['hashtags']:
        entities.setdefault(hashtag['text'], 0)
        entities[hashtag['text']] += 1
    for mention in currEntites['user_mentions']:
        entities.setdefault(mention['screen_name'], 0)
        entities[mention['screen_name']] += 1

sortedEntities = sorted(entities.items(), key=operator.itemgetter(1))
print(len(sortedEntities))
open('entities.json', 'w').write(json.dumps(sortedEntities))

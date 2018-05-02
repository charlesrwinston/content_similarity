"""
entity_analysis.py

Contains methods for computing entity vectors
"""

import json
import operator
import sys
import numpy as np
from vector_math import cosine_similarity

def get_entities_from_tweets(screenName):
    userTweets = json.loads(open('data/{}-tweets.json'.format(screenName), 'r').read())
    networkTweets = json.loads(open('data/{}-network-tweets.json'.format(screenName), 'r').read())

    userEntities = {}
    networkEntities = {}
    entityDimensions = {}

    currentDimension = 0
    for tweet in networkTweets:
        currEntites = tweet['entities']
        for hashtag in currEntites['hashtags']:
            networkEntities.setdefault(hashtag['text'], 0)
            networkEntities[hashtag['text']] += 1
            dimension = entityDimensions.setdefault(hashtag['text'], currentDimension)
            if dimension == currentDimension:   # entity not found before
                currentDimension += 1
        for mention in currEntites['user_mentions']:
            networkEntities.setdefault(mention['screen_name'], 0)
            networkEntities[mention['screen_name']] += 1
            dimension = entityDimensions.setdefault(mention['screen_name'], currentDimension)
            if dimension == currentDimension:   # entity not found before
                currentDimension += 1

    print('Total dimensions after network: {}'.format(currentDimension))

    for tweet in userTweets:
        currEntites = tweet['entities']
        for hashtag in currEntites['hashtags']:
            userEntities.setdefault(hashtag['text'], 0)
            userEntities[hashtag['text']] += 1
            dimension = entityDimensions.setdefault(hashtag['text'], currentDimension)
            if dimension == currentDimension:   # entity not found before
                currentDimension += 1
        for mention in currEntites['user_mentions']:
            userEntities.setdefault(mention['screen_name'], 0)
            userEntities[mention['screen_name']] += 1
            dimension = entityDimensions.setdefault(mention['screen_name'], currentDimension)
            if dimension == currentDimension:   # entity not found before
                currentDimension += 1

    print('Total dimensions total: {}'.format(currentDimension))

    sortedUserEntities = sorted(userEntities.items(), key=operator.itemgetter(1), reverse=True)
    sortedNetworkEntities = sorted(networkEntities.items(), key=operator.itemgetter(1), reverse=True)
    print('Length of user entities: {}'.format(len(sortedUserEntities)))
    print('Length of network entities: {}'.format(len(sortedNetworkEntities)))

    open('data/{}-sorted-user-entities.json'.format(screenName), 'w').write(json.dumps(sortedUserEntities))
    open('data/{}-sorted-network-entities.json'.format(screenName), 'w').write(json.dumps(sortedNetworkEntities))
    open('data/{}-user-entities.json'.format(screenName), 'w').write(json.dumps(userEntities))
    open('data/{}-network-entities.json'.format(screenName), 'w').write(json.dumps(networkEntities))
    open('data/{}-entity-dimensions.json'.format(screenName), 'w').write(json.dumps(entityDimensions))

def build_entity_vectors(screenName):
    sortedUserEntities = json.loads(open('data/{}-sorted-user-entities.json'.format(screenName), 'r').read())
    sortedNetworkEntities = json.loads(open('data/{}-sorted-network-entities.json'.format(screenName), 'r').read())
    userEntities = json.loads(open('data/{}-user-entities.json'.format(screenName), 'r').read())
    networkEntities = json.loads(open('data/{}-network-entities.json'.format(screenName), 'r').read())
    entityDimensions = json.loads(open('data/{}-entity-dimensions.json'.format(screenName), 'r').read())

    userVector = np.zeros(len(entityDimensions), dtype=int)
    networkVector = np.zeros(len(entityDimensions), dtype=int)

    for pair in sortedUserEntities:
        entity = pair[0]
        count = pair[1]
        np.put(userVector, entityDimensions[entity], count)

    for pair in sortedNetworkEntities:
        entity = pair[0]
        count = pair[1]
        np.put(networkVector, entityDimensions[entity], count)

    np.save('{}-user-vector'.format(screenName), userVector)
    np.save('{}-network-vector'.format(screenName), networkVector)

    similarity = cosine_similarity(userVector, networkVector)
    similarityObject = {
        'similarity': similarity,
        'total_dimensions': len(entityDimensions)
    }
    open('{}-similarity.json'.format(screenName), 'w').write(json.dumps(similarityObject))



if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'get_entities_from_tweets':
            if len(sys.argv) > 2:
                get_entities_from_tweets(sys.argv[2])
            else:
                raise Exception('No screen name provied.')
        elif sys.argv[1] == 'build_entity_vectors':
            if len(sys.argv) > 2:
                build_entity_vectors(sys.argv[2])
            else:
                raise Exception('No screen name provied.')
        else:
            raise Exception('Invalid instruction.')
    else:
        raise Exception('No instruction provied.')

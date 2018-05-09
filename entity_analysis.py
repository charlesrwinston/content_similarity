"""
entity_analysis.py

Contains methods for computing entity vectors
"""

import json
import operator
import sys
import numpy as np
from vector_math import cosine_similarity

def get_entities_from_tweets(screenName, random=False, numFriends=181, noScreenName=False, noUserMentions=False):
    userTweets = json.loads(open('data/{}-tweets.json'.format(screenName), 'r').read())
    if random:
        sampleTweets = json.loads(open('data/random-sample-tweets-{}.json'.format(numFriends), 'r').read())
    else:
        sampleTweets = json.loads(open('data/{}-network-tweets.json'.format(screenName), 'r').read())

    userEntities = {}
    sampleEntities = {}
    entityDimensions = {}

    currentDimension = 0
    for tweet in sampleTweets:
        currEntites = tweet['entities']
        for hashtag in currEntites['hashtags']:
            sampleEntities.setdefault(hashtag['text'], 0)
            sampleEntities[hashtag['text']] += 1
            dimension = entityDimensions.setdefault(hashtag['text'], currentDimension)
            if dimension == currentDimension:   # entity not found before
                currentDimension += 1
        for mention in currEntites['user_mentions']:
            if noScreenName and mention['screen_name'] == screenName:
                pass
            else:
                sampleEntities.setdefault(mention['screen_name'], 0)
                sampleEntities[mention['screen_name']] += 1
                dimension = entityDimensions.setdefault(mention['screen_name'], currentDimension)
                if dimension == currentDimension:   # entity not found before
                    currentDimension += 1

    print('Total dimensions after sample: {}'.format(currentDimension))

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
    sortedSampleEntities = sorted(sampleEntities.items(), key=operator.itemgetter(1), reverse=True)
    print('Length of user entities: {}'.format(len(sortedUserEntities)))
    print('Length of sample entities: {}'.format(len(sortedSampleEntities)))

    if random:
        open('data/{}-avg-sorted-user-entities.json'.format(screenName), 'w').write(json.dumps(sortedUserEntities))
        open('data/{}-avg-sorted-sample-entities.json'.format(screenName), 'w').write(json.dumps(sortedSampleEntities))
        open('data/{}-avg-user-entities.json'.format(screenName), 'w').write(json.dumps(userEntities))
        open('data/{}-avg-sample-entities.json'.format(screenName), 'w').write(json.dumps(sampleEntities))
        open('data/{}-avg-entity-dimensions.json'.format(screenName), 'w').write(json.dumps(entityDimensions))
    elif noScreenName:
        open('data/{}-no-screen-name-sorted-user-entities.json'.format(screenName), 'w').write(json.dumps(sortedUserEntities))
        open('data/{}-no-screen-name-sorted-sample-entities.json'.format(screenName), 'w').write(json.dumps(sortedSampleEntities))
        open('data/{}-no-screen-name-user-entities.json'.format(screenName), 'w').write(json.dumps(userEntities))
        open('data/{}-no-screen-name-sample-entities.json'.format(screenName), 'w').write(json.dumps(sampleEntities))
        open('data/{}-no-screen-name-entity-dimensions.json'.format(screenName), 'w').write(json.dumps(entityDimensions))
    else:
        open('data/{}-sorted-user-entities.json'.format(screenName), 'w').write(json.dumps(sortedUserEntities))
        open('data/{}-sorted-sample-entities.json'.format(screenName), 'w').write(json.dumps(sortedSampleEntities))
        open('data/{}-user-entities.json'.format(screenName), 'w').write(json.dumps(userEntities))
        open('data/{}-sample-entities.json'.format(screenName), 'w').write(json.dumps(sampleEntities))
        open('data/{}-entity-dimensions.json'.format(screenName), 'w').write(json.dumps(entityDimensions))

def build_entity_vectors(screenName, random=False, numFriends=181, noScreenName=False, noUserMentions=False):
    if random:
        sortedUserEntities = json.loads(open('data/{}-avg-sorted-user-entities.json'.format(screenName), 'r').read())
        sortedSampleEntities = json.loads(open('data/{}-avg-sorted-sample-entities.json'.format(screenName), 'r').read())
        userEntities = json.loads(open('data/{}-avg-user-entities.json'.format(screenName), 'r').read())
        sampleEntities = json.loads(open('data/{}-avg-sample-entities.json'.format(screenName), 'r').read())
        entityDimensions = json.loads(open('data/{}-avg-entity-dimensions.json'.format(screenName), 'r').read())
    elif noScreenName:
        sortedUserEntities = json.loads(open('data/{}-no-screen-name-sorted-user-entities.json'.format(screenName), 'r').read())
        sortedSampleEntities = json.loads(open('data/{}-no-screen-name-sorted-sample-entities.json'.format(screenName), 'r').read())
        userEntities = json.loads(open('data/{}-no-screen-name-user-entities.json'.format(screenName), 'r').read())
        sampleEntities = json.loads(open('data/{}-no-screen-name-sample-entities.json'.format(screenName), 'r').read())
        entityDimensions = json.loads(open('data/{}-no-screen-name-entity-dimensions.json'.format(screenName), 'r').read())
    else:
        sortedUserEntities = json.loads(open('data/{}-sorted-user-entities.json'.format(screenName), 'r').read())
        sortedSampleEntities = json.loads(open('data/{}-sorted-sample-entities.json'.format(screenName), 'r').read())
        userEntities = json.loads(open('data/{}-user-entities.json'.format(screenName), 'r').read())
        sampleEntities = json.loads(open('data/{}-sample-entities.json'.format(screenName), 'r').read())
        entityDimensions = json.loads(open('data/{}-entity-dimensions.json'.format(screenName), 'r').read())

    userVector = np.zeros(len(entityDimensions), dtype=int)
    sampleVector = np.zeros(len(entityDimensions), dtype=int)

    for pair in sortedUserEntities:
        entity = pair[0]
        count = pair[1]
        np.put(userVector, entityDimensions[entity], count)

    for pair in sortedSampleEntities:
        entity = pair[0]
        count = pair[1]
        np.put(sampleVector, entityDimensions[entity], count)

    if random:
        np.save('data/{}-avg-user-vector'.format(screenName), userVector)
        np.save('data/{}-avg-sample-vector'.format(screenName), sampleVector)
    else:
        np.save('data/{}-user-vector'.format(screenName), userVector)
        np.save('data/{}-sample-vector'.format(screenName), sampleVector)

    similarity = cosine_similarity(userVector, sampleVector)
    similarityObject = {
        'similarity': similarity,
        'total_dimensions': len(entityDimensions)
    }
    if random:
        open('data/{}-avg-similarity.json'.format(screenName), 'w').write(json.dumps(similarityObject))
    else:
        open('data/{}-similarity.json'.format(screenName), 'w').write(json.dumps(similarityObject))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'get_entities_from_tweets':
            if len(sys.argv) > 2:
                if len(sys.argv) > 3:
                    get_entities_from_tweets(sys.argv[2], random=sys.argv[3])
                else:
                    get_entities_from_tweets(sys.argv[2])
            else:
                raise Exception('No screen name provied.')
        elif sys.argv[1] == 'build_entity_vectors':
            if len(sys.argv) > 2:
                if len(sys.argv) > 3:
                    build_entity_vectors(sys.argv[2], random=sys.argv[3])
                else:
                    build_entity_vectors(sys.argv[2])
            else:
                raise Exception('No screen name provied.')
        else:
            raise Exception('Invalid instruction.')
    else:
        raise Exception('No instruction provied.')

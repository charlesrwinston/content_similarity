from build_twitter_data import build_friends_list, get_network_tweets, get_user_tweets, get_random_sample_tweets
from entity_analysis import get_entities_from_tweets, build_entity_vectors
from twitter_methods import get_random_sample_users
import sys

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

def main(screenName):
    #numFollowers = build_friends_list(screenName)
    #get_user_tweets(screenName)
    #get_network_tweets(screenName)
    #get_random_sample_users(numFollowers)
    #get_random_sample_tweets(numFollowers)
    #get_entities_from_tweets(screenName, random=False)
    #build_entity_vectors(screenName, random=False)
    get_entities_from_tweets(screenName, random=True)
    build_entity_vectors(screenName, random=True)
    #get_entities_from_tweets(screenName, random=False, noScreenName=True)
    #build_entity_vectors(screenName, random=True, noScreenName=True)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        raise Exception('No screen name provied.')

import tweepy
import random
import time

from tweepy.streaming import StreamListener
from tweepy import Stream
import tweepy.api

VERB_PHRASES = [
    "i try",
    "i make",
    "i press",
    "i pull",
    "i hold",
    "you try",
    "you make",
    "you push",
    "you pull",
    "i jiggle",
    "you jiggle"
]
NUM_VERBS = len(VERB_PHRASES)


OBJECT_PHRASES = [
    "your leg",
    "my leg",
    "tongues",
    "a finger",
    "navel",
    "both arms",
    "dewlap",
    "lips",
    "my hair",
    "all over"
]
NUM_OBJS = len(OBJECT_PHRASES)


class StoreStatusTextListener(StreamListener):
    """ Records the text of streamed-in statuses in a list field """

    def __init__(self, api, limit=10000):
        self.texts = set()
        self.my_limit = limit
        self.api = api

    def on_status(self, status):
        self.texts.add(status.text)
        return len(self.texts) < self.my_limit

    def on_error(self, status):
        try:
            print "error", status
        except:
            print "unprintable error"


def get_config():
    with open('autopost.config', 'r') as infile:
        config = {}
        for line in infile:
            spline = line.split(" = ")
            config[spline[0]] = spline[1].strip()
    return config


def split_sentences(text):
    sents = []
    demarcations = set(".!?")
    sent = ""
    for ch in text:
        sent += ch
        if ch in demarcations:
            sents.append(sent)
            sent = ""
    sents.append(sent)
    return sents


def get_tweet(auth):
    api = tweepy.API(auth)
    #ears = StoreStatusTextListener(api, limit=3)

    verb = VERB_PHRASES[2]
    obj = OBJECT_PHRASES[2]

    verb = "i meant"
    obj = "leg"

    print verb, obj

    query = '"%s" "%s"' % (verb, obj)

    print "query:", query

    doug = tweepy.Cursor(api.search,
                        q=query,
                        #rpp=100,
                        result_type="recent",
                        include_entities=False,
                        lang="en").items()

    num_seen = 0

    while num_seen < 10000:
        try:
            tweet = doug.next()
            t = tweet.text
            if t.lower().startswith(verb):
                print t
            else:
                print "UGH"
            time.sleep(0.1)
            num_seen += 1
        except tweepy.TweepError:
            print " TAKIN A BREATHER "
            time.sleep(60*15)


    # try:
    #     stream = Stream(auth, ears, timeout=5.0)
    #     stream.filter(track=('"%s" "%s"' % (verb, obj)), languages=("en",))
    # except:
    #     print "Problem after", len(ears.texts)
    #
    # print "\n ____::______ \n".join(ears.texts)


def get_auth():
    config = get_config()

    ckey = config["CONSUMER_KEY"]
    csec = config["CONSUMER_SECRET"]
    akey = config["ACCESS_KEY"]
    asec = config["ACCESS_SECRET"]
    
    auth = tweepy.OAuthHandler(ckey, csec)
    auth.set_access_token(akey, asec)
    return auth


def main():
    auth = get_auth()
    get_tweet(auth)


if __name__ == "__main__":
    main()


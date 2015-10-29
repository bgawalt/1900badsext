import tweepy
import random

from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy.api import API

VERB_PHRASES = [
    "i try",
    "i make",
    "i press",
    "i hold",
    "you try",
    "you make",
    "you push",
    "i jiggle"
]


OBJECT_PHRASES = [
    "your leg",
    "my leg",
    "tongues",
    "a finger",
    "navel",
    "both arms",
    "dewlap",
    "lips"
]


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


def nltk_test():

    sents = nltk.tokenize.sent_tokenize(text)
    print " _:_:_:__:_".join(sents)


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



def get_api():
    config = get_config()

    ckey = config["CONSUMER_KEY"]
    csec = config["CONSUMER_SECRET"]
    akey = config["ACCESS_KEY"]
    asec = config["ACCESS_SECRET"]
    
    auth = tweepy.OAuthHandler(ckey, csec)
    auth.set_access_token(akey, asec)
    return tweepy.API(auth)


def main():
    #api = get_api()
    #
    # api.update_status(status="SEXT: I made a teddy bear out of your belly button lint.")
    text = "This is indeed a dark and most disturbing universe. If I had a nickel, then I could buy a motor-cycle. charging up a fitbit in my usb"
    print "\n\n..___..___..\n\n".join(split_sentences(text))


if __name__ == "__main__":
    main()


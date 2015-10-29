import tweepy
import random
import time

from tweepy.streaming import StreamListener
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
    "you jiggle",
    "i hurt",
    "you hurt"
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


def actual_pos(target, text):
    raw_pos = text.find(target)
    return raw_pos if raw_pos > -1 else len(text)


def clean_sent(sent):
    link_pos = actual_pos("http://", sent)
    slink_pos = actual_pos("https://", sent)
    hash_pos = actual_pos("#", sent)
    return sent[:min((link_pos, slink_pos, hash_pos))].replace("@", "[at]")


def get_tweet(auth, verb, obj):
    api = tweepy.API(auth)

    query = '"%s" "%s"' % (verb, obj)

    raw_tweets = tweepy.Cursor(api.search,
                               q=query,
                               result_type="recent",
                               include_entities=False,
                               lang="en").items()

    num_seen = 0
    best_len = 140
    best = None
    while num_seen < 10000:
        try:
            tweet = raw_tweets.next()
            t = tweet.text
            sents = [clean_sent(s) for s in split_sentences(t)
                     if len(s) < 134
                     and s.lower().startswith(verb)]
            if len(sents) > 0:
                ssents = sorted(sents, key=lambda s: len(s))
                if len(ssents[-1]) < best_len:
                    best = ssents[-1]
            time.sleep(0.1 + 0.0001*num_seen)
            num_seen += 1
        except tweepy.TweepError:
            print " TAKIN A BREATHER "
            time.sleep(60*15)
        except StopIteration:
            break
    if best is None:
        return best
    else:
        return "SEXT: " + best


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
    tweet = None
    while tweet is None:
        verb = VERB_PHRASES[random.randint(0, len(VERB_PHRASES) - 1)]
        obj = OBJECT_PHRASES[random.randint(0, len(OBJECT_PHRASES) - 1)]
        tweet = get_tweet(auth, verb, obj)
    print tweet
    api = tweepy.API(auth)
    api.update_status(status=tweet)


if __name__ == "__main__":
    main()


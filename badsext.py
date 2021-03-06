import tweepy
import random
import time
import sys

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
    "you hurt",
    "i toss",
    "you toss",
    "i shove",
    "you shove",
    "you move",
    "i move",
    "i wiggle",
    "you wiggle",
    "i twist",
    "you twist",
    "i yell",
    "you yell",
    "i shout",
    "you shout",
    "i grab",
    "you grab",
    "i need",
    "you need"
    "i want",
    "you want",
    "i give",
    "you give",
    "i take",
    "you take",
    "i lift",
    "you lift",
    "i find",
    "you find"
]
NUM_VERBS = len(VERB_PHRASES)


OBJECT_PHRASES = [
    "your leg",
    "my leg",
    "a finger",
    "all over",
    "mess",
    "oops",
    "toes",
    "knob",
    "hooter",
    "boob",
    "junk",
    "tears",
    "my drink",
    "your drink",
    "dumb",
    "phone",
    "book",
    "burp",
    "booty",
    "bootie",
    "facebook",
    "twitter",
    "tweet",
    "animal",
    "money",
    "elbow",
    "my arm",
    "your arm"
]
NUM_OBJS = len(OBJECT_PHRASES)

BAD_WORDS = [
    "nigg",
    "fag",
    "cunt",
    "bitch"
]


def get_config(filename):
    with open(filename, 'r') as infile:
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
    sents.append(sent.strip())
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
    while num_seen < 2000:
        try:
            tweet = raw_tweets.next()
            t = tweet.text
            clean_sents = [clean_sent(s) for s in split_sentences(t)]
            good_sents = [s for s in clean_sents
                          if len(s) < 90
                          and s.lower().startswith(verb)
                          and obj in s.lower()]
            if len(good_sents) > 0:
                ssents = sorted(good_sents, key=lambda s: len(s))
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
        for bad_word in BAD_WORDS:
            if bad_word in best:
                return None
        return "SEXT: " + best


def get_auth(config_file):
    config = get_config(config_file)

    ckey = config["CONSUMER_KEY"]
    csec = config["CONSUMER_SECRET"]
    akey = config["ACCESS_KEY"]
    asec = config["ACCESS_SECRET"]
    
    auth = tweepy.OAuthHandler(ckey, csec)
    auth.set_access_token(akey, asec)
    return auth


def main():
    auth = get_auth(sys.argv[1])
    tweet = None
    while tweet is None:

        verb = VERB_PHRASES[random.randint(0, len(VERB_PHRASES) - 1)]
        obj = OBJECT_PHRASES[random.randint(0, len(OBJECT_PHRASES) - 1)]

        print "\n\n", verb, obj, "\n\n"

        tweet = get_tweet(auth, verb, obj)
    try:
        print tweet
    except UnicodeEncodeError:
        print "[Trouble Printing Tweet]"
    api = tweepy.API(auth)
    api.update_status(status=tweet)


if __name__ == "__main__":
    main()


# 1-900-BAD-SEXT

My friends Maggie and Beth wanted a Twitter bot that could tweet out some bad
sexts. I bet that you could make some by just searching for already-existing
tweets containing a few key present-tense phrases and just drop "SEXT:" in
 front of it. These jokes literally write themselves.
 
Run it with

```
$ python badsext.py
```

and it will draw a random present-tense verb and an object and hunt for sexts
in the wild out on Twitter.
 
## Dependencies

You should make a file in the root of this repo called `autopost.config`, that
looks like:

```
CONSUMER_KEY = [the key] 
CONSUMER_SECRET = [the secret]
ACCESS_KEY = [the key]
ACCESS_SECRET = [the secret]
```

That's how it authenticates itself to Twitter for read and write requests, in 
case you wanna set up your own bot account.

Library wise, I think all it needs is Tweepy:

```
$ pip install tweepy
```

It hollers about `InsecurePlatformWarning` and how "a true SSLContext object 
is not available." I don't know how to fix that. It's preposterous.

import tweepy
import nltk


def get_config():
    with open('autopost.config', 'r') as infile:
        config = {}
        for line in infile:
            spline = line.split(" = ")
            config[spline[0]] = spline[1].strip()
    return config


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
    api = get_api()
    api.update_status(status="SEXT: I made a teddy bear out of your belly button lint.")


if __name__ == "__main__":
    main()


import twitter
import re
import random
import os


class TwitterContest():

    def __init__(self):
        """
        Init the twitter API.
        """
        consumer_key = 'xxxxx'
        consumer_secret = 'xxxxxxx'
        access_token = 'xxxxxxx'
        access_token_secret = 'xxxxx'

        self.api = twitter.Api(consumer_key=consumer_key,
                               consumer_secret=consumer_secret,
                               access_token_key=access_token,
                               access_token_secret=access_token_secret)

    def post_quote(self):
        """
        Post a random quote (avoid beeing flagged as spam...)
        """
        quote_index = random.randint(1, 76233)
        quote_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'quotes.txt')

        with open(quote_file) as f:
            for i, line in enumerate(f):
                if i == quote_index - 1:
                    return self.api.PostUpdates(line[0:139])

    def get_contest_tweets(self):
        """
        Get the tweets correponding to a contest
        """
        search_word = ['gagner', 'RT', '-DM']
        tweets = []
        test = self.api.GetSearch(' '.join(search_word), count=100, result_type='recent')

        # Remove RTs
        for tweet in test:
            p = re.compile(ur'^RT @', re.IGNORECASE)
            if not re.match(p, tweet.text):
                tweets.append(tweet)
            elif tweet.retweeted_status:
                if 'RT' in tweet.retweeted_status.text and 'gagner' in tweet.retweeted_status.text:
                    tweets.append(tweet.retweeted_status)

        return tweets

    def participate_in_contest(self, tweet):
        """
        Participate in the contest of the given tweet.

        Args:
            tweet: tweet correponding to the contest.
        """
        # Follow users in the tweet if necessary
        follow = ['follow', 'Follow', 'FOLLOW', 'suivez', 'Suivez']
        if any(f in tweet.text for f in follow):
            try:
                self.api.CreateFriendship(tweet.user.id)
            except:
                pass

            for user in tweet.user_mentions:
                try:
                    self.api.CreateFriendship(user.id)
                except:
                    pass

        # Favorite tweet if necessary
        fav = ['Fav', 'fav']
        if any(f in tweet.text for f in fav):
            try:
                self.api.CreateFavorite(id=tweet.id)
            except:
                pass

        # Retweet
        try:
            self.api.PostRetweet(tweet.id)
        except:
            pass

    def run(self):
        """
        Run detection of contest and participate.
        """
        tweets = self.get_contest_tweets()

        for tweet in tweets[0:10]:
            self.participate_in_contest(tweet)

        self.post_quote()

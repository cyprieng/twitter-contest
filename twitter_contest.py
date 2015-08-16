import twitter
import re


class TwitterContest():

    def __init__(self):
        """
        Init the twitter API.
        """
        consumer_key = 'LJjCS3u6Bi8BaiEGr7fTZnJgy'
        consumer_secret = 'eCedGJimotK6VmODo8BYxIU8Ma1WdEwKHKVkEC9coWDFrse3Ef'
        access_token = '3424055837-bfJzBwxRgFSqneW6gIRTbb7WIN07GAcriAWCAVa'
        access_token_secret = 'IeX9LBAxjCrP9h3MPRauMnTw5PxkGl5vMnT5E5h1dXKHr'

        self.api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token,
                      access_token_secret=access_token_secret)

    def get_contest_tweets(self):
        """
        Get the tweets correponding to a contest
        """
        search_word = ['gagner', 'RT']
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
        # Follow the user if necessary
        if 'follow' in tweet.text or 'Follow' in tweet.text or 'FOLLOW' in tweet.text or 'suivez' in tweet.text or 'Suivez' in tweet.text:
            try:
                self.api.CreateFriendship(tweet.user.id)
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

        for tweet in tweets:
            self.participate_in_contest(tweet)

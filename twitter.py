import os
import sys

import tweepy


class TwitterAPIClient:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

    def get_liked_tweets(self, user_id):
        """
        Get liked specified user's liked tweets.

        Parameters
        ----------
        user_id: int
            Twitter user ID.
        
        Returns
        -------
        liked_tweets: []tweepy.Tweet
            List of liked tweets.
        """
        liked_tweets = self.client.get_liked_tweets(user_id,
        user_auth=True,
        tweet_fields=['created_at'],
        max_results=30).data
        print(f'[*] number of liked_tweets: {len(liked_tweets)}')

        return liked_tweets

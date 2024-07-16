import tweepy
from app.config import TWITTER_BEARER_TOKEN

class TwitterService:
    def __init__(self):
        self.client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

    def get_tweet(self, tweet_id):
        try:
            tweet = self.client.get_tweet(
                tweet_id, 
                expansions=['author_id', 'attachments.media_keys'],
                tweet_fields=['created_at', 'text'],
                user_fields=['name', 'username', 'profile_image_url'],
                media_fields=['url', 'preview_image_url']
            )
            return tweet
        except tweepy.TweepError as e:
            raise Exception(f"Error fetching tweet: {str(e)}")
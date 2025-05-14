from requests_oauthlib import OAuth1Session

from unofficial_twitter_client.config import (
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)

oauth1 = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

def tweet_by_oauth(text, reply_to_id=None):
    """OAuthを使用してツイートを投稿"""
    data = {
        "text": text
    }
    if reply_to_id:
        data["reply"] = {
            "in_reply_to_tweet_id": reply_to_id
        }
    tweet_response = oauth1.post(
        "https://api.twitter.com/2/tweets",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    return tweet_response.json()

def retweet(screen_name, id):
    """リツイート"""
    text = f"https://x.com/{screen_name}/status/{id}"
    return tweet_by_oauth(text)

def quote_tweet(text, screen_name, id):
    """引用リツイート"""
    text = f"{text} https://x.com/{screen_name}/status/{id}"
    return tweet_by_oauth(text) 
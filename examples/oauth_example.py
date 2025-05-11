#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OAuth認証のシンプルな使用例
"""

from unofficial_twitter_client import oauth

# ツイートの投稿
tweet_response = oauth.tweet_by_oauth("Hello, World!")
print("ツイート投稿結果:", tweet_response)

# リツイート
retweet_response = oauth.retweet("elonmusk", "1685096284275802112")
print("リツイート結果:", retweet_response)

# 引用リツイート
quote_response = oauth.quote_tweet("これは引用リツイートです", "elonmusk", "1685096284275802112")
print("引用リツイート結果:", quote_response) 
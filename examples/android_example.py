#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Android APIのシンプルな使用例
"""

from unofficial_twitter_client import android

# 認証情報
oauth_token = "your_access_token"
token_secret = "your_access_token_secret"

# ツイートの作成
response = android.create_tweet("Hello, World!", oauth_token, token_secret)
print("ツイート作成結果:", response)

# 最新のタイムラインを取得
timeline = android.latest_timeline(oauth_token, token_secret)
print("タイムライン:", timeline)

# ユーザー情報の取得
user_info = android.get_user("44196397", oauth_token, token_secret)
print("ユーザー情報:", user_info)

# タイムラインの検索
search_results = android.search_timeline("python", oauth_token, token_secret)
print("検索結果:", search_results) 
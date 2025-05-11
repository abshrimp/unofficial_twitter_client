#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Web APIのシンプルな使用例
"""

from unofficial_twitter_client import web

# 認証情報
oauth_token = "your_access_token"
token_secret = "your_access_token_secret"

# タイムラインの検索
search_results = web.search_timeline_web("python", oauth_token, token_secret)
print("検索結果:", search_results)

# 最新のタイムラインを取得
timeline = web.latest_timeline_web(oauth_token, token_secret)
print("タイムライン:", timeline)

# ユーザー情報の取得
user_info = web.get_user_web("44196397", oauth_token, token_secret)
print("ユーザー情報:", user_info)

# ツイートの検索
search_results = web.search_tweets("#python", 5)
print("検索結果:", search_results)

# トレンドの取得
trends = web.get_trends()
print("トレンド:", trends) 
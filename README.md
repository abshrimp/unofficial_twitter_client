# Unofficial Twitter Client

⚠️ **重要** ⚠️

このパッケージは非公式のTwitterクライアントAPIパッケージです。Twitterの利用規約に違反する可能性があり、アカウントの制限やブロックを受ける可能性があります。このパッケージの使用は完全に自己責任となります。開発者はこのパッケージの使用によるいかなる問題についても責任を負いません。

Android API、Web API、Official APIの必要最低限のAPIをサポートしています。

## インストール

```bash
pip install unofficial-twitter-client
```

## 環境変数の設定

以下の環境変数を設定する必要があります：

### API認証情報
```bash
export CONSUMER_KEY="your_consumer_key"
export CONSUMER_SECRET="your_consumer_secret"
export ACCESS_TOKEN="your_access_token"
export ACCESS_TOKEN_SECRET="your_access_token_secret"
```

### Android認証情報
```bash
export ANDROID_CONSUMER_KEY="your_android_consumer_key"
export ANDROID_CONSUMER_SECRET="your_android_consumer_secret"
export KDT="your_kdt"
export X_TWITTER_CLIENT_ADID="your_adid"
export X_CLIENT_UUID="your_uuid"
export X_TWITTER_CLIENT_DEVICEID="your_deviceid"
```
取得手順は[こちらの記事](https://note.com/abshrimp/n/nadea974dba81)を参照してください。

## 使用例

⚠️ **注意**: 以下のコードは例示用です。実際の使用時は適切なエラーハンドリングとレート制限の考慮が必要です。

```python
from unofficial_twitter_client.api import android, web, oauth

# Android APIの使用例
response = android.create_tweet("Hello, World!", oauth_token, token_secret)

# Web APIの使用例
response = web.get_user_web("44196397", oauth_token, token_secret)

# oauth1の使用例
response = oauth.retweet("elonmusk", "44196397")
```

## 機能

### Android API
- ツイートの作成
- フォローの作成
- メンションの取得
- ツイートの検索
- ユーザー情報の取得
- 最新タイムラインの取得

### Web API
- Web APIを使用したタイムライン検索
- Web APIを使用した最新タイムラインの取得
- Web APIを使用したユーザー情報の取得

### Official API
- ツイートの作成
- リツイートの作成
- 引用リツイートの作成

## 使用上の注意

- このパッケージは非公式であり、Twitterの利用規約に違反する可能性があります
- アカウントの制限やブロックを受ける可能性があります
- 大量のリクエストは避けてください
- スパム行為や迷惑行為に使用しないでください
- このパッケージの使用は完全に自己責任となります
- 開発者はこのパッケージの使用によるいかなる問題についても責任を負いません

## ライセンス

MITライセンス 
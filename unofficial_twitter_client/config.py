import os

def get_required_env(key):
    """Get required environment variable and raise error if not set"""
    value = os.environ.get(key)
    if value is None:
        raise ValueError(f"Environment variable {key} is not set. Please set it using:\nexport {key}=your_value")
    return value

# API認証情報
CONSUMER_KEY = get_required_env("CONSUMER_KEY")
CONSUMER_SECRET = get_required_env("CONSUMER_SECRET")
ACCESS_TOKEN = get_required_env("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = get_required_env("ACCESS_TOKEN_SECRET")

# Android認証情報
consumer_key = get_required_env("ANDROID_CONSUMER_KEY")
consumer_secret = get_required_env("ANDROID_CONSUMER_SECRET")
kdt = get_required_env("KDT")
x_twitter_client_adid = get_required_env("X_TWITTER_CLIENT_ADID")
x_client_uuid = get_required_env("X_CLIENT_UUID")
x_twitter_client_deviceid = get_required_env("X_TWITTER_CLIENT_DEVICEID") 
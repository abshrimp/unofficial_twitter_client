"""
Unofficial Twitter Client API
"""

from . import android, web, oauth
from .config import (
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET,
    consumer_key, consumer_secret, kdt, x_twitter_client_adid,
    x_client_uuid, x_twitter_client_deviceid
)

__version__ = "0.1.0" 
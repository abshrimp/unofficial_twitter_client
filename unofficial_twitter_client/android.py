import base64
import gzip
import hashlib
import hmac
import io
import json
import random
import time
import urllib.parse
import requests

from unofficial_twitter_client.config import (
    consumer_key, consumer_secret, kdt, x_twitter_client_adid,
    x_client_uuid, x_twitter_client_deviceid
)

def sendAndroid(url, params, oauth_token, token_secret, http_method="GET"):
    """Android APIへのリクエストを送信"""
    try:
        host = "api.twitter.com"
        url = "https://" + host + url

        oauth_nonce = "".join([str(random.randint(0, 9)) for _ in range(32)])
        oauth_timestamp = str(int(time.time()))
        parameters = {
            "oauth_consumer_key": consumer_key,
            "oauth_token": oauth_token,
            "oauth_signature_method": "HMAC-SHA1",
            "oauth_timestamp": oauth_timestamp,
            "oauth_nonce": oauth_nonce,
            "oauth_version": "1.0",
        }
        sign_params = parameters if http_method == "POST" and "graphql" in url else {**parameters, **params}
        parameter_string = "&".join(f"{k}={v}" for k, v in sorted(sign_params.items()))
        signature_base_string = f"{http_method}&{urllib.parse.quote(url, '')}&{urllib.parse.quote(parameter_string, '')}"
        signing_key = f"{consumer_secret}&{token_secret}"
        digest = hmac.new(signing_key.encode(), signature_base_string.encode(), hashlib.sha1).digest()
        oauth_signature = base64.b64encode(digest).decode()
        parameters["oauth_signature"] = oauth_signature

        headers = {
            "Host": host,
            "Timezone": "Asia/Tokyo",
            "Os-Security-Patch-Level": "2021-08-05",
            "Optimize-Body": "true",
            "Accept": "application/json",
            "X-Twitter-Client": "TwitterAndroid",
            "X-Attest-Token": "no_token",
            "User-Agent": "TwitterAndroid/10.53.2-release.0 (310532000-r-0)",
            "X-Twitter-Client-Adid": x_twitter_client_adid,
            "X-Twitter-Client-Language": "en-US",
            "X-Client-Uuid": x_client_uuid,
            "X-Twitter-Client-Deviceid": x_twitter_client_deviceid,
            "Authorization": f'OAuth realm="http://api.twitter.com/", ' + ", ".join(f'{urllib.parse.quote(k)}="{urllib.parse.quote(v)}"' for k, v in parameters.items()),
            "X-Twitter-Client-Version": "10.53.2-release.0",
            "Cache-Control": "no-store",
            "X-Twitter-Active-User": "yes",
            "X-Twitter-Api-Version": "5",
            "Kdt": kdt,
            "X-Twitter-Client-Limit-Ad-Tracking": "0",
            "Accept-Language": "en-US",
            "X-Twitter-Client-Flavor": "",
        }

        if http_method == "GET":
            url += "?"
            for param in params:
                url += param + "=" + params[param] + "&"
            url = url[:-1]
            response = requests.get(url, headers=headers)
        else:
            if "graphql" in url:
                json_bytes = json.dumps(params).encode("utf-8")
                gzip_buffer = io.BytesIO()
                with gzip.GzipFile(fileobj=gzip_buffer, mode="wb") as f:
                    f.write(json_bytes)
                gzip_data = gzip_buffer.getvalue()
                post_headers = {
                    "Accept-Encoding": "gzip, deflate, br",
                    "Content-Encoding": "gzip",
                    "Content-Type": "application/json",
                }
                headers = {**headers, **post_headers}
                response = requests.post(url, headers=headers, data=gzip_data)
            else:
                url += "?"
                for param in params:
                    url += f'{param}={params[param]}&'
                url = url[:-1]
                post_headers = {"Content-Type": "application/x-www-form-urlencoded"}
                headers = {**headers, **post_headers}
                response = requests.post(url, headers=headers)

        return response.json()
    except Exception as e:
        return {"errors": str(e)}

def create_tweet(text, oauth_token, token_secret, rep_id=None):
    """ツイートを作成"""
    reply_str = f',"reply":{{"exclude_reply_user_ids":[],"in_reply_to_tweet_id":{rep_id}}}' if rep_id is not None else ""
    json_data = {
        "features": '{"longform_notetweets_inline_media_enabled":true,"super_follow_badge_privacy_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"super_follow_user_api_enabled":true,"super_follow_tweet_api_enabled":true,"articles_api_enabled":true,"android_graphql_skip_api_media_color_palette":true,"creator_subscriptions_tweet_preview_api_enabled":true,"freedom_of_speech_not_reach_fetch_enabled":true,"tweetypie_unmention_optimization_enabled":true,"longform_notetweets_consumption_enabled":true,"subscriptions_verification_info_enabled":true,"blue_business_profile_image_shape_enabled":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"immersive_video_status_linkable_timestamps":true,"super_follow_exclusive_tweet_notifications_enabled":true}',
        "variables": f'{{"nullcast":false,"includeTweetImpression":true,"includeHasBirdwatchNotes":false,"includeEditPerspective":false,"includeEditControl":true,"includeCommunityTweetRelationship":false{reply_str},"includeTweetVisibilityNudge":true,"tweet_text":"{text}"}}',
    }
    return sendAndroid("/graphql/B8zcLvy-DN84y11pB2NObA/CreateTweet", json_data, oauth_token, token_secret, "POST")

def create_follow(id, oauth_token, token_secret):
    """フォローを作成"""
    payload = {
        "ext": "mediaRestrictions%2CaltText%2CmediaStats%2CmediaColor%2Cinfo360%2ChighlightedLabel%2CunmentionInfo%2CeditControl%2CpreviousCounts%2ClimitedActionResults%2CsuperFollowMetadata",
        "send_error_codes": "true",
        "user_id": id,
        "handles_challenges": "1",
    }
    return sendAndroid("/1.1/friendships/create.json", payload, oauth_token, token_secret, "POST")

def get_mentions(oauth_token, token_secret, cursor=None):
    """メンションを取得"""
    params = {
        "earned": "true",
        "include_ext_is_blue_verified": "true",
        "include_ext_verified_type": "true",
        "include_ext_profile_image_shape": "true",
        "include_ext_is_tweet_translatable": "true",
        "include_entities": "true",
        "include_cards": "true",
        "cards_platform": "Android-12",
        "include_carousels": "true",
        "ext": "mediaRestrictions%2CaltText%2CmediaStats%2CmediaColor%2Cinfo360%2ChighlightedLabel%2CunmentionInfo%2CeditControl%2CpreviousCounts%2ClimitedActionResults%2CsuperFollowMetadata",
        "include_media_features": "true",
        "include_blocking": "true",
        "include_blocked_by": "true",
        "include_quote_count": "true",
        "include_ext_previous_counts": "true",
        "include_ext_limited_action_results": "true",
        "tweet_mode": "extended",
        "include_composer_source": "true",
        "include_ext_media_availability": "true",
        "include_ext_edit_control": "true",
        "include_reply_count": "true",
        "include_ext_sensitive_media_warning": "true",
        "include_ext_views": "true",
        "simple_quoted_tweet": "true",
        "include_ext_birdwatch_pivot": "true",
        "include_user_entities": "true",
        "include_profile_interstitial_type": "true",
        "include_ext_professional": "true",
        "include_viewer_quick_promote_eligibility": "true",
        "include_ext_has_nft_avatar": "true",
    }
    if cursor is not None:
        params["cursor"] = cursor
    return sendAndroid("/2/notifications/mentions.json", params, oauth_token, token_secret)

def search_timeline(text, oauth_token, token_secret, cursor=None):
    """タイムラインを検索"""
    cursor_param = f"cursor%22%3A%22{cursor}%22%2C%22" if cursor is not None else ""
    params = {
        "variables": f'%7B%22{cursor_param}includeTweetImpression%22%3Atrue%2C%22query_source%22%3A%22typed_query%22%2C%22includeHasBirdwatchNotes%22%3Afalse%2C%22includeEditPerspective%22%3Afalse%2C%22includeEditControl%22%3Atrue%2C%22query%22%3A%22{urllib.parse.quote(text)}%22%2C%22timeline_type%22%3A%22Latest%22%7D',
        "features": "%7B%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22super_follow_badge_privacy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22super_follow_user_api_enabled%22%3Atrue%2C%22unified_cards_ad_metadata_container_dynamic_card_content_query_enabled%22%3Atrue%2C%22super_follow_tweet_api_enabled%22%3Atrue%2C%22articles_api_enabled%22%3Atrue%2C%22android_graphql_skip_api_media_color_palette%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22subscriptions_verification_info_enabled%22%3Atrue%2C%22blue_business_profile_image_shape_enabled%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22immersive_video_status_linkable_timestamps%22%3Atrue%2C%22super_follow_exclusive_tweet_notifications_enabled%22%3Atrue%7D",
    }
    return sendAndroid("/graphql/4NfkwyiViTLQw7ZcJmxtKg/SearchTimeline", params, oauth_token, token_secret)

def get_user(id, oauth_token, token_secret):
    """ユーザー情報を取得"""
    params = {
        "variables": f"%7B%22include_smart_block%22%3Atrue%2C%22includeTweetImpression%22%3Atrue%2C%22include_profile_info%22%3Atrue%2C%22includeTranslatableProfile%22%3Atrue%2C%22includeHasBirdwatchNotes%22%3Afalse%2C%22include_tipjar%22%3Atrue%2C%22includeEditPerspective%22%3Afalse%2C%22include_reply_device_follow%22%3Atrue%2C%22includeEditControl%22%3Atrue%2C%22include_verified_phone_status%22%3Afalse%2C%22rest_id%22%3A%22{id}%22%7D",
        "features": "%7B%22verified_phone_label_enabled%22%3Afalse%2C%22super_follow_badge_privacy_enabled%22%3Atrue%2C%22subscriptions_verification_info_enabled%22%3Atrue%2C%22super_follow_user_api_enabled%22%3Atrue%2C%22blue_business_profile_image_shape_enabled%22%3Atrue%2C%22immersive_video_status_linkable_timestamps%22%3Atrue%2C%22super_follow_exclusive_tweet_notifications_enabled%22%3Atrue%7D",
    }
    return sendAndroid("/graphql/iOA9WG49OYDPdIvJi4K7Yw/UserResultByIdQuery", params, oauth_token, token_secret)

def latest_timeline(oauth_token, token_secret, cursor=None):
    """最新のタイムラインを取得"""
    cursor_param = f"cursor%22%3A%22{cursor}%22%2C%22" if cursor is not None else ""
    params = {
        "variables": f"%7B%22{cursor_param}includeTweetImpression%22%3Atrue%2C%22request_context%22%3A%22ptr%22%2C%22includeHasBirdwatchNotes%22%3Afalse%2C%22includeEditPerspective%22%3Afalse%2C%22includeEditControl%22%3Atrue%2C%22count%22%3A100%2C%22includeTweetVisibilityNudge%22%3Atrue%2C%22autoplay_enabled%22%3Atrue%7D",
        "features": "%7B%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22super_follow_badge_privacy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22super_follow_user_api_enabled%22%3Atrue%2C%22unified_cards_ad_metadata_container_dynamic_card_content_query_enabled%22%3Atrue%2C%22super_follow_tweet_api_enabled%22%3Atrue%2C%22articles_api_enabled%22%3Atrue%2C%22android_graphql_skip_api_media_color_palette%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22subscriptions_verification_info_enabled%22%3Atrue%2C%22blue_business_profile_image_shape_enabled%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22immersive_video_status_linkable_timestamps%22%3Atrue%2C%22super_follow_exclusive_tweet_notifications_enabled%22%3Atrue%7D",
    }
    return sendAndroid("/graphql/fk-JW3tHUsfC6mBcx0ea3Q/HomeTimelineLatest", params, oauth_token, token_secret) 
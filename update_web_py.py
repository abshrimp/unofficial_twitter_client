import chromedriver_binary
import sys, time, json, urllib.parse, tempfile, shutil, os
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from typing import Union

file_path = "unofficial_twitter_client/web.py"

AUTH_TOKEN_COOKIE = {
    'name': 'auth_token',
    'value': os.environ["X_TOKEN"],
    'domain': '.x.com',
    'path': '/',
    'secure': True,
    'httpOnly': True
}

def get_api_parameters_with_cookie(driver, target_url: str, api_base_path: str, api_name: str) -> Union[dict, None]:

    driver.get(target_url)
    time.sleep(10)

    if target_url == "https://x.com/home":
        driver.execute_script("document.querySelectorAll('a[href=\"/home\"]')[3].click();")
        time.sleep(10)

    for request in driver.requests:
        if api_base_path in request.url and api_name in request.url:
            try:
                after_base_path = request.url.split(api_base_path, 1)[1]
                before_query = after_base_path.split('?', 1)[0]
                
                query_id = None
                if before_query.endswith(f'/{api_name}'):
                    query_id_segment = before_query.rsplit(f'/{api_name}', 1)[0]
                    query_id = query_id_segment.strip('/')
                
                if query_id:
                    params_from_request = {}
                    if request.method == 'POST':
                        try:
                            body = request.body.decode('utf-8')
                            params_from_request = json.loads(body)
                        except json.JSONDecodeError:
                            pass
                        except Exception:
                            pass
                    elif request.method == 'GET':
                        for key, values in request.params.items():
                            if isinstance(values, list) and values:
                                params_from_request[key] = values[0]
                            else:
                                params_from_request[key] = values

                    final_output_data = {}
                    
                    for key_name in ['variables', 'features', 'fieldToggles']:
                        if key_name in params_from_request:
                            final_output_data[key_name] = urllib.parse.quote(str(params_from_request[key_name]).replace(" ", ""))

                    # for key, value in params_from_request.items():
                    #     if key not in ['variables', 'features', 'fieldToggles']:
                    #         final_output_data[key] = value

                    return query_id, final_output_data
            except IndexError:
                pass
            except Exception:
                pass

    return None, None


def main():

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')

    temp_profile = tempfile.mkdtemp()
    shutil.rmtree(temp_profile, ignore_errors=True)
    os.makedirs(temp_profile, exist_ok=True)
    options.add_argument(f'--user-data-dir={temp_profile}')

    driver = webdriver.Chrome(options = options)
    driver.set_window_size(1920,1080)
    driver.get("https://x.com")
    driver.add_cookie(AUTH_TOKEN_COOKIE)
    driver.refresh()
    time.sleep(10)

    GRAPHQL_BASE_PATH = "/i/api/graphql/"

    output = []

    id, data = get_api_parameters_with_cookie(driver, "https://x.com/search?q=abababab&src=typed_query&f=live", GRAPHQL_BASE_PATH, "SearchTimeline")
    output.append(str(data).replace("'variables': ", "'variables': f").replace("abababab", "{urllib.parse.quote(text)}").replace("querySource", "{cursor_param}querySource"))
    output.append(id)

    id, data = get_api_parameters_with_cookie(driver, "https://x.com/home", GRAPHQL_BASE_PATH, "HomeLatestTimeline")
    output.append(str(data).replace("'variables': ", "'variables': f").replace("includePromotedContent", "{cursor_param}includePromotedContent"))
    output.append(id)


    id, data = get_api_parameters_with_cookie(driver, "https://x.com/i/user/111111", GRAPHQL_BASE_PATH, "UserByRestId")
    output.append(str(data).replace("'variables': ", "'variables': f").replace("111111", "{id}"))
    output.append(id)


    id, data = get_api_parameters_with_cookie(driver, "https://x.com/notifications/mentions", GRAPHQL_BASE_PATH, "NotificationsTimeline")
    output.append(str(data).replace("'variables': ", "'variables': f").replace("count%22", "{cursor_param}count%22"))
    output.append(id)


    id, data = get_api_parameters_with_cookie(driver, "https://x.com/Rank334/status/1899425077894259116", GRAPHQL_BASE_PATH, "TweetDetail")
    output.append(str(data).replace("'variables': ", "'variables': f").replace("1899425077894259116", "{id}"))
    output.append(id)


    driver.quit()



    code_string = """import urllib.parse

from unofficial_twitter_client.android import sendAndroid

def search_timeline_web(text, oauth_token, token_secret, cursor=None):
    \"\"\"Web APIを使用してタイムラインを検索\"\"\"
    cursor_param = f"cursor%22%3A%22{cursor}%22%2C%22" if cursor is not None else ""
    params = """ + output[0] + """
    return sendAndroid('/graphql/""" + output[1] + """/SearchTimeline', params, oauth_token, token_secret)

def latest_timeline_web(oauth_token, token_secret, cursor=None):
    \"\"\"Web APIを使用して最新のタイムラインを取得\"\"\"
    cursor_param = f"cursor%22%3A%22{cursor}%22%2C%22" if cursor is not None else ""
    params = """ + output[2] + """
    return sendAndroid('/graphql/""" + output[3] + """/HomeLatestTimeline', params, oauth_token, token_secret)

#https://x.com/i/user/1
def get_user_web(id, oauth_token, token_secret):
    \"\"\"Web APIを使用してユーザー情報を取得\"\"\"
    params = """ + output[4] + """
    return sendAndroid('/graphql/""" + output[5] + """/UserByRestId', params, oauth_token, token_secret)

def get_mentions_web(oauth_token, token_secret, cursor=None):
    \"\"\"Web APIを使用してメンションを取得\"\"\"
    cursor_param = f"cursor%22%3A%22{cursor}%22%2C%22" if cursor is not None else ""
    params = """ + output[6] + """
    return sendAndroid('/graphql/""" + output[7] + """/NotificationsTimeline', params, oauth_token, token_secret)

def get_tweet(id, oauth_token, token_secret):
    \"\"\"Web APIを使用してツイートを取得\"\"\"
    params = """ + output[8] + """
    return sendAndroid('/graphql/""" + output[9] + """/TweetDetail', params, oauth_token, token_secret)
"""

    print(code_string)

    try:
        with open(file_path, 'w', encoding='utf-8') as outfile:
            outfile.write(code_string)

    except Exception as e:
        print(f"エラーが発生しました: {e}", file=sys.stderr)
        sys.exit(1)

main()

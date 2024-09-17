import requests

url = "https://api.x.com/1.1/onboarding/task.json?flow_name=login"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:<version>) Gecko/20100101 Firefox/<version>",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Content-Type": "application/json",
    "Referer": "https://x.com/",
    "X-Guest-Token": "<guest-token>",
    "X-Twitter-Client-Language": "en",
    "X-Twitter-Active-User": "yes",
    "X-Client-Transaction-ID": "<transaction-id>",
    "Origin": "https://x.com",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Authorization": "Bearer <authorization-token>",
    "Cookie": "guest_id_marketing=<guest_id_marketing>; guest_id_ads=<guest_id_ads>; personalization_id=<personalization_id>; night_mode=2; kdt=<kdt-token>; dnt=1; att=<att-token>; guest_id=<guest_id>; gt=<gt-token>; _twitter_sess=<session-data>"
}

payload = {
    "input_flow_data": {
        "flow_context": {
            "debug_overrides": {},
            "start_location": {
                "location": "splash_screen"
            }
        }
    },
    "subtask_versions": {
        "action_list": 2,
        "alert_dialog": 1,
        "app_download_cta": 1,
        "check_logged_in_account": 1,
        "choice_selection": 3,
        "contacts_live_sync_permission_prompt": 0,
        "cta": 7,
        "email_verification": 2,
        "end_flow": 1,
        "enter_date": 1,
        "enter_email": 2,
        "enter_password": 5,
        "enter_phone": 2,
        "enter_recaptcha": 1,
        "enter_text": 5,
        "enter_username": 2,
        "generic_urt": 3,
        "in_app_notification": 1,
        "interest_picker": 3,
        "js_instrumentation": 1,
        "menu_dialog": 1,
        "notifications_permission_prompt": 2,
        "open_account": 2,
        "open_home_timeline": 1,
        "open_link": 1,
        "privacy_options": 1,
        "security_key": 3,
        "select_avatar": 4,
        "select_banner": 2,
        "settings_list": 7,
        "show_code": 1,
        "sign_up": 2,
        "sign_up_review": 4,
        "tweet_selection_urt": 1,
        "update_users": 1,
        "upload_media": 1,
        "user_recommendations_list": 4,
        "user_recommendations_urt": 1,
        "wait_spinner": 3,
        "web_modal": 1
    }
}

response = requests.post(url, headers=headers, json=payload)

print(response.status_code)
print(response.text)

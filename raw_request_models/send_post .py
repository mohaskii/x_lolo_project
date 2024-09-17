import requests

url = "https://<hostname>/i/api/graphql/<queryId>/CreateTweet"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:<version>) Gecko/20100101 Firefox/<version>",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Content-Type": "application/json",
    "Referer": "https://<hostname>/home",
    # "X-Client-UUID": "<client-uuid>",
    "X-Twitter-Auth-Type": "OAuth2Session",
    "X-CSRF-Token": "<csrf-token>",
    "X-Twitter-Client-Language": "en",
    "X-Twitter-Active-User": "yes",
    # "X-Client-Transaction-ID": "<transaction-id>",
    "Origin": "https://<hostname>",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Authorization": "Bearer <authorization-token>",
    "Cookie": "ct0=<csrf-token>; auth_token=<auth-token>"
}

payload = {
    "variables": {
        "tweet_text": "<tweet_text>",
        "dark_request": False,
        "media": {
            "media_entities": [],
            "possibly_sensitive": False
        },
        "semantic_annotation_ids": [],
        "disallowed_reply_options": None
    },
    "features": {
        "communities_web_enable_tweet_community_results_fetch": True,
        "c9s_tweet_anatomy_moderator_badge_enabled": True,
        "responsive_web_edit_tweet_api_enabled": True,
        "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
        "view_counts_everywhere_api_enabled": True,
        "longform_notetweets_consumption_enabled": True,
        "responsive_web_twitter_article_tweet_consumption_enabled": True,
        "tweet_awards_web_tipping_enabled": False,
        "creator_subscriptions_quote_tweet_preview_enabled": False,
        "longform_notetweets_rich_text_read_enabled": True,
        "longform_notetweets_inline_media_enabled": True,
        "articles_preview_enabled": True,
        "rweb_video_timestamps_enabled": True,
        "rweb_tipjar_consumption_enabled": True,
        "responsive_web_graphql_exclude_directive_enabled": True,
        "verified_phone_label_enabled": False,
        "freedom_of_speech_not_reach_fetch_enabled": True,
        "standardized_nudges_misinfo": True,
        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
        "responsive_web_graphql_timeline_navigation_enabled": True,
        "responsive_web_enhance_cards_enabled": False
    },
    "queryId": "<queryId>"
}

response = requests.post(url, headers=headers, json=payload)

print(response.status_code)
print(response.text)

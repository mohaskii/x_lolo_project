from http.cookies import SimpleCookie
from .cookie import Cookie
import json


# default user agent
USERS_AGENT = "linux_Chrome"

USERS_AGENTS = {
    "linux_Firefox": "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
    "linux_Chrome": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    # Need some contributions for more users agents approved by Twitter
}

GET_TOK_REQUEST_COMPONENTS = {
    "headers": {
        "User-Agent": USERS_AGENTS[USERS_AGENT],
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "Sec-GPC": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Priority": "u=0,i",
        "Te": "trailers"
    },
    "url": "https://x.com/"
}


def g(tok: str) -> str:
    return f"https://twitter.com/x/migrate?tok={tok}"


GET_IDS_COOKIES_REQUEST_COMPONENTS = {
    "headers": {
        "User-Agent": USERS_AGENTS[USERS_AGENT],
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "Sec-GPC": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Priority": "u=0,i",
        "Te": "trailers"
    },
    "url": g
}


def generate_x_guest_token_header(cookies: Cookie) -> dict:
    return {
        "User-Agent": USERS_AGENTS[USERS_AGENT],
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://twitter.com/",
        "DNT": "1",
        "Sec-GPC": "1",
        "Cookie": cookies.encode(),
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Priority": "u=0,i",
        "Te": "trailers"
    }


GET_X_GUEST_TOKEN_REQUEST_COMPONENTS = {
    "headers": generate_x_guest_token_header,
    "url": "https://x.com/?mx=2"
}


def generate_x_guest_flow_header(cookie: Cookie, guest_token: str) -> dict:
    return {
        "User-Agent": USERS_AGENTS[USERS_AGENT],
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Content-Type": "application/json",
        "Referer": "https://x.com/",
        "X-Guest-Token": guest_token,
        "X-Twitter-Client-Language": "en",
        "X-Twitter-Active-User": "yes",
        "Origin": "https://x.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        # Don't think I made a mistake by putting this token here 😂 It's hard-coded by Twitter developers."
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "Cookie": cookie.encode()
    }


GET_FLOW_TOKEN_REQUEST_COMPONENTS = {
    "headers": generate_x_guest_flow_header,
    "payload": {
        "input_flow_data": {
            "flow_context": {
                "debug_overrides": {},
                "start_location": {
                    "location": "splash_screen"
                }
            }
        },
        # to be honest idk tf is going on here
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
            # "phone_verification": 4
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
    },
    "url": "https://api.x.com/1.1/onboarding/task.json?flow_name=login"
}


def generate_payload_for_pnlr(flow_token: str):
    return {
        "flow_token": f"{flow_token}0",
        "subtask_inputs": [
            {
                "js_instrumentation": {
                    "link": "next_link",
                    "response": "{\"rf\":{\"a0d88821990b93ed8b88c8f2cec1f6a55523bb3cd3a2e129ff38e4a2aafcccdc\":-191,\"d44f82f7bef967329ae54476dba7b7666c7f50ae9601553cfb73cca45aef4e0f\":-150,\"f729d9835742998b799a599791853043fca0e8149a5f524cd0c602bcb85e1823\":-41,\"af92f7e5e499ec661c124ded9d5f2bbf1a16aec65dbc00ace19445e1cec4f4fb\":-46},\"s\":\"_MvpLYcsh1W_k0dKBFD9czEMmK2Q7HjnizH5MQ-k7bsNT56kdpL0z9S7yTRKcLZbguhVQ9Y7vuxMgrMpbQDN4UeYLXpbGQbtlpZGxrdMulSQbNVMCCuiBWSSkPppPUYZKCRyd9SE_FydBp3GjqoT87eGbynjpJvHjyup81NjkNmZwkxchT-Q6maE0mi-By_f__KIvin1FGLWDjnD-W56TU4GR_H2nxpZ2Kyjt849xyWTp-4id2H6tbU2K_R4fSv5-1l7xO9vmuvUwRf_IHzPU7tWP-bNvBkjkmC9DF1dXa1AwHO-eQiBQ5gsFegJRZpWuzjZA549NJZ3a-9r0mDBSgAAAZHzhFAV\"}"
                },
                "subtask_id": "LoginJsInstrumentationSubtask"
            }
        ]
    }


def generate_payload_for_sur(flow_token: str, username: str):
    return {
        "flow_token": f"{flow_token}1",
        "subtask_inputs": [
            {
                "subtask_id": "LoginEnterUserIdentifierSSO",
                "settings_list": {
                    "setting_responses": [
                        {
                            "key": "user_identifier",
                            "response_data": {
                                "text_data": {
                                    "result": username
                                }
                            }
                        }
                    ],
                    "link": "next_link"
                }
            }
        ]
    }


def generate_payload_for_spr(flow_token: str, password: str):
    return {
        "flow_token": f"{flow_token}7",
        "subtask_inputs": [
            {
                "subtask_id": "LoginEnterPassword",
                "enter_password": {
                    "password": password,
                    "link": "next_link"
                }
            }
        ]
    }


PASS_NEXT_LINK_REQUEST_COMPONENTS = {
    "headers": GET_FLOW_TOKEN_REQUEST_COMPONENTS["headers"],
    "url": "https://api.x.com/1.1/onboarding/task.json",
    "payload": generate_payload_for_pnlr
}

SUBMIT_USERNAME_REQUEST_COMPONENTS = {
    "headers": GET_FLOW_TOKEN_REQUEST_COMPONENTS["headers"],
    "url": "https://api.x.com/1.1/onboarding/task.json",
    "payload": generate_payload_for_sur
}

SUBMIT_PASSWORD_REQUEST_COMPONENTS = {
    "headers": GET_FLOW_TOKEN_REQUEST_COMPONENTS["headers"],
    "url": "https://api.x.com/1.1/onboarding/task.json",
    "payload": generate_payload_for_spr
}


def generate_valid_session_headers(sess) -> dict:
    return {
        "User-Agent": USERS_AGENTS[USERS_AGENT],
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Content-Type": "application/json",
        "Referer": "https://x.com/home",
        "X-Twitter-Auth-Type": "OAuth2Session",
        "X-CSRF-Token": sess.x_csrf_token,
        "X-Twitter-Client-Language": "en",
        "X-Twitter-Active-User": "yes",
        "Origin": "https://x.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "Cookie": sess.cookies.encode(),
        "TE": "trailers"
    }


def generate_payload_for_text_post(text: str):
    return {
        "variables": {
            "tweet_text": text,
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
    }


TEXT_POST_REQUEST_COMPONENTS = {
    "url": "https://x.com/i/api/graphql/xT36w0XM3A8jDynpkram2A/CreateTweet",
    "headers": generate_valid_session_headers,
    "payload": generate_payload_for_text_post
}



def a(v):
    return {
        "variables": json.dumps({
            "screen_name": v,
            "withSafetyModeUserFields": True
        }),
        "features": json.dumps({
            "hidden_profile_subscriptions_enabled": True,
            "rweb_tipjar_consumption_enabled": True,
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": False,
            "subscriptions_verification_info_is_identity_verified_enabled": True,
            "subscriptions_verification_info_verified_since_enabled": True,
            "highlights_tweets_tab_ui_enabled": True,
            "responsive_web_twitter_article_notes_tab_enabled": True,
            "subscriptions_feature_can_gift_premium": True,
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "responsive_web_graphql_timeline_navigation_enabled": True
        }),
        "fieldToggles": json.dumps({
            "withAuxiliaryUserLabels": False
        })
    }


def b(user_id, cursor =  None):
    return {
        "variables": json.dumps({
            "count" : 30,
            "cursor": cursor,
            "userId": user_id,
            "includePromotedContent": False,
            "withQuickPromoteEligibilityTweetFields": True,
            "withVoice": True,
            "withV2Timeline": True
        }),
        "features": json.dumps({
            "rweb_tipjar_consumption_enabled": True,
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": False,
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "communities_web_enable_tweet_community_results_fetch": True,
            "c9s_tweet_anatomy_moderator_badge_enabled": True,
            "articles_preview_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "responsive_web_twitter_article_tweet_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": False,
            "creator_subscriptions_quote_tweet_preview_enabled": False,
            "freedom_of_speech_not_reach_fetch_enabled": True,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
            "rweb_video_timestamps_enabled": True,
            "longform_notetweets_rich_text_read_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "responsive_web_enhance_cards_enabled": False
        }),
        "fieldToggles": json.dumps({
            "withArticlePlainText": False
        })
    }


GRAPHQL_QUERIES = {
    "base_url": " https://x.com/i/api/graphql/",
    "get_user_by_username": {
        "query_id": "Yka-W8dz7RaEuQNkroPkYw/UserByScreenName",
        "query": a
    },
    "me": {
        "query_id": "HC-1ZetsBT1HKVUOvnLE8Q/Viewer",
        "query": {
            "variables": '{"withCommunitiesMemberships":true}',
            "features": '{"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}',
            "fieldToggles": '{"isDelegate":false,"withAuxiliaryUserLabels":false}'
        }
    },
    "get_user_posts": {
        "query_id": "E3opETHurmVJflFsUBVuUQ/UserTweets",
        "query": b,
    },
    "get_next_user_posts_paginator": {
        "query_id": "E3opETHurmVJflFsUBVuUQ/UserTweets",
        "query": b,
    }

}

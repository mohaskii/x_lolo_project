# `x_lolo` Documentation

The `x_lolo` package includes several classes that manage interactions with X (formerly Twitter) platform through its unofficial API. Each class provides specific methods for performing various Twitter operations like authentication, posting content, user interactions, and data retrieval.

---

## Session

Session is a class dedicated to managing user sessions for interacting with the X (formerly Twitter) API. It provides methods for authentication, posting content, and retrieving user data.

### Methods

| Method                    | Arguments                                              | Return Value            | Description                                                                    |
|--------------------------|--------------------------------------------------------|------------------------|--------------------------------------------------------------------------------|
| __init__()               | load_from (str\|None)                                  | None                   | Initializes a new session, optionally loading from a YAML file.                |
| login()                  | username_email (str), password (str), save_session_to (str) | None               | Performs user authentication with provided credentials.                         |
| add_post()               | text (str), media_url (str\|None)                      | Post                   | Creates a new post with the given text and optional media.                     |
| get_user_by_username()   | username (str)                                         | User                   | Retrieves user information for the specified username.                         |
| me()                     | None                                                   | User                   | Retrieves information about the currently authenticated user.                   |
| get_user_posts()         | user_name (str), pagination_count (int)                | list[Post]             | Retrieves a list of posts from the specified user.                             |

### Properties

| Property         | Type           | Description                                                   |
|------------------|----------------|---------------------------------------------------------------|
| cookies          | Cookie         | Stores session cookies for authentication.                    |
| x_guest_token    | str           | Guest token for API authentication.                           |
| x_csrf_token     | str           | CSRF token for request validation.                            |
| flow_token       | str           | Token for managing authentication flow.                        |
| user_id          | str           | ID of the authenticated user.                                 |

---

## Post

Post is a class dedicated to managing individual posts (tweets) on the X (formerly Twitter) platform. It provides methods for interacting with posts and managing their properties.

### Methods

| Method                    | Arguments                                              | Return Value            | Description                                                                    |
|--------------------------|--------------------------------------------------------|------------------------|--------------------------------------------------------------------------------|
| __init__()               | linked_session                                         | None                   | Initializes a new Post object with an associated session.                      |
| like()                   | None                                                   | None                   | Likes the post using the linked session.                                       |

> Note: The following methods are planned but not yet implemented:
> - `unlike()`
> - `comment(content: str)`
> - `share()`


### Properties

| Property         | Type                | Description                                                   |
|------------------|---------------------|---------------------------------------------------------------|
| id               | str           | The unique identifier of the post.                            |
| user_owner       | User           | The user who created the post.                                |
| creation_date    | Date          | The date and time when the post was created.                  |
| like_count       | int           | The number of likes on the post.                              |
| text_content     | str           | The text content of the post.                                 |
| comment_count    | int           | The number of comments on the post.                           |
| view             | int           | The number of views the post has received.                    |
| repost           | int        | The number of times the post has been reposted.               |
| medias           | List[Media]   | List of media attachments associated with the post.           |

---

## User

User is a class dedicated to managing user profiles on the X (formerly Twitter) platform. It provides methods for accessing user information and performing user-related actions.

### Methods

| Method                    | Arguments                                              | Return Value            | Description                                                                    |
|--------------------------|--------------------------------------------------------|------------------------|--------------------------------------------------------------------------------|
| __init__()               | linked_session                                         | None                   | Initializes a new User object with an associated session.                      |
| follow()                 | None                                                   | None                   | Follows this user using the linked session.                                    |
| unfollow()               | None                                                   | None                   | Unfollows this user using the linked session.                                  |

### Properties

| Property           | Type                | Description                                                   |
|-------------------|---------------------|---------------------------------------------------------------|
| id                | str           | The unique identifier of the user.                            |
| username          | str           | The user's username/handle.                                   |
| name              | str           | The user's display name.                                      |
| profile_image_url | str           | URL of the user's profile image.                              |
| bio               | str           | The user's biography/description.                             |
| location          | str           | The user's location information.                              |
| website           | str           | The user's website URL.                                       |
| created_at        | datetime      | When the user account was created.                            |
| followers_count   | int           | Number of followers the user has.                             |
| following_count   | int           | Number of users this user follows.                            |
| tweet_count      | int           | Number of tweets posted by the user.                          |
| is_verified      | bool          | Whether the user is verified.                                 |
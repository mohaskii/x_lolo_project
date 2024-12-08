# x_lolo

x_lolo is a Python library that allows direct use of Twitter's (formerly X) unofficial API without intermediaries, enhancing security.

## Key Features

- Direct interaction with Twitter's unofficial API
- Developed based on reverse engineering of the API
- Utilizes the HTTPS proxy [mitmproxy](https://mitmproxy.org/) for traffic analysis
- No dependency on web scraping tools like Selenium
- Automation capabilities for various Twitter interactions

## Objectives

- Provide a simple Python interface to interact with Twitter's API
- Offer a secure alternative to traditional authentication methods
- Allow developers to access Twitter features without relying on third-party services

## Project Status

The project is currently under development. It is designed for developers who need direct control over interactions with Twitter's API. 
Currently implemented features include:
- Authentication (login)
- Session management (save/load)
- Post creation and interaction
- User information retrieval
- Follower management
- Post retrieval

### Example Usage:
```python
from x_lolo.session import Session

# Method 1: Create a new session and login
new_session = Session()
new_session.login(
    username_email="your_email@example.com",
    password="your_password",
    save_session_to="session_data.yaml",# Optional: save session for later use
)

# Method 2: Load an existing session
existing_session = Session(load_from="session_data.yaml")

# Create a post
post = existing_session.add_post("Hello, Twitter!")

# Get user information
user = existing_session.get_user_by_username("lolo")
print(f"User: {user.name}")
print(f"Followers: {user.followers_count}")

# Get current user information
me = existing_session.me()
print(f"My username: {me.username}")

# Get user's recent posts (with pagination)
user_posts = existing_session.get_user_posts("twitter", pagination_count=2)
for post in user_posts:
    print(f"Post content: {post.text_content}")
    print(f"Likes: {post.like_count}")

```
The project is hosted at: https://github.com/mohaskii/x_lolo_project/

Contributions are welcome!

Your help in making x_lolo better is greatly appreciated
# Import libraries
import json
import tweepy
import praw

# Open config file and set your Twitter App's unique keys with Reddit's API
with open("config.json") as file:
    data = json.load(file)

    tweepyAuth = tweepy.OAuthHandler(data["twitter"]["api_key"], data["twitter"]["api_secret_key"])
    tweepyAuth.set_access_token(data["twitter"]["access_token"], data["twitter"]["access_token_secret"])
    twitter = tweepy.API(tweepyAuth)

    # Create a read-only reddit instance
    reddit = praw.Reddit(client_id=data["reddit"]["client_id"],
                         client_secret=data["reddit"]["client_secret"],
                         username=data["reddit"]["username"],
                         password=data["reddit"]["password"],
                         user_agent="dk")

# Twitter snippet
print("-"*40, " Twitter ", "-"*40)
# Get top 10 Tweets from your own Twitter account
for item in twitter.home_timeline(count=10):
    print(f'{item.user.screen_name} said:')
    print(item.text)
    print(f'URL: www.twitter.com/{item.user.screen_name}/status/{item.id}\n')

# Reddit snippet
print("-"*40, " Reddit ", "-"*40)
# Get top 10 posts from your own reddit account
for item in reddit.front.top(limit=10):
    print(item.title)
    print("URL:", item.url, '\n')
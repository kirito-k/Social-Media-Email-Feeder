"""
    FileName:       main
    Author:         Devavrat Kalam
    Language:       Python3
    Description:    Social Media Email Service that calls Reddit and Twitter using API calls
                    and send email self containing the collected results.
"""

# Import libraries
import smtplib, ssl
import getpass
import json
import tweepy
import praw

def social_media_instaces(configFile):
    """
    Create Reddit and Twitter API instances
    :param configFile: File containing Configuration details
    :return: Return Reddit and Twitter API instances
    """

    # Open config file and set your Twitter App's unique keys with Reddit's API
    with open(configFile) as file:
        data = json.load(file)

        # Create Twitter instance using Tweepy API wrapper
        tweepyAuth = tweepy.OAuthHandler(data["twitter"]["api_key"], data["twitter"]["api_secret_key"])
        tweepyAuth.set_access_token(data["twitter"]["access_token"], data["twitter"]["access_token_secret"])
        twitter = tweepy.API(tweepyAuth)

        # Create Reddit instance using Praw API wrapper
        reddit = praw.Reddit(client_id=data["reddit"]["client_id"],
                             client_secret=data["reddit"]["client_secret"],
                             username=data["reddit"]["username"],
                             password=data["reddit"]["password"],
                             user_agent="dk")

    return twitter, reddit

def get_twitter_posts(twitter):
    """
    Perform Reddit API call and get top 10 feeds from home timeline
    :param twitter: Tweepy API instance
    :return: Twitter tweets in string format
    """

    # Twitter snippet
    context = '-'*40 + ' Twitter ' + '-'*40 + '\n'
    print(context)

    # Get top 10 Tweets from your own Twitter account
    index = 1
    for item in twitter.home_timeline(count=10):
        template = f'{index}) {item.user.screen_name} said: \n{item.text} ' \
                   f'\nURL: www.twitter.com/{item.user.screen_name}/status/{item.id}\n\n'
        print(template)
        context += template
        index += 1

    return context


def get_reddit_posts(reddit):
    """
    Perform Reddit API call and get top 10 feeds from home timeline
    :param reddit: Praw API instance
    :return: Reddit blogs in string format
    """

    # Reddit snippet
    context = '-'*40 + ' Reddit ' + '-'*40 + '\n'
    print(context)

    # Get top 10 posts from your own reddit account
    index = 1
    for item in reddit.front.top(limit=10):
        template = f'{index}) {item.title} \nURL: {item.url} \n\n'
        print(template)
        context += template
        index += 1

    return context


def send_email(msg):
    """
    Send email
    :param msg: Message to be sent to Email
    :return: None
    """

    port = 465
    sender_email = 'Your_Email'
    password = getpass.getpass(f'\nEnter your password {sender_email}\n')
    receiver_email = 'Receiver_Email'

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login(sender_email, password)

        msg = 'Subject: Your Daily Social Media Feed is here!\n\n' + msg
        server.sendmail(sender_email, receiver_email, msg.encode("utf-8"))


def main():
    print("Gathering Data")
    twitter, reddit = social_media_instaces('config.json')

    # Create msg that contains tweets and reddit feeds
    msg = ""
    msg = msg + get_twitter_posts(twitter) + '\n'
    msg = msg + get_reddit_posts(reddit)

    print("Email Authentication")
    send_email(msg)

if __name__ == '__main__':
    main()

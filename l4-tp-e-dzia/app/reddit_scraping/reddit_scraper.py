"""Reddit scraper file."""

import datetime
import json
import pandas as pd
import praw
from os import path

from reddit_scraping.reddit_submission import RedditSubmission


def load_credentials():
    """Loading credentials.

    :return: reddit object
    """
    with open("reddit_scraping/reddit_credentials.json", 'r') as f:
        credentials = json.load(f)
    reddit = praw.Reddit(client_id=credentials['client_id'],
                         client_secret=credentials['client_secret'],
                         user_agent=credentials['user_agent'])
    return reddit


def scrap_reddit_data(reddit, subreddit_name='all', num_posts=100):
    """Scraps reddit data.

    :param reddit: reddit
    :param subreddit_name: name
    :param num_posts: number of posts
    :return: data
    """
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.new(limit=num_posts)

    submissions = []

    for post in posts:
        if post.author is not None:
            author_name = post.author.name
        else:
            author_name = ""
        r = RedditSubmission(title=post.title, external_url=post.url,
                             text=post.selftext, score=post.score,
                             timestamp=datetime.datetime.fromtimestamp(
                                 post.created_utc, tz=datetime.timezone.utc),
                             id=post.id, author=author_name,
                             upvote_ratio=post.upvote_ratio,
                             distinguished=post.distinguished,
                             num_comments=post.num_comments,
                             num_crossposts=post.num_crossposts,
                             over_18=post.over_18,
                             permalink='https://www.reddit.com' +
                                       post.permalink,
                             text_embedding=None,
                             subreddit=post.subreddit.display_name)
        submissions.append(r)

    # posts = pd.DataFrame.from_records([s.to_dict() for s in submissions])
    return submissions


def save_csv(submissions, filename):
    """Saves as csv.

    :param submissions: submissions
    :param filename: file name
    """
    df = pd.DataFrame.from_records([s.to_dict() for s in submissions])
    if path.exists(filename):
        df.to_csv(filename, sep=';', header=False, decimal=',', mode='a',
                  doublequote=True)
    else:
        df.to_csv(filename, sep=';', header=True, decimal=',', mode='w',
                  doublequote=True)


def get_reddit_data(subreddit_name='all', num_posts=10):
    """Gets reddit data.

    :param subreddit_name: name of subreddit
    :param num_posts: number of posts
    :return: reddit data
    """
    reddit = load_credentials()
    posts = scrap_reddit_data(reddit, subreddit_name=subreddit_name,
                              num_posts=num_posts)
    return posts


if __name__ == "__main__":
    posts = get_reddit_data(subreddit_name='all', num_posts=10)
    save_csv(posts, "posts.csv")

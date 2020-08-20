import datetime
import json
import pandas as pd
import praw
from os import path


def load_credentials():
    with open("reddit_credentials.json", 'r') as f:
        credentials = json.load(f)
    reddit = praw.Reddit(client_id=credentials['client_id'],
                         client_secret=credentials['client_secret'],
                         user_agent=credentials['user_agent'])
    return reddit


def scrap_reddit_data(reddit, subreddit_name='all', num_posts=100):
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.new(limit=num_posts)

    post_urls = []
    post_titles = []
    post_texts = []
    post_scores = []
    post_timestamps = []
    post_ids = []
    post_comments = []
    post_authors = []
    post_upvote_ratio = []
    post_distinguished = []
    post_num_comments = []
    post_num_crossposts = []
    post_over18 = []
    post_permalink = []

    for post in posts:
        post_urls.append(post.url)
        post_titles.append(post.title.replace("'", "''"))
        post_texts.append(post.selftext.replace("'", "''"))
        post_scores.append(post.score)
        post_timestamps.append(datetime.datetime.fromtimestamp(post.created_utc, tz=datetime.timezone.utc))
        post_ids.append(post.id)
        post_authors.append(post.author.name)
        post_upvote_ratio.append(post.upvote_ratio)
        post_distinguished.append(1 if post.distinguished else 0)
        post_num_comments.append(post.num_comments)
        post_num_crossposts.append(post.num_crossposts)
        post_over18.append(post.over_18)
        post_permalink.append('https://www.reddit.com' + post.permalink)

        post.comments.replace_more(limit=0)
        comments = []
        for top_level_comment in post.comments:
            comments.append((top_level_comment.id, top_level_comment.author, top_level_comment.body))
        post_comments.append(comments)

    dict_reddit = {
        'username': post_authors,
        'post_id': post_ids,
        'post_title': post_titles,
        'post_text': post_texts,
        'image_url': post_urls,
        'post_url': post_permalink,
        'date_posted': post_timestamps,
        'num_upvotes': post_scores,
        'upvote_ratio': post_upvote_ratio,
        'is_nsfw': post_over18,
        'is_distinguished': post_distinguished,
        'num_comments': post_num_comments,
        'num_shares': post_num_crossposts,
        'comments': post_comments
    }

    posts = pd.DataFrame.from_dict(dict_reddit, orient='index')
    posts = posts.transpose()
    return posts


def save_csv(df, filename):
    if path.exists(filename):
        df.to_csv(filename, sep=';', header=False, decimal=',', mode='a', doublequote=True)
    else:
        df.to_csv(filename, sep=';', header=True, decimal=',', mode='w', doublequote=True)


def get_reddit_data(subreddit_name='all', num_posts=10):
    reddit = load_credentials()
    posts = scrap_reddit_data(reddit, subreddit_name=subreddit_name, num_posts=num_posts)
    return posts


if __name__ == "__main__":
    posts = get_reddit_data(subreddit_name='all', num_posts=10)
    save_csv(posts, "posts.csv")
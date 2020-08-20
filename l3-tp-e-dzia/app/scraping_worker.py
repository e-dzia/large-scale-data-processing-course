"""Scraping worker file."""

import datetime

from celery_base import app
import celery_base
from docker_logs import get_logger

from reddit_scraping.reddit_scraper import get_reddit_data, save_csv


logging = get_logger("scraping_worker")


def save_metrics(posts, subreddit_name):
    """Saves metrics.

    :param posts: posts
    :param subreddit_name: name of subreddit
    """
    num_fetched = len(posts)
    logging.info(f"Fetched {num_fetched} submissions from {subreddit_name}")

    celery_base.new_submissions_counter.labels(subreddit_name).inc(num_fetched)
    for submission in posts:
        celery_base.post_length_histogram.labels(subreddit_name).observe(
            len(submission.title))


def get_submissions(subreddit_name='all', num_posts=10):
    """Gets all submissions.

    :param subreddit_name: subreddit name
    :param num_posts: number of posts
    :return: all submissions
    """
    return get_reddit_data(subreddit_name=subreddit_name, num_posts=num_posts)


@app.task(bind=True, name='tasks.submission_fetching', serializer='pickle',
          queue="scraping")
def submission_fetching(self, subreddit_name='all', num_posts=10,
                        filename=None):
    """Fetching submissions.

    :param self: celery app
    :param subreddit_name: subreddit name
    :param num_posts: number of posts
    :param filename: file name
    :return: submissions
    """
    logging.info(f"Fetching {num_posts} submissions from {subreddit_name}")
    now = datetime.datetime.now(datetime.timezone.utc)
    posts = get_submissions(subreddit_name, num_posts)

    interval = now - datetime.timedelta(
        seconds=celery_base.SUBMISSION_FETCHING_INTERVAL)
    posts_tmp = []

    for post in posts:
        if post.timestamp >= interval:
            posts_tmp.append(post)
    posts = posts_tmp

    save_metrics(posts, subreddit_name)

    if filename is not None:
        save_csv(posts, filename)

    return posts

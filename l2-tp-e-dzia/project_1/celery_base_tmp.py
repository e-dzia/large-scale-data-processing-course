import datetime

from celery import Celery
from celery.schedules import crontab
from docker_logs import get_logger
from reddit_scraper import get_reddit_data, save_csv
from prometheus_client import Summary, Histogram, Counter
import pandas as pd

logging = get_logger("task")

SUBMISSION_FETCHING_INTERVAL = 30.0
SUBREDDIT_NAME = 'AskReddit'  # ProgrammerHumor
NUM_POSTS = 10
FILENAME = None  # "posts-all.csv"

new_submissions_counter = Counter('new_submissions', 'Counter of new submissions', ['subreddit_name'])
num_comments_counter = Counter('num_comments', 'Counter of number of comments', ['subreddit_name'])
hour_histogram = Histogram('hour', 'Hour of new submissions', ['subreddit_name'], buckets=range(0, 24, 1))
post_length_histogram = Histogram('post_len', 'Post length of new submissions', ['subreddit_name'], buckets=range(0, 1000, 100))
submission_fetch_time = Histogram('submission_fetch_time', 'Submission fetch times in seconds', ['subreddit_name'])

app = Celery()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(SUBMISSION_FETCHING_INTERVAL,
                             submission_fetching.s(SUBREDDIT_NAME, NUM_POSTS, True, FILENAME))


@submission_fetch_time.time()
def get_submissions(subreddit_name='all', num_posts=10):
    return get_reddit_data(subreddit_name=subreddit_name, num_posts=num_posts)


@app.task(bind=True, name='submission_fetching')
def submission_fetching(self, subreddit_name='all', num_posts=10, only_new=True, filename=None):
    logging.info(f"Fetching {num_posts} submissions from {subreddit_name}")
    now = datetime.datetime.now(datetime.timezone.utc)
    posts = get_submissions(subreddit_name, num_posts)
    if only_new:
        interval = now - datetime.timedelta(seconds=SUBMISSION_FETCHING_INTERVAL)
        posts = posts[posts.date_posted >= interval]
        # print(posts[['username', 'date_posted']])
    num_fetched = posts.shape[0]
    sum_comments = posts.num_comments.sum()
    logging.info(f"Fetched {num_fetched} submissions from {subreddit_name}")

    new_submissions_counter.labels(subreddit_name).inc(num_fetched)
    num_comments_counter.labels(subreddit_name).inc(sum_comments)
    for index, post in posts.iterrows():
        post_length_histogram.labels(subreddit_name).observe(round(len(post.post_text), -2))
        hour_histogram.labels(subreddit_name).observe(int(post['date_posted'].hour))

    if filename is not None:
        save_csv(posts, filename)

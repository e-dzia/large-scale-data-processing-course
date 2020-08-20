"""Worker file."""

from celery import group
from celery_base import app
import celery_base
from celery.result import allow_join_result
from docker_logs import get_logger
from scraping_worker import submission_fetching
from embeddings_worker import embedding_calculating


logging = get_logger("scheduling_worker")


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Setting up periodic tasks.

    :param sender: sender
    :param kwargs: args
    """
    sender.add_periodic_task(celery_base.SUBMISSION_FETCHING_INTERVAL,
                             subreddits_scraping.s())


@app.task(bind=True, name='tasks.subreddits_scraping', serializer='pickle',
          queue="default")
def subreddits_scraping(self):
    """Scraping subreddits.

    :param self: celery
    """
    print(".")
    celery_base.num_subreddits.set(len(celery_base.SUBREDDIT_NAMES))
    tasks = []
    for subreddit_name in celery_base.SUBREDDIT_NAMES:
        tasks.append(submission_fetching.s(subreddit_name, num_posts=10))
    results = group(tasks).apply_async()
    with allow_join_result():
        submissions = results.join()
    submissions = [item for sublist in submissions for item in sublist]

    tasks = []
    for submission in submissions:
        tasks.append(embedding_calculating.s(submission))
    results = group(tasks).apply_async()
    with allow_join_result():
        submissions = results.join()

    print(len(submissions))

"""Database worker file."""

from celery_base import app
from docker_logs import get_logger
from reddit_scraping.reddit_submission import RedditSubmission

import pymongo

logging = get_logger("database_worker")

mongo_uri = 'mongodb://root:toor@mongodb:27017'  # /reddit
var = RedditSubmission


@app.task(bind=True, name='tasks.database_insert', serializer='pickle',
          queue="database")
def database_insert(self, post):
    """Inserts post into database.

    :param self: celery
    :param post: RedditSubmission
    :return:
    """
    client = pymongo.MongoClient(mongo_uri)
    db = client.reddit
    collection = db["posts"]

    reddit_post_dict = post.to_dict()

    x = collection.insert_one(reddit_post_dict)

    print("database: ", x.inserted_id)

    return post

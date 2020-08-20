"""Embeddings worker file."""

from celery_base import app
from docker_logs import get_logger
from pymagnitude import Magnitude
import numpy as np

from database_worker import database_insert

logging = get_logger("embeddings_worker")


@app.task(bind=True, name='tasks.embedding_calculating', serializer='pickle',
          queue="embeddings")
def embedding_calculating(self, post):
    """Calculating embedding.

    :param self: celery
    :param post: RedditSubmission
    :return:
    """
    vectors = Magnitude("embeddings/embedding-18.magnitude")
    sentence = post.title
    embeddings = vectors.query(sentence.split())

    embedding = np.mean(embeddings, axis=0)
    post.text_embedding = embedding

    print("embeddings")
    database_insert.s(post).apply_async()

    return post

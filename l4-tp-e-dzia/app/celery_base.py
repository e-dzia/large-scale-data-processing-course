"""Celery base file."""

from celery import Celery
from docker_logs import get_logger
from kombu import Exchange, Queue
from prometheus_client import Histogram, Counter, Gauge

logging = get_logger("task")

SUBMISSION_FETCHING_INTERVAL = 30.0
SUBREDDIT_NAMES = ['funny', 'pics', 'politics', 'news', 'AskRedditAfterDark',
                   'gonewildstories'  # 'nsfw', 'gonewild', 'rule34',
                   # 'AskReddit',
                   ]
NUM_POSTS = 10
FILENAME = None  # "posts-all.csv"

new_submissions_counter = Counter('new_submissions',
                                  'Counter of new submissions',
                                  labelnames=['subreddit_name'])
post_length_histogram = Histogram('title_len',
                                  'Title length of new submissions',
                                  labelnames=['subreddit_name'],
                                  buckets=range(0, 200, 10))
num_subreddits = Gauge('num_subreddits', 'Number of subreddits')

app = Celery()
app.conf.task_serializer = 'pickle'
app.conf.result_serializer = 'pickle'
app.conf.accept_content = ['pickle']

default_exchange = Exchange('default', type='direct')
embeddings_exchange = Exchange('embeddings', type='direct')

app.conf.task_queues = (
    Queue('default', default_exchange, routing_key='default'),
    Queue('embeddings', embeddings_exchange, routing_key='embeddings')
)
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange = 'default'
app.conf.task_default_routing_key = 'default'

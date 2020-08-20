# from celery_base import submission_fetching, SUBREDDIT_NAME, FILENAME
from random import random
from docker_logs import get_logger
from prometheus_client import CollectorRegistry, multiprocess, generate_latest

logging = get_logger("runner")

# submission_fetching.delay(SUBREDDIT_NAME, 10, False, FILENAME)

# result = submission_fetching.delay(random()).get(timeout=10)
# logging.info(f"Task returned: {result}")

# registry = CollectorRegistry()
# # multiprocess.MultiProcessCollector(registry)
# data = generate_latest(registry)
# print(data)
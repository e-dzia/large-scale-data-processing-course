"""Reddit submission file."""
import datetime

import numpy as np


class RedditSubmission:
    """Class of Reddit Submission."""

    def __init__(self, title: str, text: str, score: int,
                 timestamp: datetime.datetime, text_embedding: np.ndarray,
                 id: int, author: str, upvote_ratio: float, distinguished: bool,
                 num_comments: int, num_crossposts: int, over_18: bool,
                 permalink: str, external_url: str,
                 subreddit: str) -> None:
        """Init func.

        :param title: title
        :param text: text
        :param score: score
        :param timestamp: timestamp
        :param text_embedding: embedding
        :param id: id
        :param author: author
        :param upvote_ratio: upvotes
        :param distinguished: distinguished
        :param num_comments: number of comments
        :param num_crossposts: number of crossposts
        :param over_18: is over 18
        :param permalink: permalink
        :param external_url: external url
        :param subreddit: name of subreddit
        """
        self.id = id
        self.permalink = permalink
        self.subreddit = subreddit
        self.author = author
        self.title = title
        self.title_length = len(title)
        self.text = text
        self.text_length = len(text)
        self.text_embedding = text_embedding
        self.score = score
        self.over_18 = over_18
        self.num_comments = num_comments
        self.timestamp = timestamp
        self.upvote_ratio = upvote_ratio
        self.distinguished = distinguished
        self.num_crossposts = num_crossposts
        self.external_url = external_url

    def to_dict(self):
        """Changes object to dict object.

        :return: dict
        """
        return {
            'id': self.id,
            'author': self.author,
            'title': self.title,
            'text': self.text,
            'text_embedding': self.text_embedding,
            'permalink': self.permalink,
            'external_url': self.external_url,
            'timestamp': self.timestamp,
            'score': self.score,
            'upvote_ratio': self.upvote_ratio,
            'over_18': self.over_18,
            'distinguished': self.distinguished,
            'num_comments': self.num_comments,
            'num_crossposts': self.num_crossposts,
            'subreddit': self.subreddit,
            'title_length': self.title_length,
            'text_length': self.text_length
        }

    @property
    def text_embedding(self):
        """Property of text embedding.

        :return: embedding
        """
        return self.__text_embedding

    @text_embedding.setter
    def text_embedding(self, embedding):
        """Setter of text embedding.

        :param embedding: embedding
        :return: None
        """
        if type(embedding) is np.ndarray:
            self.__text_embedding = embedding.tolist()
        else:
            self.__text_embedding = embedding

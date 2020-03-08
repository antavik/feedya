import logging

import database as db

from typing import Tuple
from concurrent.futures import ThreadPoolExecutor as TPE, as_completed

from settings import THREADS_QUANTITY, THREAD_TIMEOUT
from entities import NewsItemEntity, FeedEntity
from exceptions import NewsAlreadyExists


def _mark_late_news(news: NewsItemEntity) -> NewsItemEntity:
    try:
        news = db.create_news(news)
    except NewsAlreadyExists as exc:
        news.late = True

        logging.debug(exc)
    except Exception as exc:
        logging.error(exc)
    else:
        news.late = False

    return news


def _process_news(feeds: Tuple[FeedEntity]) -> Tuple[FeedEntity]:
    with TPE(max_workers=THREADS_QUANTITY) as executor:
        futures = tuple(
            executor.submit(_mark_late_news, n)
            for f in feeds for n in f.news
        )

        for future in as_completed(futures, timeout=THREAD_TIMEOUT):
            future.result()

        return feeds


def prepare_news(feeds: Tuple[FeedEntity]) -> Tuple[FeedEntity]:
    for feed in _process_news(feeds):
        feed.news.sort(key=lambda n: n.publication_date, reverse=True)

        feed.news = [n for n in feed.news if not n.late]

    return feeds

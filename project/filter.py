import logging

from typing import Iterator, List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor as TPE, as_completed

from settings import THREADS_QUANTITY, THREAD_TIMEOUT, MAX_LATE_NEWS
from database import create_news
from entities import NewsItemEntity, FeedEntity
from exceptions import NewsAlreadyExists


def _block_ad(news: NewsItemEntity) -> bool:

    return 'реклама' in news.description


def _mark_late_news(news: NewsItemEntity) -> NewsItemEntity:
    try:
        news = create_news(news)
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
            for f in feeds for n in f.news if not _block_ad(n)
        )

        for future in as_completed(futures, timeout=THREAD_TIMEOUT):
            future.result()

        return feeds


def _count_late_news(news: List[NewsItemEntity]) -> int:
    fresh_news = tuple(n for n in news if n.late)

    return len(fresh_news)


def prepare_news(feeds: Tuple[FeedEntity]) -> Tuple[FeedEntity]:
    for feed in _process_news(feeds):
        feed.news.sort(key=lambda n: n.publication_date, reverse=True)

        if (late_news_qty := _count_late_news(feed.news)) > MAX_LATE_NEWS:
            fresh_news = len(feed.news) - late_news_qty
            feed.news = feed.news[:fresh_news + MAX_LATE_NEWS]

    return feeds

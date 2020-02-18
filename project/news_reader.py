import logging
import datetime

from typing import Iterator, Tuple
from concurrent.futures import ThreadPoolExecutor as TPE, as_completed

from settings import THREADS_QUANTITY, THREAD_TIMEOUT, COLLECTOR_CONFIGURATION
from entities import FeedEntity, NewsItemEntity


def _get_feed_raw_data(feed: FeedEntity) -> FeedEntity:

    get_feed = COLLECTOR_CONFIGURATION[feed.feed_type].collector

    feed.raw_data = get_feed(feed)
    feed.collection_date = datetime.datetime.now()

    return feed


def _parse_raw_data(feed: FeedEntity) -> Iterator[NewsItemEntity]:

    parse = COLLECTOR_CONFIGURATION[feed.feed_type].parser

    return parse(feed)


def _get_feeds_data(feeds: Tuple[FeedEntity]) -> Tuple[FeedEntity]:
    with TPE(max_workers=THREADS_QUANTITY) as executor:
        futures = tuple(
            executor.submit(_get_feed_raw_data, f)
            for f in feeds
        )

        for future in as_completed(futures, timeout=THREAD_TIMEOUT):
            future.result()

        logging.info('Feeds were received.')

        return feeds


def _parse_feeds_data(feeds: Tuple[FeedEntity]) -> Tuple[FeedEntity]:
    for feed in feeds:
        if feed.raw_data:
            try:
                feed.news = [n for n in _parse_raw_data(feed)]
            except KeyError as exp:
                logging.error('%s cannot be parsed: %s.', feed, exp)
        else:
            logging.warning('%s is empty.', feed)

    return feeds


def get_news(feeds) -> Tuple[FeedEntity]:

    return _parse_feeds_data(_get_feeds_data(feeds))

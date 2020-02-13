import requests
import logging

from typing import Union

from entities import FeedEntity


def get_feed(feed: FeedEntity) -> Union[str, None]:
    try:
        response = requests.get(feed.url)
        response.raise_for_status()
    except Exception as exc:
        raw_data = None

        logging.warning(exc)
    else:
        raw_data = response.text

    return raw_data

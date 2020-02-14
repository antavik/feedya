import logging

from typing import Iterator
from dateutil.parser import parse as dp

from bs4 import BeautifulSoup
from lxml import html

from entities import FeedEntity, NewsItemEntity


def _repair_rss_xml(raw_xml: str) -> str:
    replace_table = {
        '&#x3C;': '<',
        '&#x3E;': '>',
        '&#039;': '\'',
        '&amp;': '&',
    }

    for invalid, replacment in replace_table.items():
        raw_xml = raw_xml.replace(invalid, replacment)

    return raw_xml


def parse_rss_xml_document(feed: FeedEntity) -> Iterator[NewsItemEntity]:
    _rss_configurations = (
        {'body': 'channel',
         'item': 'item',
         'pub_date': 'pubDate',
         'url': 'link',
         },
        {'body': 'feed',
         'item': 'entry',
         'pub_date': 'published',
         'url': 'id',
         },
    )

    soup = BeautifulSoup(_repair_rss_xml(feed.raw_data), 'xml')

    for configuration in _rss_configurations:
        if body := soup.find(configuration['body']):
            for item in body.findChildren(configuration['item']):
                title = item.title.text.strip()
                url = item.find(configuration['url']).text

                publication_date = dp(
                    item.find(configuration['pub_date']).text, fuzzy=True
                )

                if not feed.data.get('ignore_descriptions'):
                    description = item.description.text.strip() if item.description else ''
                else:
                    description = ''

                yield NewsItemEntity(
                    title=title,
                    description=description,
                    url=url,
                    feed=feed.title,
                    publication_date=publication_date,
                    collection_date=feed.collection_date,
                )

            break
        else:
            continue

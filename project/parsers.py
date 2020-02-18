import logging

from typing import Iterator
from dateutil.parser import parse as dp

from bs4 import BeautifulSoup
from lxml import html

from entities import FeedEntity, NewsItemEntity


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

    soup = BeautifulSoup(feed.raw_data, 'lxml-xml')

    for configuration in _rss_configurations:
        if body := soup.find(configuration['body']):
            for item in body.findChildren(configuration['item']):
                url = item.find(configuration['url']).text.strip()
                title = item.title.text.strip() if item.title else url

                publication_date = dp(
                    item.find(configuration['pub_date']).text, fuzzy=True
                )

                if description_item := item.description:
                    description_soap = BeautifulSoup(description_item.text,
                                                     'lxml')
                    description = description_soap.text
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

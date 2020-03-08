import abc
import logging
import urllib

from dateutil.parser import parse as dp
from typing import Iterator

from bs4 import BeautifulSoup
from lxml import html, etree

from entities import FeedEntity, NewsItemEntity
from utils import block_ad


REGISTRIES = {}


class Parser(metaclass=abc.ABCMeta):

    def __init_subclass__(cls):
        if not hasattr(cls, 'feed_type'):
            feed_type = cls.__name__.lower()
            setattr(cls, 'feed_type', feed_type)

        REGISTRIES[cls.feed_type] = cls.parse

    @staticmethod
    @abc.abstractmethod
    def parse(feed):
        pass


class RSS(Parser):

    def parse(feed):
        _rss_configurations = (
            {'body': 'channel',
             'news': 'item',
             'pub_date': 'pubDate',
             'url': 'link',
             },
            {'body': 'feed',
             'news': 'entry',
             'pub_date': 'updated',
             'url': 'link',
             },
        )

        soup = BeautifulSoup(feed.raw_data, 'lxml-xml')

        for configuration in _rss_configurations:
            if body := soup.find(configuration['body']):
                for item in body.findChildren(configuration['news']):
                    if url := (item.find(configuration['url']).text or item.find(configuration['url'])['href']):
                        url = url.strip()

                    title = item.title.text.strip() if item.title else url

                    publication_date = dp(
                        item.find(configuration['pub_date']).text, fuzzy=True
                    )

                    if item.description:
                        description_soap = BeautifulSoup(
                            item.description.text, 'lxml'
                        )
                        description = description_soap.text
                    else:
                        description = ''

                    if block_ad(description):
                        continue

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


class HN(Parser):

    def parse(feed):
        max_news = feed.data['max_news']

        _title_xpath = '//table//tr[3]/td/table//tr[td[@class="votelinks"]]/td[3]/a'
        _description_xpath = '//table//tr[3]/td/table//tr/td[span[@class="score"] and a[last() and @href]]'
        _relative_points_xpath = 'span[@class="score"]/text()'
        _relative_thread_link_xpath = 'a[last()]/@href'
        _relative_comments_xpath = 'a[last()]/text()'

        html_page = html.fromstring(feed.raw_data)

        titles = html_page.xpath(_title_xpath)
        descriptions = html_page.xpath(_description_xpath)

        for title, description in zip(titles[:max_news], descriptions):
            thread_id = description.xpath(_relative_thread_link_xpath)[0]
            points = description.xpath(_relative_points_xpath)[0]
            comments = description.xpath(_relative_comments_xpath)[0]
            internal_url = urllib.parse.urljoin(
                'https://news.ycombinator.com/', thread_id
            )

            yield NewsItemEntity(
                title=title.text,
                url=title.attrib['href'],
                feed=feed.title,
                publication_date=feed.collection_date,
                collection_date=feed.collection_date,
                data={
                    'url': internal_url,
                    'url_comment': f'{points}, {comments}',
                }
            )

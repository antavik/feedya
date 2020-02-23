import logging

from typing import Iterator
from dateutil.parser import parse as dp

from bs4 import BeautifulSoup
from lxml import html

from entities import FeedEntity, NewsItemEntity
from utils import block_ad


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


def parse_hn_html_document(feed: FeedEntity) -> Iterator[NewsItemEntity]:
    max_news = 15

    _title_xpath = '/html/body/center/table//tr[3]/td/table//tr[@class="athing"]/td[3]/a'
    _description_xpath = '/html/body/center/table//tr[3]/td/table//tr[not(@class) and position()<last()]/td[2]'
    _relative_points_xpath = 'span[1]/text()'
    _relative_thread_link_xpath = 'a[3]/@href'
    _relative_comments_xpath = 'a[3]/text()'

    html_page = html.fromstring(feed.raw_data)

    titles = html_page.xpath(_title_xpath)
    descriptions = html_page.xpath(_description_xpath)

    for title, description in zip(titles[:max_news], descriptions[:max_news]):
        points = description.xpath(_relative_points_xpath)[0]
        thread_id = description.xpath(_relative_thread_link_xpath)[0]
        comments = description.xpath(_relative_comments_xpath)[0]

        yield NewsItemEntity(
            title=title.text,
            url=title.attrib['href'],
            feed=feed.title,
            publication_date=feed.collection_date,
            collection_date=feed.collection_date,
            data={
                'url': f'https://news.ycombinator.com/{thread_id}',
                'url_comment': f'{points}, {comments}',
            }
        )

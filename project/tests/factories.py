import factory

from pytest_factoryboy import register
from faker import Faker

from entities import FeedEntity, NewsItemEntity


faker = Faker()


@register
class FeedEntityFactory(factory.Factory):

    class Meta:
        model = FeedEntity

    feed_type = factory.Iterator(('rss', 'test',))
    title = factory.Faker('company')
    url = factory.Faker('url')
    data = factory.Iterator(({}, None))
    raw_data = None
    collection_date = factory.Faker('date')
    news = []


@register
class NewsItemEntityFactory(factory.Factory):

    class Meta:
        model = NewsItemEntity

    pk = None
    title = factory.Faker('company')
    description = factory.Faker('text')
    url = factory.Faker('url')
    publication_date = factory.Faker('date')
    collection_date = factory.Faker('date')
    feed = factory.Faker('company')
    data = {}
    late = None

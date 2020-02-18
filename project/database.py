import logging
import contextlib
import json

from sqlalchemy import (
    create_engine, Table, Column, Integer, String, DateTime, MetaData,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.exc import IntegrityError

from settings import DB_URL
from entities import NewsItemEntity
from exceptions import NewsAlreadyExists


_ENGINE = create_engine(DB_URL)

_METADATA = MetaData()

news = Table(
    'news',
    _METADATA,
    Column('id', Integer, primary_key=True),
    Column('feed', String(50), nullable=False),
    Column('title', String(200), nullable=False),
    Column('url', String(300), nullable=False, unique=True, index=True),
    Column('publication_date', DateTime, nullable=False),
    Column('collection_date', DateTime, nullable=False),
    Column('data', JSONB)
)

_METADATA.create_all(_ENGINE)


@contextlib.contextmanager
def establish_connection():
    try:
        connection = _ENGINE.connect()
    except Exception as exp:
        logging.error(exp)
    else:
        yield connection
    finally:
        connection.close()


def create_news(entity: NewsItemEntity) -> NewsItemEntity:
    query = news.insert().values(
        feed=entity.feed,
        title=entity.title,
        url=entity.url,
        publication_date=entity.publication_date,
        collection_date=entity.collection_date,
        data=json.dumps(entity.data)
    )
    query.compile()

    with establish_connection() as connection:
        try:
            result = connection.execute(
                query
            )

            query.bind = _ENGINE
        except IntegrityError:
            raise NewsAlreadyExists(f'News {entity.url} already exists.')
        else:
            entity.pk = result.inserted_primary_key

    return entity

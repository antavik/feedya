import logging
import contextlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from settings import DB_URL
from models.model import Model
from models import News
from entities import NewsItemEntity
from exceptions import NewsAlreadyExists


_ENGINE = create_engine(DB_URL)

Model.metadata.create_all(_ENGINE)

_SESSION = sessionmaker(bind=_ENGINE)


@contextlib.contextmanager
def establish_session():
    try:
        session = _SESSION()
    except Exception as exp:
        logging.error(exp)
    else:
        yield session
    finally:
        session.close()


def create_news(entity: NewsItemEntity) -> NewsItemEntity:
    obj = News(feed=entity.feed,
               title=entity.title,
               url=entity.url,
               publication_date=entity.publication_date,
               collection_date=entity.collection_date,
               data=entity.data)

    with establish_session() as session:
        try:
            session.add(obj)
            session.commit()
        except IntegrityError:
            session.rollback()

            raise NewsAlreadyExists(f'News {entity.url} already exists.')
        else:
            entity.pk = obj.id

    return entity

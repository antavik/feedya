from .model import Model

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB


class News(Model):

    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    feed = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    url = Column(String(300), nullable=False, unique=True, index=True)
    publication_date = Column(DateTime, nullable=False)
    collection_date = Column(DateTime, nullable=False)
    data = Column(JSONB)

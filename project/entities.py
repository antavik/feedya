from datetime import datetime
from dataclasses import dataclass, field
from typing import Union, Optional, Dict, List


@dataclass(repr=False)
class NewsItemEntity:
    title: str
    description: str
    url: str
    feed: str
    publication_date: datetime
    collection_date: datetime
    data: Dict = field(default_factory=dict)
    pk: Optional[int] = None
    late: Optional[bool] = None

    @property
    def pub_date_str(self):

        return self.publication_date.strftime('%d-%b-%Y')

    def __eq__(self, other):

        return self.url == other

    def __repr__(self):
        class_name = self.__class__.__name__

        return (
            f'{class_name}('
            f'id={self.pk}, title={self.title}, '
            f'url={self.url}, late={self.late}, '
            f'pub_date={self.publication_date})'
        )


@dataclass
class FeedEntity:
    feed_type: str
    title: str
    url: str
    data: Dict = field(default_factory=dict)
    raw_data: Optional[str] = None
    collection_date: Optional[datetime] = None
    news: List[NewsItemEntity] = field(default_factory=list)

    def __hash__(self):

        return hash(self.url)

    def __repr__(self):

        return f'FeedEntity(title={self.title})'

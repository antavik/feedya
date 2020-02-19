from tests.factories import NewsItemEntityFactory

from filter import _mark_late_news, _count_late_news, _block_ad
from exceptions import NewsAlreadyExists


class TestFilter:

    def test_mark_late_news__new_entity__fresh_news(self, mocker):
        entity = NewsItemEntityFactory()

        mock = mocker.patch('filter.create_news')
        mock.return_value = entity

        marked_entity = _mark_late_news(entity)

        assert not marked_entity.late

    def test_mark_late_news__new_entity__late_news(self, mocker):
        entity = NewsItemEntityFactory(title='qwe')

        mock = mocker.patch('filter.create_news')
        mock.side_effect = NewsAlreadyExists

        marked_entity = _mark_late_news(entity)

        assert marked_entity.late

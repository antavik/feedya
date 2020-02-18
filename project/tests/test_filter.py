from tests.factories import NewsItemEntityFactory

from filter import _mark_late_news, _count_late_news, _block_ab
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

    def test_count_late_news__late_news_list__int(self):
        news_list = tuple(NewsItemEntityFactory(late=True) for _ in range(3))

        lenth = _count_late_news(news_list)

        assert lenth
        assert isinstance(lenth, int)

    def test_count_late_news__no_late_news_list__int(self):
        news_list = tuple(NewsItemEntityFactory() for _ in range(3))

        lenth = _count_late_news(news_list)

        assert not lenth
        assert isinstance(lenth, int)

    def test_count_late_news__empty_list__int(self):
        news_list = tuple()

        lenth = _count_late_news(news_list)

        assert not lenth
        assert isinstance(lenth, int)

    def test_block_ad__valid_news__false(self):
        entity = NewsItemEntityFactory()

        assert not _block_ab(entity)

    def test_block_ad__news_with_ad__true(self):
        entity = NewsItemEntityFactory(description='реклама')

        assert _block_ab(entity)

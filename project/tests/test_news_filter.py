import news_filter

from tests.factories import NewsItemEntityFactory

from exceptions import NewsAlreadyExists


class TestNewsFilter:

    def test_mark_late_news__new_entity__fresh_news(self, mocker):
        entity = NewsItemEntityFactory()

        mock = mocker.patch('news_filter.db.create_news')
        mock.return_value = entity

        marked_entity = news_filter._mark_late_news(entity)

        assert not marked_entity.late

    def test_mark_late_news__new_entity__late_news(self, mocker):
        entity = NewsItemEntityFactory(title='qwe')

        mock = mocker.patch('news_filter.db.create_news')
        mock.side_effect = NewsAlreadyExists

        marked_entity = news_filter._mark_late_news(entity)

        assert marked_entity.late

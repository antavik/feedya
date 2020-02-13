import pytest

from tests.factories import FeedEntityFactory

from collectors import get_feed


class TestCaseCollectors:

    @pytest.mark.parametrize('http_response', [(200, 'test')], indirect=True)
    def test_get_feed__feed__raw_data(self, mocker, http_response):
        mock = mocker.patch('requests.get')
        mock.return_value = http_response

        test_feed = FeedEntityFactory()

        raw_data = get_feed(test_feed)

        assert raw_data is not None and isinstance(raw_data, str)

    @pytest.mark.parametrize('http_response', [(400, 'test')], indirect=True)
    def test_get_feed__feed__none(self, mocker, http_response):
        mock = mocker.patch('requests.get')
        mock.return_value = http_response

        test_feed = FeedEntityFactory()

        raw_data = get_feed(test_feed)

        assert raw_data is None

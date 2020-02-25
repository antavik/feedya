from utils import block_ad


class TestUtils:

    def test_block_ad__text_without_ad__false(self):
        test_str = 'test'

        assert not block_ad(test_str)

    def test_block_ad__text_with_ad__true(self):
        test_str = 'реклама'

        assert block_ad(test_str)

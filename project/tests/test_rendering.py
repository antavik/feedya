from tests.factories import FeedEntityFactory

from rendering import color_randomizer, render_html_email


class TestRendering:

    def test_color_randomizer__tupe(self):
        colors = color_randomizer()

        assert len(colors) == 2

    def test_render_html_email__feeds__str(self):
        feeds = tuple(FeedEntityFactory() for _ in range(3))

        html_page = render_html_email(feeds)

        assert isinstance(html_page, str)
        assert '<!DOCTYPE html>' in html_page

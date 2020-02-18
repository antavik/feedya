import logging

from typing import Tuple
from random import choice

from jinja2 import Environment, FileSystemLoader
from jinja2.environment import Template

from settings import TEMPLATES_DIR, TEMPLATE_NAME, TODAY_DATETIME
from entities import FeedEntity
from feeds import FEEDS


def color_randomizer() -> Tuple[str]:
    _support_color_pairs = (
        ('#fff3b0', '#3574cc',),
        ('#25b8a9', '#b82534',),
        ('#b6ff1c', '#651cff',),
        ('#19f76d', '#f719a3',),
        ('#aec575', '#8c75c5',),
        ('#8dcf83', '#a759b3',),
        ('#6dd81b', '#9d3ee5',),
        ('#96ca98', '#ca96c8',),
        ('#2a7e6c', '#dd2e53',),
        ('#42e4e7', '#e74542',),
        ('#bed0ff', '#83785b',),
    )

    return choice(_support_color_pairs)


def _get_html_template() -> Template:
    env_template = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=True
    )

    return env_template.get_template(TEMPLATE_NAME)


def render_html_email(feeds: Tuple[FeedEntity]) -> str:
    template = _get_html_template()

    title_bg_color, title_font_color = color_randomizer()

    email = template.render(
        title_bg_color=title_bg_color,
        title_font_color=title_font_color,
        feed_datetime=TODAY_DATETIME,
        feeds=FEEDS
    )

    logging.info('Email feed was prepared.')

    return email

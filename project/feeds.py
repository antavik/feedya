from entities import FeedEntity as FE


FEEDS = (
    FE('rss', 'The Verge', 'https://www.theverge.com/rss/index.xml', data={'ignore_descriptions': True}),
    FE('rss', 'Wired', 'https://www.wired.com/feed/rss'),
    FE('rss', 'VB', 'https://feeds.feedburner.com/venturebeat/SZYF'),
    FE('rss', 'TechCrunch', 'http://feeds.feedburner.com/TechCrunch/'),
    FE('rss', 'BBC Tech', 'http://feeds.bbci.co.uk/news/technology/rss.xml'),
    FE('rss', 'NYT Tech', 'https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml'),
    FE('rss', 'Engadged', 'https://www.engadget.com/rss.xml', data={'ignore_descriptions': True}),
    FE('rss', 'WSJ Tech', 'https://feeds.a.dj.com/rss/RSSWSJD.xml'),
    FE('rss', 'BBC Science & Environment', 'http://feeds.bbci.co.uk/news/science_and_environment/rss.xml'),
    FE('rss', 'dev.by', 'https://dev.by/rss'),
    FE('rss', 'NYT Home Page', 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'),
    FE('rss', 'python PEP', 'https://www.python.org/dev/peps/peps.rss'),
    FE('rss', 'tut.by', 'https://news.tut.by/rss/index.rss'),
)

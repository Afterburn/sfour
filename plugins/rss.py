import feedparser


def execute(plugins, url):
    p = feedparser.parse(url)
    print(p['feed']['title'])


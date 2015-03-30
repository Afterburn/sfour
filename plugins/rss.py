import feedparser


def execute(url):
    p = feedparser.parse(url)
    print(p['feed']['title'])


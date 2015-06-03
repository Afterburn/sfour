import logging
from datetime import datetime
from time import mktime

import feedparser
from bs4 import BeautifulSoup

#https://pythonhosted.org/feedparser/

logger = logging.getLogger()

def assert_value(value, feed):
    if value in feed:
        return True

    return False


def validate(feed):
    if 'feed' not in feed:
        logger.warn('feed not in feed')
        return False

    for entry in feed.entries:
        if 'summary_detail' not in entry or 'value' not in entry['summary_detail']:
            logger.warn('feed missing summary_detail: %s ' % (feed['feed']['title']))
            return False

        if 'published' not in entry:
            logger.warn('feed missing published')
            return False


    if 'title' not in feed['feed']:
        logger.warn('title not in feed')
        return False
    
    if not len(feed.entries):
        logger.warn('no entries in feed')
        return False

    return True


def strip_html(data):
    return BeautifulSoup(data).get_text()


def convert_time(time_string):
    return datetime.fromtimestamp(mktime(time_string))


def execute(url, db, **args):


    feed = feedparser.parse(url)
    
    logger.debug('feed status: %s' % (feed.status))

    if not validate(feed):
        logger.warn('feed not valid')
        return False

   
    title = feed['feed']['title']

    # Validate the feed
    print(feed)

    # This queries the database for an existing title, if it does not exist it adds it. We also 
    # need the parent "id" for the "entry".
    query = db.session.query(db.base.classes.rss.title, db.base.classes.rss.id).filter_by(title=title).first()

    if not query:
        query = db.base.classes.rss(title=title)

    for entry in feed.entries:
        summary_detail = strip_html(entry['summary_detail']['value'])
        published      = convert_time(entry['published_parsed'])

        data = db.base.classes.entry(summary_detail=summary_detail,
                                      published=published,
                                      parent_id=query.id, 
                                      url=url)

        db.session.add(data)

        if 'notify' in args:
            args['plugins']('notify').execute(entry, db, **args)

    db.session.commit()


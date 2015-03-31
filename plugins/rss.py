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
        if 'value' not in entry['summary_detail']:
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

def execute(plugins, db, url):
    feed = feedparser.parse(url)
    
    logger.info('feed status: %s' % (feed.status))

    if not validate(feed):
        logger.info('feed not valid')
        return False

    logger.info('feed validated')

    feed_db = db.base.classes.rss(title=feed['feed']['title'])

    for e in feed.entries:
        summary_detail = BeautifulSoup(e['summary_detail']['value']).get_text()
        published      = datetime.fromtimestamp(mktime(e['published_parsed']))

        entry = db.base.classes.entry(summary_detail=summary_detail,
                                      published=published)
        
        feed_db.entry_collection.append(entry)


    db.session.add(feed_db)
    db.session.commit()


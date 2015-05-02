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


def strip_html(data):
    return BeautifulSoup(data).get_text()


def convert_time(time_string):
    return datetime.fromtimestamp(mktime(time_string))



def alert_on(**args):
    if 'change' in args:
        pass



def execute(url, db, **args):


    feed = feedparser.parse(url)
    
    logger.debug('feed status: %s' % (feed.status))

    if not validate(feed):
        logger.warn('feed not valid')
        return False

   
    title = feed['feed']['title']

    # This queries the database for an existing title, if it does not exist it adds it. We also 
    # need the parent "id" for the "entry".
    query = db.session.query(db.base.classes.rss.title, db.base.classes.rss.id).filter_by(title=title).first()

    if not query:
        query = db.session.classes.rss(title=title)

    for e in feed.entries:
        summary_detail = strip_html(e['summary_detail']['value'])
        published      = convert_time(e['published_parsed'])

        entry = db.base.classes.entry(summary_detail=summary_detail,
                                      published=published,
                                      parent_id=query.id)

        db.session.add(entry)

    db.session.commit()


    if 'alert_on' in args:
        alert_on(**args)

import logging
from jinja2 import Environment, FileSystemLoader






#https://pythonhosted.org/feedparser/

'''{'updated_parsed': time.struct_time(tm_year=2015, tm_mon=5, tm_mday=26, tm_hour=19, tm_min=57, tm_sec=0, tm_wday=1, tm_yday=146, tm_isdst=0), 'links': [{'href': u'http://alerts.weather.gov/cap/wwacapget.php?x=AK1253A8F4B7F4.SpecialWeatherStatement.1253A9134D40AK.AFCSPSALU.2d35fbe00ba2f1771418d34c289c4a30', 'type': u'text/html', 'rel': u'alternate'}], u'cap_expires': u'2015-05-28T12:00:00-08:00', 'valuename': u'VTEC', 'summary_detail': {'base': u'http://alerts.weather.gov/cap/us.php?x=0', 'type': u'text/plain', 'value': u'...HIGH WATER LEVELS ON AREA RIVERS DRAINING THE WOOD RIVER MOUNTAINS THIS WEEK... AREAS NORTH AND WEST OF DILLINGHAM HAVE BEEN IMPACTED WITH PERSISTENT RAIN OVER THE PAST WEEK...WITH SOME AREAS RECEIVING AN ESTIMATED 3 TO 4 INCHES. THIS HAS RESULTED IN STEADILY RISING WATER LEVELS ON AREA RIVERS DRAINING THE WOOD RIVER', 'language': None}, u'cap_status': u'Actual', u'cap_event': u'Special Weather Statement', 'id': u'http://alerts.weather.gov/cap/wwacapget.php?x=AK1253A8F4B7F4.SpecialWeatherStatement.1253A9134D40AK.AFCSPSALU.2d35fbe00ba2f1771418d34c289c4a30', 'published_parsed': time.struct_time(tm_year=2015, tm_mon=5, tm_mday=26, tm_hour=19, tm_min=57, tm_sec=0, tm_wday=1, tm_yday=146, tm_isdst=0), 'author': u'w-nws.webmaster@noaa.gov', u'cap_effective': u'2015-05-26T11:57:00-08:00', u'cap_geocode': u'', 'title_detail': {'base': u'http://alerts.weather.gov/cap/us.php?x=0', 'type': u'text/plain', 'value': u'Special Weather Statement issued May 26 at 11:57AM AKDT by NWS', 'language': None}, 'updated': u'2015-05-26T11:57:00-08:00', u'cap_severity': u'Minor', u'cap_msgtype': u'Alert', 'link': u'http://alerts.weather.gov/cap/wwacapget.php?x=AK1253A8F4B7F4.SpecialWeatherStatement.1253A9134D40AK.AFCSPSALU.2d35fbe00ba2f1771418d34c289c4a30', 'authors': [{'name': u'w-nws.webmaster@noaa.gov'}], u'cap_polygon': u'', 'author_detail': {'name': u'w-nws.webmaster@noaa.gov'}, u'cap_certainty': u'Observed', u'cap_category': u'Met', u'cap_urgency': u'Expected', u'cap_parameter': u'', 'value': u'', 'summary': u'...HIGH WATER LEVELS ON AREA RIVERS DRAINING THE WOOD RIVER MOUNTAINS THIS WEEK... AREAS NORTH AND WEST OF DILLINGHAM HAVE BEEN IMPACTED WITH PERSISTENT RAIN OVER THE PAST WEEK...WITH SOME AREAS RECEIVING AN ESTIMATED 3 TO 4 INCHES. THIS HAS RESULTED IN STEADILY RISING WATER LEVELS ON AREA RIVERS DRAINING THE WOOD RIVER', 'guidislink': True, 'published': u'2015-05-26T11:57:00-08:00', 'title': u'Special Weather Statement issued May 26 at 11:57AM AKDT by NWS', u'cap_areadesc': u'Bristol Bay'}'''

logger = logging.getLogger()
env    = Environment()

def execute(db, **args):
    message = args['message']
    args = args['notify']

    # Notify on anything new
    if 'new' in args and args['new'] == True:
        logging.debug('notification: %s' % args)
        msg = env.from_string(args['message'])
        print(msg.render(args['entry']))


    if message:
        print(message)

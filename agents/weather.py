import logging
import json
import requests

logger = logging.getLogger()

def execute(db, **args):

    assert 'api_key' in args
    assert 'zip_code' in args


    #query = db.session.query(db.base.classes.rss.title, db.base.classes.rss.id).filter_by(title=title).first()

    #if not query:
    #    query = db.base.classes.rss(title=title)

        #data = db.base.classes.entry(summary_detail=summary_detail,
        #                              published=published,
        #                              parent_id=query.id, 
        #                              url=url)

        #db.session.add(data)

        #if 'notify' in args:
        #    args['plugins']('notify').execute(entry, db, **args)

    #db.session.commit()


    #http://www.wunderground.com/weather/api/d/docs?d=data/forecast10day&MR=1
    #{u'avehumidity': 83, u'maxhumidity': 0, u'avewind': {u'kph': 1, u'degrees': 257, u'dir': u'WSW', u'mph': 1}, u'icon_url': u'http://icons.wxug.com/i/c/k/partlycloudy.gif', u'snow_allday': {u'cm': 0.0, u'in': 0.0}, u'maxwind': {u'kph': 13, u'degrees': 0, u'dir': u'', u'mph': 8}, u'minhumidity': 0, u'period': 1, u'pop': 20, u'skyicon': u'', u'high': {u'fahrenheit': u'71', u'celsius': u'21'}, u'qpf_night': {u'mm': 0, u'in': 0.0}, u'qpf_allday': {u'mm': 0, u'in': 0.01}, u'low': {u'fahrenheit': u'48', u'celsius': u'9'}, u'snow_night': {u'cm': 0.0, u'in': 0.0}, u'date': {u'tz_short': u'MDT', u'weekday_short': u'Wed', u'isdst': u'1', u'monthname': u'June', u'hour': 19, u'min': u'00', u'ampm': u'PM', u'tz_long': u'America/Denver', u'month': 6, u'epoch': u'1433379600', u'sec': 0, u'weekday': u'Wednesday', u'pretty': u'7:00 PM MDT on June 03, 2015', u'year': 2015, u'yday': 153, u'day': 3, u'monthname_short': u'Jun'}, u'snow_day': {u'cm': None, u'in': None}, u'qpf_day': {u'mm': None, u'in': None}, u'conditions': u'Partly Cloudy', u'icon': u'partlycloudy'}


    page = requests.get("http://api.wunderground.com/api/%s/forecast10day/q/%s.json" % (args['api_key'], args['zip_code']))
   
     
    for item in json.loads(page.text)['forecast']['simpleforecast']['forecastday']:
        query = db.session.query(db.base.classes.forecast).filter_by(month=item['date']['month'], 
                                                                  day=item['date']['day'], 
                                                                  year=item['date']['year']).delete()


        data = db.base.classes.forecast(month=item['date']['month'],
                                        day=item['date']['day'],
                                        year=item['date']['year'],
                                        high=item['high']['fahrenheit'],
                                        low=item['low']['fahrenheit'],
                                        conditions=item['icon'],
                                        pop=item['pop'])

        db.session.add(data)


    db.session.commit()



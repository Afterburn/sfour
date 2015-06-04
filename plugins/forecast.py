import logging
import json
import datetime

logger = logging.getLogger()

def execute(db, **args):




    now = datetime.datetime.now().day


    if 'clear_weather' in args:
        days = args['clear_weather']['days']
        pop  = args['clear_weather']['pop']

        query = db.session.query(db.base.classes.forecast).filter(db.base.classes.forecast.day <= days)

        for forecast in query:
            if not forecast.pop <= pop:
                return False


        if 'notify' in args:
            args['message'] = 'Less than %s%% chance of rain for the next %s days' % (pop, days)
            args['plugins']('notify').execute(db, **args)
            







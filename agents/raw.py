import logging
import datetime
from jinja2 import Environment, FileSystemLoader


#https://pythonhosted.org/feedparser/
logger = logging.getLogger()
env    = Environment()

def execute(db, **args):
    databases = {}

    for key in db.base.metadata.tables.keys():
        databases[key] = getattr(db.base.classes, key)

    now = datetime.datetime.now()
    

        

        


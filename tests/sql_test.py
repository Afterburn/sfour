import datetime

from sql.db_connect import Connect
from main import ConfigManager

config   = ConfigManager()
settings = config.get_settings()



db = Connect(settings['db_path'])

query = db.session.query(db.base.classes.rss.title, db.base.classes.rss.id).filter_by(title='Current Watches, Warnings and Advisories for the United States Issued by the National Weather Service').first()

entry = db.base.classes.entry(summary_detail='test', published=datetime.datetime.now(), parent_id=query.id)

session = db.base.classes.rss(title='test')

print(dir(session))



db.session.add(entry)
db.session.commit()


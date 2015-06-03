from sqlalchemy import Column, Integer, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from sql import items_schema, rss_schema, forecast_schema


Base   = declarative_base()
engine = create_engine('sqlite:///items.db', echo=True)

#items_schema.Base.metadata.create_all(engine)
rss_schema.Base.metadata.create_all(engine)
forecast_schema.Base.metadata.create_all(engine)

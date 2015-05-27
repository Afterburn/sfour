from . import *

class Entry(Base):
    __tablename__ = "entry"
    id             = Column(Integer, primary_key=True)
    parent_id      = Column(Integer, ForeignKey('rss.id'))
    summary_detail = Column(String)
    published      = Column(DateTime)
    url            = Column(String)


class RSS(Base):
    __tablename__ = "rss"
    id      = Column(Integer, primary_key=True)
    title   = Column(String, unique=True)
    entries = relationship('Entry', backref='rss', lazy='dynamic')

    def __unicode__(self):
        return self.id



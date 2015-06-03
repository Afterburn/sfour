from . import *

class Items(Base):
    __tablename__ = "forecast"
    id      = Column(Integer, primary_key=True)
    day     = Column(Integer)
    month   = Column(Integer)
    year    = Column(Integer)
    high    = Column(Float)
    low     = Column(Float)
    pop     = Column(Integer)
    conditions = Column(String)



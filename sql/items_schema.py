from . import *

class Items(Base):
    __tablename__ = "items"
    id      = Column(Integer, primary_key=True)
    name    = Column(String)
    value   = Column(String)



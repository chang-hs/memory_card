from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, DeclarativeBase

class Base(DeclarativeBase):
    pass

engine = create_engine('sqlite:///op_schedule.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base.query = db_session.query_property()

def init_db(app):
    import models
    Base.metadata.create_all(bind=engine)
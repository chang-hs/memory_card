from typing import List
from sqlalchemy.sql import functions
from sqlalchemy import String, Date, Time, Integer, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from db import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, DeclarativeBase
from flask_login import UserMixin

class Base(DeclarativeBase):
    pass

engine = create_engine('sqlite:///memory_card.db')

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base.query = db_session.query_property()

class Card(Base):
    __tablename__="card"
    id: Mapped[int] = mapped_column(primary_key=True)
    lang: Mapped[str] = mapped_column(String)
    word: Mapped[str] = mapped_column(String)
    func: Mapped[str] = mapped_column(String, nullable=True)
    meaning: Mapped[str] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=functions.now())
    learnt: Mapped[bool] = mapped_column(Boolean, default=False)
    difficulty: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self) -> str:
        return f"Word: {self.word}"
    
class User(Base, UserMixin):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f"User {self.username}"
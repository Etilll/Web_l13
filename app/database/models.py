from sqlalchemy import Column, Integer, String, Date, Boolean, func, Table, UniqueConstraint
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .db import Base, engine

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String, default=None)
    mail = Column(String, default=None)
    phone = Column(String)
    birthday = Column(Date, default=None)
    owner = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'))
    theuser = relationship("User", backref="contacts")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    avatar = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)


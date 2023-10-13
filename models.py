# coding: utf-8
from typing import Annotated

from fastapi import Depends
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.orm import relationship, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

engine = create_engine('mysql+mysqlconnector://root:@localhost/svelteluentodb')
session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False, unique=True)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(45), nullable=False, unique=True)
    password = Column(MEDIUMTEXT, nullable=False)
    roles_id = Column(ForeignKey('roles.id', ondelete='CASCADE'), nullable=False, index=True)
    access_token_identifier = Column(String(45))
    refresh_token_identifier = Column(String(45))

    roles = relationship('Role')


class TodoList(Base):
    __tablename__ = 'todo_lists'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    users_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    users = relationship('User')


class TodoItem(Base):
    __tablename__ = 'todo_items'

    id = Column(Integer, primary_key=True)
    body = Column(String(45))
    done_date = Column(DateTime)
    todo_lists_id = Column(ForeignKey('todo_lists.id', ondelete='CASCADE'), nullable=False, index=True)

    todo_lists = relationship('TodoList')


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


Db = Annotated[Session, Depends(get_db)]

#!/usr/bin/env python3
"""This module defines an SQLAlchemy model named User"""


from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    Class User represents a user columns for mySQL table

    __tablename__: name of table
    id: user id
    email: user email
    hashed_password: user's encrypted/hashed password
    seesion_id: id of session
    reset_token: reset token
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    seesion_id = Column(String(250))
    reset_token = Column(String(250))

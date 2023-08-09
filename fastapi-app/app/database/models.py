# -*- encoding: utf-8 -*-
import datetime
import uuid
import sys
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.ext.declarative import declarative_base

sys.dont_write_bytecode = True

base = declarative_base()

class user(base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    mail_address = Column(String(255))
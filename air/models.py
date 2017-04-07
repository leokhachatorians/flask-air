import sqlalchemy
from sqlalchemy import (
        Column, Integer, String, ForeignKey,
)

from sqlalchemy.orm import (
        mapper, relationship, backref
)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

#class User(Model):
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return "<User {}>".format(self.username)

#class Sheets(Model):
class Sheets(Base):
    __tablename__ = 'sheets'
    id = Column(Integer, primary_key=True)
    user_id =  Column(Integer)
    sheet_name = Column(String(180), unique=True)

    def __init__(self, user_id, sheet_name):
        self.user_id = user_id
        self.sheet_name = sheet_name

    def __repr__(self):
        return "<User's:{} Sheet_Name:{}>".format(
                self.user_id,
                self.sheet_name)

#class Sheets_Schema(Model):
class Sheets_Schema(Base):
    __tablename__ = 'sheets_schema'
    id = Column(Integer, primary_key=True)
    sheet_id = Column(Integer, ForeignKey("sheets.id"))
    sheet = relationship('Sheets',
            backref=backref('sheets_schema', lazy='dynamic'))
    column_name = Column(String(150), unique=True)
    column_type = Column(String(80))
    column_num = Column(Integer)

    def __init__(self, sheet, column_name, column_type, column_num):
        self.sheet = sheet
        self.column_name = column_name
        self.column_type = column_type
        self.column_num = column_num

    def __repr__(self):
        return "<Sheets_Schema {} {} {} {}>".format(
                self.sheet, self.column_name, self.column_type,
                self.column_num)

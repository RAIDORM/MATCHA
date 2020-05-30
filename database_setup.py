import sys
# for creating the mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

# for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# for creating foreign key relationship between the tables
from sqlalchemy.orm import relationship

# for configuration
from sqlalchemy import create_engine

# create declarative_base instance
Base = declarative_base()

# we'll add classes here

# creates a create_engine instance at the bottom of the file
engine = create_engine('sqlite:///R:\\MATCHA-master\\database.db?check_same_thread=False')

Base.metadata.create_all(engine)

# we create the class Book and extend it from the Base Class.


class users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    tickets = Column(Integer, nullable=False)
    uid = Column(String(250))
    bip_card_time = Column(String(250))
    password = Column(String(250), nullable=False)
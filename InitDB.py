from sqlalchemy import create_engine, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///test.db')
metadata = MetaData()
Base = declarative_base()

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    status = Column(String)
    role = Column(String)

class Tasks(Base):
    __tablename__ = "Tasks"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id')) 
    deadline = Column(String)
    theme = Column(String)
    message = Column(String)
    status = Column(String)

Base.metadata.create_all(engine)

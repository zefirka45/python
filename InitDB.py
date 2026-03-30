from sqlalchemy import create_engine, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import declarative_base,relationship

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
    applicant_id = Column(Integer, ForeignKey('Users.id')) #Заявитель
    executor_id = Column(Integer, ForeignKey('Users.id')) #Испольнитель
    deadline = Column(String)
    theme = Column(String)
    message = Column(String)
    status = Column(String)

    #Связь между классами
    applicant = relationship("User", foreign_keys=[applicant_id])
    executor = relationship("User", foreign_keys=[executor_id])

Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DATETIME, Boolean, BigInteger, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
import json, datetime, random

DeclBase = declarative_base()


class Task(DeclBase):
    __tablename__ = "Task"
    ID = Column(Integer, primary_key=True)
    StatusID = Column(Integer)
    Context = Column(String)
    EmployeeID = Column(Integer)
    Comments = Column(String)
    StartTime = Column(DATETIME, default=datetime.datetime.utcnow())
    EndTime = Column(DATETIME)



class TaskStatus(DeclBase):
    __tablename__ = "TaskStatus"
    ID = Column(Integer, primary_key=True)
    Name = Column(String)
    IsView = Column(Integer)


class Employee(DeclBase):
    __tablename__ = "Employee"
    ID = Column(Integer, primary_key=True)
    Name = Column(String)
    LastName = Column(String)
    TelegramID = Column(BigInteger)
    TelegramChatID = Column(BigInteger)
    Birthday = Column(DATETIME)
    BranchShopID = Column(Integer)
    PostID = Column(Integer)
    TimeTraking = Column(Boolean)


class BranchShop(DeclBase):
    __tablename__ = "BranchShop"
    ID = Column(Integer, primary_key=True)
    Adress = Column(String)
    Town = Column(String)

class TimeTrakingStatus(DeclBase):
    __tablename__ = "TimeTrakingStatus"
    ID = Column(Integer, primary_key=True)
    Name = Column(String)

class TimeTraking(DeclBase):
    __tablename__ = "TimeTraking"
    ID = Column(Integer, primary_key=True)
    EmployeeID = Column(Integer, ForeignKey(Employee.ID))
    DayTime = Column(DateTime(timezone=False))
    Status = Column(Integer, ForeignKey(TimeTrakingStatus.ID))





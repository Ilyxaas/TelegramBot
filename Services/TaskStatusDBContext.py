from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Column, Integer, String, DATETIME, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB, psycopg2
from sqlalchemy.orm import Session
import json, datetime, random

from Models import Models


class TaskStatusDBContext:
    def __init__(self):
        self.engine = create_engine("postgresql+psycopg2://ilya:Password@localhost/SergeyDiplomaProject")
        self.session = Session(bind=self.engine)

    def GetStatusTask(self, StatusID):
        TaskStatus = self.session.query(Models.TaskStatus).get(StatusID)
        return TaskStatus.Name

    def GetStatusTask_List(self):
        lst = self.session.query(Models.TaskStatus).filter(Models.TaskStatus.IsView == 1).all()
        result = []
        for element in lst:
            result.append(element.Name)
        return result



from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Column, Integer, String, DATETIME, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB, psycopg2
from sqlalchemy.orm import Session
import json, datetime, random

from Models import Models
from Services import TimeServices

class TaskDBContext:

    def __init__(self):
        self.engine = create_engine("postgresql+psycopg2://ilya:Password@localhost/SergeyDiplomaProject")
        self.session = Session(bind=self.engine)

    def Insert(self, _EndTime, _TelegramID, _Contex):
        try:
            EmployeeID = self.session.query(Models.Employee.ID).filter(Models.Employee.TelegramID == _TelegramID).first()
            task = Models.Task()
            task.StatusID = 1
            task.Context = _Contex
            task.EmployeeID = EmployeeID[0]
            task.EndTime = _EndTime
            task.StartTime = datetime.datetime.utcnow()
            task.Comments = ""

            self.session.add(task)
            self.session.commit()
        except:
            print(f"Insert Task Error EmployeeID = {EmployeeID} Task Object = {task}")

    def DeleteTask(self, TaskID):
        Task = self.session.query(Models.Task).get(TaskID)
        try:
            self.session.delete(Task)
            self.session.commit()
        except:
            print(f"Delete Task Error Task ID = {TaskID} Task Object = {Task}")

    def UpdateStatus(self, StatusID, _TaskID, _Comments=""):
        try:
            print("UpdateStatus")
            _Task = self.session.query(Models.Task).get(_TaskID)
            if _Task is not None:
                _Task.StatusID = StatusID
                _Task.Comments = _Comments
                self.session.add(_Task)
                self.session.commit()
        except:
            print(f"Update Status Task Error. Task object = {_Task}")

    def CountTasks(self, _EmployeeID):
        return self.session.query(Models.Task).filter(Models.Task.EmployeeID == _EmployeeID).count()

    def GetAllTasks(self, _EmployeeID):
        Tasks = self.session.query(Models.Task).filter(Models.Task.EmployeeID == _EmployeeID).all()
        print(Tasks)
        return Tasks

    def GetTask(self, TaskID, EmployeeID) -> Models.Task:
        print(f"TaskId ={TaskID}   EmployeeID={EmployeeID}")
        Task = self.session.query(Models.Task). \
            filter(Models.Task.ID == TaskID and Models.Task.EmployeeID == EmployeeID).first()
        return Task

    def GetAllTasks_ID_InCurrentDay(self, _EmployeeID) -> []:
        Count = self.session.query(Models.Task).filter(Models.Task.EmployeeID == _EmployeeID and
                                                       Models.Task.StartTime < datetime.datetime.utcnow()).count()
        if Count > 0:
            Tasks = self.session.query(Models.Task).filter(Models.Task.EmployeeID == _EmployeeID and
                                                           Models.Task.StartTime < datetime.datetime.utcnow()).all()
            ResultID = []

            for Task in Tasks:
                ResultID.append(Task.ID)

            return ResultID
        else:
            return []

    def GetAllTasks_InCurrentDay(self, _EmployeeID) -> []:
        Count = self.session.query(Models.Task).filter(Models.Task.EmployeeID == _EmployeeID and
                                                       Models.Task.EndTime >= datetime.datetime.utcnow()).count()
        if Count > 0:
            Tasks = self.session.query(Models.Task).filter(Models.Task.EmployeeID == _EmployeeID and
                                                           Models.Task.EndTime >= datetime.datetime.utcnow()).all()
            ResultID = []

            for Task in Tasks:
                if TimeServices.TimeServices.CompareDate(Task.EndTime, datetime.datetime.utcnow()):
                    ResultID.append(Task)

            return ResultID
        else:
            return []

    def GetAll_ActiveTasks_InCurrentDay(self, _EmployeeID) -> []:
        Count = self.session.query(Models.Task).filter(Models.Task.EmployeeID == _EmployeeID and
                                                       Models.Task.EndTime >= datetime.datetime.utcnow()).count()
        if Count > 0:
            Tasks = self.session.query(Models.Task).filter(Models.Task.EmployeeID == _EmployeeID and
                                                           Models.Task.EndTime >= datetime.datetime.utcnow()).all()
            ResultID = []

            for Task in Tasks:
                if TimeServices.TimeServices.CompareDate(Task.EndTime, datetime.datetime.utcnow()) and Task.StatusID in [0, 1, 3]:
                    ResultID.append(Task)

            return ResultID
        else:
            return []

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Column, Integer, String, DATETIME, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB, psycopg2
from sqlalchemy.orm import Session
import json, datetime, random
from Services import TimeServices
from Models import Models


class TimeTrakingDBContext:
    def __init__(self):
        self.engine = create_engine("postgresql+psycopg2://ilya:Password@localhost/SergeyDiplomaProject")
        self.session = Session(bind=self.engine)

    def Insert(self, EmployeeID, Status):

            Traking = Models.TimeTraking()
            Traking.EmployeeID = EmployeeID
            Traking.Status = Status
            Traking.DayTime = TimeServices.TimeServices.GetCurrentDayTime()
            self.session.add(Traking)
            self.session.commit()

    def LastTrakingFromPeople(self, EmployeeID):
        ID = self.session.query(func.max(Models.TimeTraking.ID).
                                filter(Models.TimeTraking.EmployeeID == EmployeeID)).all()[0][0]
        return self.session.query(Models.TimeTraking).get(ID)

    def CurrentStatusTrakingName(self, ID):
        print(f"StatusID = {ID}")
        return self.session.query(Models.TimeTrakingStatus).get(ID).Name


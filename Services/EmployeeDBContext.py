
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Column, Integer, String, DATETIME, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB, psycopg2
from sqlalchemy.orm import Session
import json, datetime, random

from Models import Models


class EmployeeDBContext:
    def __init__(self):
        self.engine = create_engine("postgresql+psycopg2://ilya:Password@localhost/SergeyDiplomaProject")
        self.session = Session(bind=self.engine)

    def IsAdmin(self, ID):
        _Task = self.session.query(Models.Employee).get(ID)
        if _Task is None:
            return None

        if _Task.PostID == 1:
            return True
        else:
            return False

    def IsAdmin(self, TelegramID):
        _Task = self.session.query(Models.Employee).filter(Models.Employee.TelegramID == TelegramID)
        if _Task is None:
            return None

        if _Task[0].PostID == 1:
            return True
        else:
            return False

    def SetChatIDIfEmpty(self, TelegramID, ChatID):
        _Task = self.session.query(Models.Employee).filter(Models.Employee.TelegramID == TelegramID).first()
        print(_Task.TelegramChatID)
        if _Task is not None:
            if _Task.TelegramChatID is None:
                _Task.TelegramChatID = ChatID
                self.session.commit()


    def IsExist(self, ID):
        _Task = self.session.query(Models.Employee).get(ID)
        if _Task is None:
            return False
        else:
            return True

    def IsExist(self, TelegramID):
        _Task = self.session.query(Models.Employee).filter(Models.Employee.TelegramID == TelegramID).count()
        if _Task == 0:
            return False
        else:
            return True

    def GetEmployee(self, TelegramID):
        Employee = self.session.query(Models.Employee).filter(Models.Employee.TelegramID == TelegramID).first()
        if Employee is not None:
            return Employee
        else:
            return None

    def GetEmployeeInTown(self, Town):
        ShopID = []
        ShopIDquerry = self.session.query(Models.BranchShop.ID).filter(Models.BranchShop.Town == Town).all()
        for i in ShopIDquerry:
            for j in i:
                ShopID.append(j)

        Employees = self.session.query(Models.Employee).all()
        result = []
        for i in Employees:
            if i.BranchShopID in ShopID:
                result.append(i)
        return result

    def IsExist(self, Name, LName, Town):
        ShopID = []
        ShopIDquerry = self.session.query(Models.BranchShop.ID).filter(Models.BranchShop.Town == Town).all()
        for i in ShopIDquerry:
            for j in i:
                ShopID.append(j)

        Employees = self.session.query(Models.Employee).filter(Models.Employee.Name == Name and Models.Employee.LastName == LName).all()
        result = []
        telegram = None
        for i in Employees:
            if i.BranchShopID in ShopID:
                result.append(i)
        if len(result) == 1:
            telegram = result[0].TelegramID
        print(result)
        return bool(len(result) > 0), telegram














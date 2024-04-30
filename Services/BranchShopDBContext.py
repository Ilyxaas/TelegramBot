from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Column, Integer, String, DATETIME, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB, psycopg2
from sqlalchemy.orm import Session
import json, datetime, random

from Models import Models


class BranchShopDBContext:
    def __init__(self):
        self.engine = create_engine("postgresql+psycopg2://ilya:Password@localhost/SergeyDiplomaProject")
        self.session = Session(bind=self.engine)

    def GetTowns(self):
        result = []
        resultQuery = self.session.query(Models.BranchShop.Town).group_by(Models.BranchShop.Town).all()
        for i in resultQuery:
            for j in i:
                result.append(j)
        return result

    def GetShopsInTown(self, Town):
        return self.session.query(Models.BranchShop.ID).filter(Models.BranchShop.Town == Town).all()

    def ExistsTown(self, Town):
        print(Town)
        res = self.session.query(Models.BranchShop).filter(Models.BranchShop.Town == Town).all()
        print(res)
        if len(res) > 0:
            return True
        else:
            False

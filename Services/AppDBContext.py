from Services import TaskDBContext, EmployeeDBContext, TaskStatusDBContext, BranchShopDBContext, TimeServices, \
    TimeTrakingDBContext


class AppDBContext:
    def __init__(self):
        self.__Task = TaskDBContext.TaskDBContext()
        self.__Employee = EmployeeDBContext.EmployeeDBContext()
        self.__TaskStatus = TaskStatusDBContext.TaskStatusDBContext()
        self.__BranchShop = BranchShopDBContext.BranchShopDBContext()
        self.__TimeTraking = TimeTrakingDBContext.TimeTrakingDBContext()

        self.__Time = TimeServices.TimeServices()

    def GetTask(self):
        return self.__Task

    def GetEmployee(self):
        return self.__Employee

    def GetTaskStatus(self):
        return self.__TaskStatus

    def GetBranchShop(self):
        return self.__BranchShop

    def GetTime(self):
        return self.__Time

    def GetTimeTraking(self):
        return self.__TimeTraking

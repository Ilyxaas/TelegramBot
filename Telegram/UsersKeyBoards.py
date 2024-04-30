from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from Services import AppDBContext


class UsersKeyBoard:
    def __init__(self):
        self.AppDB = AppDBContext.AppDBContext()
        print("Bot Started...")

    def TrakingKeyBoard(self, Status):
        kb = []
        if Status == 0:
            kb.append([types.KeyboardButton(text="Закончить работу")])
            kb.append([types.KeyboardButton(text="Ушёл на перерыв")])
        elif Status == 1:
            kb.append([types.KeyboardButton(text="Начать работу")])
        elif Status == 2:
            kb.append([types.KeyboardButton(text="Пришёл с перерыва")])
        elif Status == 3:
            kb.append([types.KeyboardButton(text="Закончить работу")])
        kb.append([types.KeyboardButton(text="В главное меню")])
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder="Что будем делать..."
        )
        return keyboard



    def MainKeyBoard(self, TelegramID):
        Employee = self.AppDB.GetEmployee().GetEmployee(TelegramID=TelegramID)
        if Employee is not None:
            if Employee.TimeTraking == True:
                kb = [
                    [
                        types.KeyboardButton(text="Отслеживание рабочего времени")
                    ],
                ]
                keyboard = types.ReplyKeyboardMarkup(
                    keyboard=kb,
                    resize_keyboard=True,
                    input_field_placeholder="Что будем делать..."
                )
                return keyboard
            if Employee.PostID == 1:

                kb = [
                    [
                        types.KeyboardButton(text="Активные задачи"),
                        types.KeyboardButton(text="Отчёт по задаче")
                    ],
                ]
                keyboard = types.ReplyKeyboardMarkup(
                    keyboard=kb,
                    resize_keyboard=True,
                    input_field_placeholder="Что будем делать..."
                )
                return keyboard
            elif Employee.PostID == 0:
                    kb = [
                        [
                            types.KeyboardButton(text="Добавить задачу"),
                            types.KeyboardButton(text="Удалить задачу")
                        ],
                    ]
                    keyboard = types.ReplyKeyboardMarkup(
                        keyboard=kb,
                        resize_keyboard=True,
                        input_field_placeholder="Что будем делать..."
                    )
                    return keyboard
        return None

    def WelcomeMessage(self, TelegramID):
        Employee = self.AppDB.GetEmployee().GetEmployee(TelegramID=TelegramID)
        if Employee is None:
            return "Вы не являетесь авторизованным пользователем, пожалуйста обратитесь к администратору для выдачи " \
                   "роли.", None
        else:
            return f"Добрый день {Employee.Name} {Employee.LastName}! \n  Приступим к работе.", Employee

    def TownsKeyboard(self, TelegramID):
        Employee = self.AppDB.GetEmployee().GetEmployee(TelegramID=TelegramID)
        if Employee is None:
            return "Вы не являетесь авторизованным пользователем, пожалуйста обратитесь к администратору для выдачи " \
                   "роли. "
        if Employee.PostID == 0:
            Towns = self.AppDB.GetBranchShop().GetTowns()
            kb = []
            for element in Towns:
                kb.append([types.KeyboardButton(text=str(element))])
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            return keyboard

    def PepopleInTownsKeyboard(self, TelegramID, Town):
        Employee = self.AppDB.GetEmployee().GetEmployee(TelegramID=TelegramID)
        if Employee.PostID == 0:
            users = self.AppDB.GetEmployee().GetEmployeeInTown(Town)
            kb = []
            for element in users:
                kb.append([types.KeyboardButton(text=str(element.LastName + " " + element.Name))])
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True)
            return keyboard

    def TimeTaskEndKeyboard(self):
        kb = []
        kb.append([types.KeyboardButton(text="До конца текущего дня")])
        kb.append([types.KeyboardButton(text="До конца следующего дня")])
        kb.append([types.KeyboardButton(text="До конца недели")])
        kb.append([types.KeyboardButton(text="До конца месяца")])
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        return keyboard

    def ApplyOrRepeatKeyboard(self):
        kb = []
        kb.append([types.KeyboardButton(text="Отправить задачу")])
        kb.append([types.KeyboardButton(text="Заполнить задачу заново")])
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        return keyboard

    def ApplyOrDeleteKeyboard(self):
        kb = []
        kb.append([types.KeyboardButton(text="Удалить")])
        kb.append([types.KeyboardButton(text="Вернуться обратно")])
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        return keyboard







    def TasksEmployers(self, TelegramID):
        Employee = self.AppDB.GetEmployee().GetEmployee(TelegramID=TelegramID)
        print(Employee)
        if Employee is None:
            return "Вы не являетесь авторизованным пользователем, пожалуйста обратитесь к администратору для выдачи " \
                   "роли. "
        if Employee.PostID != 1:
            return "Данный функционал не соответствует вашему статусу."
        else:

            Tasks = self.AppDB.GetTask().GetAll_ActiveTasks_InCurrentDay(Employee.ID)
            Message = f"{Employee.Name}, на данный момент у вас <b>{len(Tasks)}</b> активных задач. \n"
            print(Tasks)
            if len(Tasks) > 0:
                for Task in Tasks:
                    TaskMessage = f"\nНомер задачи: <b>{Task.ID}</b> \n Задание: <b>{Task.Context}</b> \n Статус работы: " \
                          f"<b>{self.AppDB.GetTaskStatus().GetStatusTask(Task.StatusID)}</b>" \
                          f"\n Задача поставлена: <b>{Task.StartTime}</b> \n Выполнить до: <b>{Task.EndTime}</b> \n"
                    Message += TaskMessage
                return Message
            else:
                return "На данный момент у вас нет активных задач."

    def TasksEmployersRemove(self, TelegramID):
        Employee = self.AppDB.GetEmployee().GetEmployee(TelegramID=TelegramID)
        if Employee is None:
            return "Вы не являетесь авторизованным пользователем, пожалуйста обратитесь к администратору для выдачи " \
                   "роли. ", None, None
        if Employee.PostID == 1:
            return "Данный функционал не соответствует вашему статусу.", None, None

        Count = self.AppDB.GetTask().CountTasks(Employee.ID)
        Message = ""
        kb = []
        if Count > 0:
            Tasks = self.AppDB.GetTask().GetAllTasks_InCurrentDay(Employee.ID)

        TaskIDs = []
        print("Tasks: " + str(Tasks))
        for Task in Tasks:
            TaskIDs.append(Task.ID)
            kb.append([types.KeyboardButton(text=str(Task.ID))])
            TaskMessage = f"\nНомер задачи: <b>{Task.ID}</b> \n Задание: <b>{Task.Context}</b> \n Статус работы: " \
                          f"<b>{self.AppDB.GetTaskStatus().GetStatusTask(Task.StatusID)}</b>" \
                          f"\n Задача поставлена: <b>{Task.StartTime}</b> \n Выполнить до: <b>{Task.EndTime}</b> \n"
            Message += TaskMessage
            Keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        return Message, Keyboard, TaskIDs

    def OneTaskEmployers(self, TaskID, TelegramID):
        Message = ""
        Employee = self.AppDB.GetEmployee().GetEmployee(TelegramID=TelegramID)
        if Employee is None:
            Message = "Для вас нет такой задачи"
        else:
            Task = self.AppDB.GetTask().GetTask(EmployeeID=Employee.ID, TaskID=TaskID)
        if Task is None:
            Message = "Для вас нет такой задачи"
        else:
            TaskMessage = f"\nНомер задачи: <b>{Task.ID}</b> \n Задание: <b>{Task.Context}</b> \n Статус работы: " \
                          f"<b>{self.AppDB.GetTaskStatus().GetStatusTask(Task.StatusID)}</b>" \
                          f"\n Задача поставлена: <b>{Task.StartTime}</b> \n Выполнить до: <b>{Task.EndTime}</b> \n"
            Message += TaskMessage

        return Message

    def make_row_keyboard(self, items: list[str]) -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        for i in items:
            builder.add(types.KeyboardButton(text=str(i)))
        builder.adjust(5)
        return builder.as_markup(resize_keyboard=True)

    def CurrentTasks(self, TelegramID):
        Employee = self.AppDB.GetEmployee().GetEmployee(TelegramID=TelegramID)
        if Employee is not None:
            List = self.AppDB.GetTask().GetAll_ActiveTasks_InCurrentDay(Employee.ID)
            lstId = []
            for i in List:
                lstId.append(i.ID)
            return lstId
        return []

    def IsExistEmployee(self, TelegramID):
        return self.AppDB.GetEmployee().IsExist(TelegramID=TelegramID)

    def NotAuthorizeMessage(self):
        return "Вы не являетесь авторизованным пользователем, пожалуйста обратитесь к администратору для выдачи " \
                   "роли."

    def NoneMessagetaskResultKeyboard(self):
        builder = ReplyKeyboardBuilder().add(types.KeyboardButton(text="Без комментариев"))
        return builder.as_markup(resize_keyboard=True)

    def GetStatusTaskKeyBoard(self):
        list = self.AppDB.GetTaskStatus().GetStatusTask_List()
        kb = []
        for element in list:
            kb.append([types.KeyboardButton(text=str(element))])
        kb.append([types.KeyboardButton(text=str("Оставить как есть"))])
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        return keyboard
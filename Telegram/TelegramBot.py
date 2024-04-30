from aiogram import Bot, Dispatcher, types, Router
from aiogram import F
from aiogram.client import bot
from aiogram.dispatcher import router
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from Telegram import UsersKeyBoards, TaskResult, GenerateTask, DeleteTask, SenderMessages, Traking

dp = Dispatcher()
UsersUI = UsersKeyBoards.UsersKeyBoard()
Sender = SenderMessages.SendMessange()
router = Router()




class TelegramBot:

    def __init__(self):
        self.Token = "6782006016:AAHXVUYS9kKqJ4UK4fGfFMwYOB3kufl8r28"
        self.bot = Bot(token=self.Token)
        Sender.SetBot(self.bot)


    @dp.message(Command("start"))
    async def cmd_start(message: types.Message, state: FSMContext):
        await state.set_state(None)
        WelcomeMessage, Employee = UsersUI.WelcomeMessage(message.from_user.id)
        if Employee is not None:
            keyboard = UsersUI.MainKeyBoard(Employee.TelegramID)
            await message.answer(WelcomeMessage, reply_markup=keyboard)
            UsersUI.AppDB.GetEmployee().SetChatIDIfEmpty(message.from_user.id, message.chat.id)
        else:
            await message.answer(WelcomeMessage)


    @dp.message(F.text == "Отслеживание рабочего времени")
    async def cmd_StartTimeTraking(message: types.Message, state: FSMContext):
        Employee = UsersUI.AppDB.GetEmployee().GetEmployee(TelegramID=message.from_user.id)
        if Employee is not None and Employee.TimeTraking is True:
            await state.update_data(EmployeeID=Employee.ID)
            keyboard = UsersUI.TownsKeyboard(message.from_user.id)
            await state.set_state(Traking.Traking.choosing_Town)
            await message.answer("Выберите соответствующий город", reply_markup=keyboard)
        else:
            WelcomeMessage, Employee = UsersUI.WelcomeMessage(message.from_user.id)
            if Employee is not None:
                keyboard = UsersUI.MainKeyBoard(Employee.TelegramID)
            await message.answer(WelcomeMessage, reply_markup=keyboard)

    @dp.message(StateFilter(Traking.Traking.choosing_Town))
    async def cmd_TownTimeTraking(message: types.Message, state: FSMContext):
        await state.update_data(TelegramID=message.from_user.id)
        if UsersUI.AppDB.GetBranchShop().ExistsTown(Town=message.text):
            await state.update_data(Town=message.text)
            keyboard = UsersUI.PepopleInTownsKeyboard(message.from_user.id, message.text)
            await state.set_state(Traking.Traking.choosing_People)
            await message.answer("Выберите сотрудника", reply_markup=keyboard)
        else:
            await message.answer("Город выбран не верно, укажите верные данные")
            keyboard = UsersUI.TownsKeyboard(message.from_user.id)
            await state.set_state(DeleteTask.DeleteTask.choosing_Town)
            await message.answer("Выберите соответствующий город", reply_markup=keyboard)

    @dp.message(StateFilter(Traking.Traking.choosing_People))
    async def cmd_PeopleTimeTraking(message: types.Message, state: FSMContext):
        Mes = message.text.split(' ')
        TaskData = await state.get_data()

        Exist, _TelegramID = UsersUI.AppDB.GetEmployee().IsExist(Mes[1], Mes[0], TaskData['Town'])
        if Exist:
            Employee = UsersUI.AppDB.GetEmployee().GetEmployee(TelegramID=message.from_user.id)
            LastTraking = UsersUI.AppDB.GetTimeTraking().LastTrakingFromPeople(EmployeeID= Employee.ID)
            keyboard = UsersUI.TrakingKeyBoard(Status=LastTraking.Status)
            StatusName = UsersUI.AppDB.GetTimeTraking().CurrentStatusTrakingName(LastTraking.Status)
            await message.answer(f"Ваше рабочее состояние: {StatusName}", reply_markup=keyboard)
            await state.set_state(Traking.Traking.chosing_Status)
        else:
            await message.answer("Такого Сотрудника не существует, укажите верные данные")
            keyboard = UsersUI.PepopleInTownsKeyboard(message.from_user.id, TaskData['Town'])
            await state.set_state(Traking.Traking.choosing_People)
            await message.answer("Выберите сотрудника", reply_markup=keyboard)

    @dp.message(StateFilter(Traking.Traking.chosing_Status))
    async def cmd_SetTimetraking(message: types.Message, state: FSMContext):
        async def GoToMainMenu(message: types.Message, state: FSMContext):
            await state.set_state(None)
            keyboard = UsersUI.MainKeyBoard(TaskData['TelegramID'])
            await message.answer("Продолжим работу", reply_markup=keyboard)

        TaskData = await state.get_data()
        if message.text == "Закончить работу":
            UsersUI.AppDB.GetTimeTraking().Insert(TaskData['EmployeeID'], 1)
            await GoToMainMenu(message, state)
            return
        elif message.text == "Ушёл на перерыв":
            UsersUI.AppDB.GetTimeTraking().Insert(TaskData['EmployeeID'], 2)
            await GoToMainMenu(message, state)
            return
        elif message.text == "Начать работу":
            UsersUI.AppDB.GetTimeTraking().Insert(TaskData['EmployeeID'], 0)
            await GoToMainMenu(message, state)
            return
        elif message.text == "Пришёл с перерыва":
            UsersUI.AppDB.GetTimeTraking().Insert(TaskData['EmployeeID'], 3)
            await GoToMainMenu(message, state)
            return
        elif message.text == "В главное меню":
            await GoToMainMenu(message, state)
            return
        else:
            pass









    @dp.message(F.text.lower() == "добавить задачу")
    async def cmd_Newtask(message: types.Message, state: FSMContext):
        keyboard = UsersUI.TownsKeyboard(message.from_user.id)
        await state.set_state(GenerateTask.GenerateTask.choosing_Town)
        await message.answer("Выберите соответствующий город", reply_markup=keyboard)

    @dp.message(F.text == "Удалить задачу")
    async def cmd_Newtask(message: types.Message, state: FSMContext):
        keyboard = UsersUI.TownsKeyboard(message.from_user.id)
        await state.set_state(DeleteTask.DeleteTask.choosing_Town)
        await message.answer("Выберите соответствующий город", reply_markup=keyboard)

    @dp.message(StateFilter(DeleteTask.DeleteTask.choosing_Town))
    async def cmd_TownStateRemoveTask(message: types.Message, state: FSMContext):

        if UsersUI.AppDB.GetBranchShop().ExistsTown(Town=message.text):
            await state.update_data(Town=message.text)
            keyboard = UsersUI.PepopleInTownsKeyboard(message.from_user.id, message.text)
            await state.set_state(DeleteTask.DeleteTask.choosing_People)
            await message.answer("Выберите сотрудника", reply_markup=keyboard)
        else:
            await message.answer("Город выбран не верно, укажите верные данные")
            keyboard = UsersUI.TownsKeyboard(message.from_user.id)
            await state.set_state(DeleteTask.DeleteTask.choosing_Town)
            await message.answer("Выберите соответствующий город", reply_markup=keyboard)

    @dp.message(StateFilter(GenerateTask.GenerateTask.choosing_Town))
    async def cmd_TownStateAddTask(message: types.Message, state: FSMContext):

        if UsersUI.AppDB.GetBranchShop().ExistsTown(Town=message.text):
            await state.update_data(Town=message.text)
            keyboard = UsersUI.PepopleInTownsKeyboard(message.from_user.id, message.text)
            await state.set_state(GenerateTask.GenerateTask.choosing_People)
            await message.answer("Выберите сотрудника", reply_markup=keyboard)
        else:
            await message.answer("Город Выбран не верно, укажите верные данные")
            keyboard = UsersUI.TownsKeyboard(message.from_user.id)
            await state.set_state(GenerateTask.GenerateTask.choosing_Town)
            await message.answer("Выберите соответствующий город", reply_markup=keyboard)

    @dp.message(StateFilter(GenerateTask.GenerateTask.choosing_People))
    async def cmd_PeopleInTownAddTask(message: types.Message, state: FSMContext):
        Mes = message.text.split(' ')
        TaskData = await state.get_data()
        print(Mes[0] + " " + Mes[1])
        Exist, _TelegramID = UsersUI.AppDB.GetEmployee().IsExist(Mes[1], Mes[0], TaskData['Town'])
        if Exist:
            await state.update_data(TelegramID=_TelegramID)
            await state.update_data(Name=Mes[1])
            await state.update_data(LName=Mes[0])
            await message.answer("Сформулируйте задание:", reply_markup=types.ReplyKeyboardRemove())
            await state.set_state(GenerateTask.GenerateTask.choosing_Task_Description)
        else:
            await message.answer("Такого Сотрудника не существует, укажите верные данные")
            keyboard = UsersUI.PepopleInTownsKeyboard(message.from_user.id, TaskData['Town'])
            await state.set_state(GenerateTask.GenerateTask.choosing_People)
            await message.answer("Выберите сотрудника", reply_markup=keyboard)

    @dp.message(StateFilter(DeleteTask.DeleteTask.choosing_People))
    async def cmd_PeopleInTownRemoveTask(message: types.Message, state: FSMContext):
        Mes = message.text.split(' ')
        TaskData = await state.get_data()
        Exist, _TelegramID = UsersUI.AppDB.GetEmployee().IsExist(Mes[1], Mes[0], TaskData['Town'])
        if Exist:
            Mes, Keyboard, TasksID = UsersUI.TasksEmployersRemove(message.from_user.id)
            if len(TasksID) == 0:
                await message.answer("У данного сотрудника нет активных задач" + Mes,
                                     reply_markup=types.ReplyKeyboardRemove(),
                                     parse_mode=ParseMode.HTML)
                WelcomeMessage, Employee = UsersUI.WelcomeMessage(message.from_user.id)
                if Employee is not None:
                    keyboard = UsersUI.MainKeyBoard(Employee.TelegramID)
                await message.answer("Давай попробуем заново: ", reply_markup=keyboard)
                await state.set_state(None)

            await state.update_data(TasksID=TasksID)
            await state.update_data(TelegramID=_TelegramID)
            await state.update_data(Name=Mes[1])
            await state.update_data(LName=Mes[0])
            await message.answer("Выберите задачу на удаление: \n Вот список задач данного сотрудника: \n" + Mes,
                                 reply_markup=Keyboard,
                                 parse_mode=ParseMode.HTML)
            await state.set_state(DeleteTask.DeleteTask.ApplyDeleteTask)
        else:
            await message.answer("Такого Сотрудника не существует, укажите верные данные")
            keyboard = UsersUI.PepopleInTownsKeyboard(message.from_user.id, TaskData['Town'])
            await state.set_state(GenerateTask.GenerateTask.choosing_People)
            await message.answer("Выберите сотрудника", reply_markup=keyboard)

    @dp.message(StateFilter(DeleteTask.DeleteTask.ApplyDeleteTask))
    async def cmd_ApplyOrRepeatRemoveTask(message: types.Message, state: FSMContext):
        TaskData = await state.get_data()
        TasksID = TaskData['TasksID']
        ExeptCast = False
        try:
            MessageTask = int(message.text)
        except:
            ExeptCast = True
            MessageTask = -1
        if ExeptCast is False and MessageTask in TasksID:
           print("gfgfg")
           await state.update_data(DeleteTaskID=MessageTask)
           Keyboard = UsersUI.ApplyOrDeleteKeyboard()
           await message.answer("Подтвердите удаление:",
                                reply_markup=Keyboard,
                                parse_mode=ParseMode.HTML)
           await state.set_state(DeleteTask.DeleteTask.ConfirmDeleteTask)
        else:
            await message.answer("Задачи с таким номером нет для данного сотрудника. \n Попробуйте еще раз")
            Mes, Keyboard, TasksID = UsersUI.TasksEmployersRemove(message.from_user.id)
            await message.answer("Выберите задачу на удаление: \n Вот список задач данного сотрудника: \n" + Mes,
                                 reply_markup=Keyboard,
                                 parse_mode=ParseMode.HTML)
            await state.set_state(DeleteTask.DeleteTask.ApplyDeleteTask)

    @dp.message(StateFilter(DeleteTask.DeleteTask.ConfirmDeleteTask))
    async def cmd_ConfirmRemoveTask(message: types.Message, state: FSMContext):
        print("Мы тут были")
        if message.text == "Удалить":
            TaskData = await state.get_data()
            IDTask = TaskData['DeleteTaskID']
            UsersUI.AppDB.GetTask().DeleteTask(IDTask)

            WelcomeMessage, Employee = UsersUI.WelcomeMessage(message.from_user.id)
            keyboard = UsersUI.MainKeyBoard(Employee.TelegramID)
            await message.answer("Задача успешна удалена. Работник уже вкурсе об этом", reply_markup=keyboard)
            try:
                await Sender.SendMessageFromPeople(
                    "Список задач бы уменьшен. Советую ознакомиться",
                    UsersUI.AppDB.GetEmployee().GetEmployee(TaskData['TelegramID']).TelegramChatID)
            except:
                await message.answer(
                    "Ошибка отправки сообщения пользователю. Скорее всего работник не находится в чате с ботом",
                    reply_markup=types.ReplyKeyboardRemove())
            await state.set_state(None)

        elif message.text == "Вернуться обратно":
            WelcomeMessage, Employee = UsersUI.WelcomeMessage(message.from_user.id)
            keyboard = UsersUI.MainKeyBoard(Employee.TelegramID)
            await message.answer("Отлично. Возвращаемся обратно", reply_markup=keyboard)
            await state.set_state(None)
        else:
            Keyboard = UsersUI.ApplyOrDeleteKeyboard()
            await message.answer("Нет такого варианта, попробуйте еще раз:",
                                 reply_markup=Keyboard,
                                 parse_mode=ParseMode.HTML)
            await state.set_state(DeleteTask.DeleteTask.ApplyDeleteTask)

    @dp.message(StateFilter(GenerateTask.GenerateTask.choosing_Task_Description))
    async def cmd_TimeTask(message: types.Message, state: FSMContext):

        keyboard = UsersUI.TimeTaskEndKeyboard()
        await state.update_data(TaskText=message.text)
        await message.answer("Укажите срок выполнения в формате даты: <b>гггг-мм-дд</b> или воспользуйтесь "
                             "стандартными:", parse_mode=ParseMode.HTML, reply_markup=keyboard)
        await state.set_state(GenerateTask.GenerateTask.choosing_DateEnd)

    @dp.message(StateFilter(GenerateTask.GenerateTask.choosing_DateEnd))
    async def cmd_ApplyTask(message: types.Message, state: FSMContext):
        async def TrueApplyTask(message: types.Message, state: FSMContext):
            TaskData = await state.get_data()
            keyboard = UsersUI.ApplyOrRepeatKeyboard()
            await state.set_state(GenerateTask.GenerateTask.ApplyTask)
            await message.answer(f"Задание для: <b>{TaskData['Name']} {TaskData['LName']}</b> ({TaskData['Town']}) \n" +
                                 f"<b>Описание</b>: {TaskData['TaskText']} \n" +
                                 f"<b>Выполнить до: {TaskData['EndTime']}</b>:",
                                 parse_mode=ParseMode.HTML, reply_markup=keyboard)

        if message.text == "До конца текущего дня":
            await state.update_data(EndTime=UsersUI.AppDB.GetTime().CurrentDay())
            await TrueApplyTask(message=message, state=state)
        elif message.text == "До конца следующего дня":
            await state.update_data(EndTime=UsersUI.AppDB.GetTime().NextDay())
            await TrueApplyTask(message=message, state=state)
        elif message.text == "До конца недели":
            await state.update_data(EndTime=UsersUI.AppDB.GetTime().EndDayInWeek())
            await TrueApplyTask(message=message, state=state)
        elif message.text == "До конца месяца":
            await state.update_data(EndTime=UsersUI.AppDB.GetTime().EndDayInMonth())
            await TrueApplyTask(message=message, state=state)
        else:
            date, exist = UsersUI.AppDB.GetTime().StringToDateTime(message.text)
            if date is not None and exist is True:
                await state.update_data(EndTime=date)
                await TrueApplyTask(message=message, state=state)
            else:
                await message.answer("Неверный формат данных.")
                keyboard = UsersUI.TimeTaskEndKeyboard()
                await message.answer("Укажите срок выполнения в формате даты: <b>гггг-мм-дд</b> или воспользуйтесь "
                                     "стандартными:", parse_mode=ParseMode.HTML, reply_markup=keyboard)
                await state.set_state(GenerateTask.GenerateTask.choosing_DateEnd)

    @dp.message(StateFilter(GenerateTask.GenerateTask.ApplyTask))
    async def cmd_TimeTask(message: types.Message, state: FSMContext):
        if message.text == "Отправить задачу":
            TaskData = await state.get_data()
            UsersUI.AppDB.GetTask().Insert(_EndTime=TaskData['EndTime'],
                                           _TelegramID=TaskData['TelegramID'], _Contex=TaskData['TaskText'])
            await state.set_state(None)
            WelcomeMessage, Employee = UsersUI.WelcomeMessage(message.from_user.id)
            if Employee is not None:
                keyboard = UsersUI.MainKeyBoard(Employee.TelegramID)
            await message.answer("Задача отправленна. \nЧто будем делать дальше?", reply_markup=keyboard)

            try:
                await Sender.SendMessageFromPeople(
                    "Появилась новая задача. Советую ознакомиться",
                    UsersUI.AppDB.GetEmployee().GetEmployee(TaskData['TelegramID']).TelegramChatID)
            except:
                await message.answer(
                    "Ошибка отправки сообщения пользователю. Скорее всего работник не находится в чате с ботом",
                    reply_markup=types.ReplyKeyboardRemove())
            await state.set_state(None)

        elif message.text == "Заполнить задачу заново":
            keyboard = UsersUI.TownsKeyboard(message.from_user.id)
            await state.set_state(GenerateTask.GenerateTask.choosing_Town)
            await message.answer("Выберите соответствующий город", reply_markup=keyboard)
        else:
            keyboard = UsersUI.ApplyOrRepeatKeyboard()
            await state.set_state(GenerateTask.GenerateTask.ApplyTask)
            await message.answer("Такого варианта не существует попробуйте еще раз",
                                 parse_mode=ParseMode.HTML, reply_markup=keyboard)

    @dp.message(F.text.lower() == "активные задачи")
    async def cmd_ActualTask(message: types.Message):
        TasksMessage = UsersUI.TasksEmployers(message.from_user.id)
        keyboard = UsersUI.MainKeyBoard(message.from_user.id)
        await message.answer(TasksMessage, reply_markup=keyboard, parse_mode="html")

    @dp.message(StateFilter(None), F.text.lower() == "отчёт по задаче")
    async def cmd_food(message: Message, state: FSMContext):
        Employee = UsersUI.AppDB.GetEmployee().GetEmployee(TelegramID=message.from_user.id)
        if Employee is not None:
            lst_ID = UsersUI.CurrentTasks(message.from_user.id)
            if len(lst_ID) > 0:
                await message.answer(
                    text="Выберите задачу:",
                    reply_markup=UsersUI.make_row_keyboard(lst_ID)
                )
                # Устанавливаем пользователю состояние "выбирает название"
                await state.set_state(TaskResult.ResultTask.choosing_Task_ID)
            else:
                await message.answer(
                    text="У вас нет активных задач."
                )
                # Устанавливаем пользователю состояние "выбирает название"
                await state.set_state(None)
        else:
            await message.answer(
                text=f"{UsersUI.NotAuthorizeMessage()}",
            )
            await state.set_state(None)

    @dp.message(TaskResult.ResultTask.choosing_Task_ID)
    async def cmd_GetTaskForStatus(message: Message, state: FSMContext):
        TaskMessage = UsersUI.OneTaskEmployers(int(message.text), message.from_user.id)
        await message.answer(
            text="Задача:" + TaskMessage, parse_mode="html"
        )
        await message.answer(
            text="Выберите статус задачи:",
            reply_markup=UsersUI.GetStatusTaskKeyBoard()
        )
        await state.update_data(Task_ID=message.text.lower())

        await state.set_state(TaskResult.ResultTask.choosing_Task_Comment)

    @dp.message(TaskResult.ResultTask.choosing_Task_Comment)
    async def cmd_UpdateTaskMessage(message: Message, state: FSMContext):
        await state.update_data(Status=message.text.lower())
        await  message.answer(
            "Укажите коментарий к проделанной работе. Или отошлите пустое сообщение для продолжения",
            reply_markup=UsersUI.NoneMessagetaskResultKeyboard()
        )
        await state.set_state(TaskResult.ResultTask.UpdateTaskStatus)

    @dp.message(TaskResult.ResultTask.UpdateTaskStatus)
    async def cmd_UpdateTaskStatus(message: Message, state: FSMContext):
        await state.update_data(Comment=message.text.lower())
        ResMessage = " "
        UserData = await state.get_data()
        if UserData["Comment"] != "без комментариев":
            ResMessage = UserData["Comment"]

        print("Status: " + UserData["Status"] + "|IDTask" + str(UserData["Task_ID"]))
        if (UserData["Status"] == "выполнена"):
            UsersUI.AppDB.GetTask().UpdateStatus(4, UserData["Task_ID"], ResMessage)
        elif (UserData["Status"] == "в работе"):
            UsersUI.AppDB.GetTask().UpdateStatus(0, UserData["Task_ID"], ResMessage)
        elif (UserData["Status"] == "проблема выполнения"):
            UsersUI.AppDB.GetTask().UpdateStatus(3, UserData["Task_ID"], ResMessage)
        elif (UserData["Status"] == "оставить как есть"):
            UsersUI.AppDB.GetTask().UpdateStatus(5, UserData["Task_ID"], ResMessage)

        await message.answer(
            text="Состояние изменено", parse_mode="html"
        )

        WelcomeMessage, Employee = UsersUI.WelcomeMessage(message.from_user.id)
        await state.set_state(None)
        keyboard = UsersUI.MainKeyBoard(Employee.TelegramID)
        await message.answer("Продолжаем работу", reply_markup=keyboard)

    async def main(self):
        await dp.start_polling(self.bot)

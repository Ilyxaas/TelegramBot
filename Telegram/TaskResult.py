from aiogram.fsm.state import StatesGroup, State


class ResultTask(StatesGroup):
    choosing_Task_ID = State()
    choosing_Task_Status = State()
    choosing_Task_Comment = State()
    UpdateTaskStatus = State()



from aiogram.fsm.state import StatesGroup, State


class GenerateTask(StatesGroup):
    choosing_Town = State()
    choosing_People = State()
    choosing_DateEnd = State()
    choosing_Task_Description = State()
    ApplyTask = State()




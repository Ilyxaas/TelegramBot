from aiogram.fsm.state import StatesGroup, State


class DeleteTask(StatesGroup):
    choosing_Town = State()
    choosing_People = State()
    chosing_Task = State()
    ApplyDeleteTask = State()
    ConfirmDeleteTask = State()
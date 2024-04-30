from aiogram.fsm.state import StatesGroup, State


class Traking(StatesGroup):
    choosing_Town = State()
    choosing_People = State()
    chosing_Status = State()

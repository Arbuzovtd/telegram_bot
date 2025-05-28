from aiogram.fsm.state import StatesGroup, State

class Registration(StatesGroup):
    AwaitingPhone = State()

from aiogram.fsm.state import State, StatesGroup

class MebelSG(StatesGroup):
    name = State()
    values = State()

class CostSG(StatesGroup):
    selecting_project = State()
    entering_amount = State()

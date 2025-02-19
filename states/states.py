from aiogram.fsm.state import State, StatesGroup


class WorkAI(StatesGroup):
    process = State()

class Reg(StatesGroup):
    name = State()
    contact = State()

class JobSearch(StatesGroup):
    city = State()
    profession = State()
    schedule = State()
    salary = State()
class Subscribe(StatesGroup):
    ask_subscribe = State()
    time_choose = State()

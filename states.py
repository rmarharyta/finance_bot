from aiogram.fsm.state import State, StatesGroup

class ExpenseState(StatesGroup):
    amount = State()
    category = State()
    confirm = State()

class IncomeState(StatesGroup):
    amount = State()
    confirm = State()

class SavingsState(StatesGroup):
    amount = State()
    confirm = State()
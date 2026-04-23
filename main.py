import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext

from config import TOKEN
from db import init_db
from states import ExpenseState, IncomeState, SavingsState

from handlers.start import start
from handlers.expense import start_expense, get_amount, get_category, confirm
from handlers.income import income_start, income_confirm, income_amount, income_add, income_set 
from handlers.savings import savings_add, savings_amount, savings_confirm, savings_set, show, edit
from handlers.stats import finance_chart, stats_menu, stats_handler

from keyboards import main_kb

bot = Bot(TOKEN)
dp = Dispatcher(storage=MemoryStorage())

async def main():
    await init_db()
    
    # start
    dp.message.register(start, F.text == "/start")

    # expense FSM
    dp.message.register(start_expense, F.text == "➕ Витрата")
    dp.message.register(get_amount, ExpenseState.amount)
    dp.callback_query.register(get_category, ExpenseState.category)
    dp.callback_query.register(confirm, ExpenseState.confirm)

    
    # income
    dp.message.register(income_start, F.text == "💵 Дохід")

    dp.message.register(income_add, F.text == "➕ Додати дохід")
    dp.message.register(income_set, F.text == "💵 Змінити дохід")

    dp.message.register(income_amount, IncomeState.amount)
    dp.callback_query.register(income_confirm, IncomeState.confirm)
    
    # savings
    dp.message.register(show, F.text == "🏦 Заощадження")
    
    dp.message.register(savings_add, F.text == "➕ Додати заощадження")
    dp.message.register(savings_set, F.text == "💰 Змінити заощадження")
    
    dp.message.register(savings_amount, SavingsState.amount)
    dp.callback_query.register(savings_confirm, SavingsState.confirm)    
    # stats
    dp.message.register(stats_menu, F.text == "📊 Статистика")
    dp.callback_query.register(stats_handler)

    dp.message.register(finance_chart, F.text == "📈 Графік")
    
    dp.message.register(back_to_menu, F.text == "⬅ В меню")
    

    await dp.start_polling(bot)

async def back_to_menu(message, state: FSMContext):
    await state.clear()
    await message.answer("🔙 Повернулись в меню", reply_markup=main_kb)


if __name__ == "__main__":
    asyncio.run(main())


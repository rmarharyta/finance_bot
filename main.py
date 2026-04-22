import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext

from config import TOKEN
from db import init_db
from states import ExpenseState

from handlers.start import start
from handlers.expense import start_expense, get_amount, get_category, confirm
from handlers.income import income
from handlers.savings import show, edit
from handlers.stats import stats_menu, stats_handler

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

    # income /  income
    dp.message.register(income, F.text.startswith("/income"))
    dp.message.register(income, F.text == "💵 Дохід")

    # savings
    dp.message.register(show, F.text == "🏦 Заощадження")
    dp.message.register(edit, F.text.startswith("/savings"))

    # stats
    dp.message.register(stats_menu, F.text == "📊 Статистика")
    dp.callback_query.register(stats_handler)

    dp.message.register(back_to_menu, F.text == "⬅ В меню")
    

    await dp.start_polling(bot)

async def back_to_menu(message, state: FSMContext):
    await state.clear()
    await message.answer("🔙 Повернулись в меню", reply_markup=main_kb)


if __name__ == "__main__":
    asyncio.run(main())


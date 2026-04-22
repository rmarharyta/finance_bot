import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
from db import init_db

from handlers.start import start
from handlers.expense import start_expense, get_amount, get_category, confirm
from handlers.income import income
from handlers.savings import show, edit
from handlers.stats import stats_menu, stats_handler

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

    # income / savings
    dp.message.register(income, F.text.startswith("/income"))
    dp.message.register(show, F.text == "🏦 Заощадження")
    dp.message.register(edit, F.text.startswith("/savings"))

    # stats
    dp.message.register(stats_menu, F.text == "📊 Статистика")
    dp.callback_query.register(stats_handler)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
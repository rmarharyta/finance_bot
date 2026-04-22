from aiogram.types import CallbackQuery
from finance_logic import calculate
from db import get_by_category

def period_sql(period):
    if period=="day":
        return "AND date(date) = date('now')"
    elif period=="week":
        return "AND date(date) >= date('now', '-7 days')"
    elif period=="month":
        return "AND date(date) >= date('now', 'start of month')"
    elif period=="half_year":
        return "AND date(date) >= date('now', '-6 month')"
    elif period=="year":
        return "AND date(date) >= date('now', 'start of year')"
    return ""

async def stats_menu(message):
    from keyboards import stats_kb, back_kb
    await message.answer("📊 Обери період:", reply_markup=stats_kb, reply_markup=back_kb)
    
async def stats_handler(callback: CallbackQuery):
    
    sql=period_sql(callback.data)
    
    income, expenses, balance, savings = await calculate(
        callback.from_user.id, sql
    )
    
    cats = await get_by_category(callback.from_user.id, sql)
    
    text=f"""
    📊 Статистика

    💵 Дохід: {income}
    💸 Витрати: {expenses}
    💰 Баланс: {balance}
    🏦 Заощадження: {savings}

    📂 Категорії:"""
    for c, v in cats:
            text += f"{c}: {v}\n"

    await callback.message.answer(text)
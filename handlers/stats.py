from aiogram.types import CallbackQuery, Message
from finance_logic import calculate
from graph import generate_finance_chart
from db import get_by_category, get_income_by_days, get_expenses_by_days

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
    await message.answer("📊 Обери період:", reply_markup=stats_kb)
async def stats_handler(callback: CallbackQuery):
    
    sql=period_sql(callback.data)
    
    income, expenses, balance, savings = await calculate(
        callback.from_user.id, sql
    )
    
    cats = await get_by_category(callback.from_user.id, sql)
    income_data = await get_income_by_days(callback.from_user.id)
    expense_data = await get_expenses_by_days(callback.from_user.id)

    text=f"""
    📊 Статистика

    💵 Дохід: {income}
    💸 Витрати: {expenses}
    💰 Баланс: {balance}
    🏦 Заощадження: {savings}

    📂 Категорії:
    """
    for c, v in cats:
            text += f"{c}: {v}\n"

    chart_buffer = await generate_finance_chart(income_data, expense_data)
    await callback.message.answer_photo(photo=chart_buffer, caption=text)

async def finance_chart(message: Message):
    income = await get_income_by_days(message.from_user.id)
    expenses = await get_expenses_by_days(message.from_user.id)

    if not income and not expenses:
        await message.answer("❌ Немає даних для графіка")
        return

    img = await generate_finance_chart(income, expenses)

    await message.answer_photo(photo=img, caption="📊 Ваш фінансовий графік")
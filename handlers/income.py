from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states import IncomeState
from db import add_income, get_income
from keyboards import back_kb, main_kb, income_kb, confirm_kb


# 📌 Меню доходу
async def income_start(message: Message, state: FSMContext):
    await state.clear()

    income = await get_income(message.from_user.id)

    await message.answer(
        f"💵 Загальний дохід: {income}",
        reply_markup=income_kb
    )


# ➕ Додати дохід
async def income_add(message: Message, state: FSMContext):
    await state.update_data(mode="add")

    await message.answer(
        "Введіть суму для додавання:",
        reply_markup=back_kb
    )

    await state.set_state(IncomeState.amount)



# ✍️ Ввід суми
async def income_amount(message: Message, state: FSMContext):
    text = message.text.replace(",", ".").strip()

    if text == "⬅ В меню":
        await state.clear()
        await message.answer("🔙 Повернулись в меню", reply_markup=main_kb)
        return

    try:
        amount = float(text)
    except ValueError:
        await message.answer("❌ Введіть число")
        return

    await state.update_data(amount=amount)

    await message.answer(
        f"💵 Підтвердити додавання {amount}?",
        reply_markup=confirm_kb
    )

    await state.set_state(IncomeState.confirm)

# ✔️ підтвердження
async def income_confirm(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    amount = data.get("amount")

    if callback.data == "yes":
        await add_income(callback.from_user.id, amount)
        await callback.message.answer("💵 Дохід додано", reply_markup=main_kb)
    else:
        await callback.message.answer("❌ Скасовано", reply_markup=main_kb)

    await state.clear()
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from states import SavingsState
from db import get_savings, set_savings, add_savings
from keyboards import back_kb, main_kb, savings_kb, confirm_kb


# меню
async def show(message, state: FSMContext):
    await state.clear()
    savings = await get_savings(message.from_user.id)

    await message.answer(
        f"🏦 Ваші заощадження: {savings}",
        reply_markup=savings_kb
    )


# ➕ додати
async def savings_add(message, state: FSMContext):
    await state.set_data({"mode": "add"})
    await message.answer("Введіть суму:", reply_markup=back_kb)
    await state.set_state(SavingsState.amount)


# 💰 змінити
async def savings_set(message, state: FSMContext):
    await state.set_data({"mode": "set"})
    await message.answer("Введіть нову суму:", reply_markup=back_kb)
    await state.set_state(SavingsState.amount)


# введення суми
async def savings_amount(message, state: FSMContext):
    text = message.text.replace(",", ".").strip()

    if text == "⬅ В меню":
        await state.clear()
        await message.answer("🔙 Повернулись в меню", reply_markup=main_kb)
        return

    try:
        amount = float(text)
    except ValueError:
        await message.answer("❌ Введи число")
        return

    await state.update_data(amount=amount)

    data = await state.get_data()
    mode = data.get("mode")

    action = "додати" if mode == "add" else "змінити на"

    await message.answer(
        f"Підтвердити: {action} {amount}?",
        reply_markup=confirm_kb
    )

    await state.set_state(SavingsState.confirm)


# підтвердження
async def savings_confirm(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()

    if callback.data == "yes":
        amount = data.get("amount")
        mode = data.get("mode")

        if mode == "add":
            await add_savings(callback.from_user.id, amount)
            await callback.message.answer("🏦 Додано", reply_markup=main_kb)

        elif mode == "set":
            await set_savings(callback.from_user.id, amount)
            await callback.message.answer("🏦 Оновлено", reply_markup=main_kb)

    else:
        await callback.message.answer("❌ Скасовано", reply_markup=main_kb)

    await state.clear()
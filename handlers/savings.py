from aiogram.fsm.context import FSMContext
from states import SavingsState
from db import get_savings, set_savings
from keyboards import back_kb, main_kb

async def show(message, state: FSMContext):
    await state.clear()
    savings = await get_savings(message.from_user.id)

    await message.answer(
        f"💰 Ваші заощадження: {savings}\n\nВведіть нову суму:",
        reply_markup=back_kb
    )

    await state.set_state(SavingsState.amount)


async def edit(message, state: FSMContext):
    text = message.text.replace(",", ".").strip()

    if text == "⬅ В меню":
        return

    try:
        amount = float(text)
    except ValueError:
        await message.answer("❌ Введи число")
        return

    await set_savings(message.from_user.id, amount)
    await message.answer("✔ Оновлено", reply_markup=main_kb)

    await state.clear()
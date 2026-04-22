from aiogram.fsm.context import FSMContext
from states import IncomeState
from db import set_income
from keyboards import back_kb, main_kb

async def income_start(message, state: FSMContext):
    await state.clear()
    await message.answer("Введіть дохід:", reply_markup=back_kb)
    await state.set_state(IncomeState.amount)


async def income_amount(message, state: FSMContext):
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

    await set_income(message.from_user.id, amount)
    await message.answer("💵 Дохід збережено", reply_markup=main_kb)

    await state.clear()
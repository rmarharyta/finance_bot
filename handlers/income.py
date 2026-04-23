from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from states import IncomeState
from db import set_income, add_income, get_income
from keyboards import back_kb, main_kb, income_kb, confirm_kb

async def income_start(message: Message, state: FSMContext):
    await state.clear()
    income = await get_income(message.from_user.id)

    await message.answer(
        f"💵 Ваш дохід: {income}",
        reply_markup=income_kb
    )
async def income_add(message, state: FSMContext):
    await state.set_data({"mode": "add"})
    await message.answer("Введіть суму для додавання:", reply_markup=back_kb)
    await state.set_state(IncomeState.amount)

async def income_set(message, state: FSMContext):
    await state.set_data({"mode": "set"})
    await message.answer("Введіть нову суму доходу:", reply_markup=back_kb)
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

    # зберігаємо суму в FSM
    await state.update_data(amount=amount)

    data = await state.get_data()
    mode = data.get("mode")

    action = "додати до доходу" if mode == "add" else "змінити дохід на"

    await message.answer(
        f"Підтвердити: {action} {amount}?",
        reply_markup=confirm_kb
    )

    await state.set_state(IncomeState.confirm)


async def income_confirm(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()

    if callback.data == "yes":
        amount = data.get("amount")
        mode = data.get("mode")

        if mode == "add":
            await add_income(callback.from_user.id, amount)
            await callback.message.answer("💵 Дохід додано", reply_markup=main_kb)

        elif mode == "set":
            await set_income(callback.from_user.id, amount)
            await callback.message.answer("💵 Дохід змінено", reply_markup=main_kb)

    else:
        await callback.message.answer("❌ Скасовано", reply_markup=main_kb)

    await state.clear()
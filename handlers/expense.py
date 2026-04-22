from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from states import ExpenseState
from db import add_expense
from keyboards import categories, confirm_kb, back_kb

async def start_expense(message, state: FSMContext):
    await state.clear()
    await message.answer("Введіть суму витрати:",
        reply_markup=back_kb)
    await state.set_state(ExpenseState.amount)

async def get_amount(message, state: FSMContext):
    text = message.text.replace(",", ".").strip()

    if text == "⬅ В меню":
        await state.clear()
        from keyboards import main_kb
        await message.answer("🔙 В меню", reply_markup=main_kb)
        return
    
    try:
        amount = float(text)
    except ValueError:
        await message.answer("❌ Невірний формат. Введіть число (наприклад 100 або 99.5).")
        return
    
    await state.update_data(amount=amount)
    await message.answer("Оберіть категорію витрати:", reply_markup=categories)

    await state.set_state(ExpenseState.category)

async def get_category(callback, state: FSMContext):
    await callback.answer()
    await state.update_data(category=callback.data)
    
    data = await state.get_data()
    
    await callback.message.answer(
        f"Підтвердіть додавання витрати: {data['amount']} ?",
        reply_markup=confirm_kb 
        )
    
    await state.set_state(ExpenseState.confirm)
    
async def confirm(callback, state: FSMContext):
    await callback.answer()
    data = await state.get_data()

    if callback.data == "yes":
        await add_expense(
            callback.from_user.id,
            data['amount'],
            data['category']
        )
        await callback.message.answer("✔ Додано")

    else:
        await callback.message.answer("❌ Скасовано")

    await state.clear()
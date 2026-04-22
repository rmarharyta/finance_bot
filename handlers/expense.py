from aiogram.fsm.context import FSMContext
from states import ExpenseState
from db import add_expense
from keyboards import categories

async def start_expense(message, state: FSMContext):
    await message.answer("Введіть суму витрати:")
    await state.set_state(ExpenseState.amount)

async def get_amount(message, state: FSMContext):
    await state.update_data(amount=float(message.text))
    await message.answer("Оберіть категорію витрати:", reply_markup=categories)
    await state.set_state(ExpenseState.category)
    
async def get_category(callback, state: FSMContext):
    await state.update_data(category=callback.data)
    
    data = await state.get_data()
    
    await callback.message.answer(
        f"Підтвердіть додавання витрати: {data['amount']} ?", 
        )
    
    await state.set_state(ExpenseState.confirm)
    
async def confirm(callback, state: FSMContext):
    data = await state.get_data()
    
    if callback.data == "yes":
        await add_expense(
            callback.from_user.id,
            data['amount'],
            data['category']
        )
        await callback.message.answer("✔ Додано")
    
    await state.clear()
    
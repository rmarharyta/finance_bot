from aiogram import types
from keyboards import main_kb

async def start(message: types.Message):
    await message.answer("💰 Фінансовий бот готовий до роботи", reply_markup=main_kb)
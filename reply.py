from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Витрати"), KeyboardButton(text="💵 Дохід")],
        [KeyboardButton(text="🏦 Заощадження"), KeyboardButton(text="📊 Статистика")]
    ],
    resize_keyboard=True
)
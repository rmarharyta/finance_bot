from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

categories = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🍽 Їжа", callback_data="food")],
    [InlineKeyboardButton(text="🏠 Квартира", callback_data="home")],
    [InlineKeyboardButton(text="🚗 Машина", callback_data="car")],
    [InlineKeyboardButton(text="💳 Кредит", callback_data="credit")],
    [InlineKeyboardButton(text="🎮 Розваги", callback_data="fun")],
    [InlineKeyboardButton(text="✈️ Подорожі", callback_data="travel")],
    [InlineKeyboardButton(text="🐾 Тварини", callback_data="pets")]
])

stats_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📅 День", callback_data="day")],
    [InlineKeyboardButton(text="📆 Тиждень", callback_data="week")],
    [InlineKeyboardButton(text="🗓 Місяць", callback_data="month")],
    [InlineKeyboardButton(text="🗂 6 міс", callback_data="half_year")],
    [InlineKeyboardButton(text="📊 Рік", callback_data="year")]
])
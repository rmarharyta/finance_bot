from db import set_income

async def income(message):
    try:
        _, value = message.text.split()
        await set_income(message.from_user.id, float(value))
        await message.answer("💵 Дохід збережено")
    except Exception:
        await message.answer("❌ Невірний формат. Використання: /income 5000")
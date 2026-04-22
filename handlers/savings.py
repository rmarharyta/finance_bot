from db import get_savings, set_savings

async def show(message):
    savings = await get_savings(message.from_user.id)
    await message.answer(f"💰 Ваші заощадження: {savings}")
    
async def edit(message):
    try:
        _, value = message.text.split()
        await set_savings(message.from_user.id, float(value))
        await message.answer("✔ Заощадження оновлено")
    except Exception:
        await message.answer("❌ Невірний формат. Використання: /savings 2000")
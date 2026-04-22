import aiosqlite
from config import DB_NAME

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                category TEXT,
                date TEXT DEFAULT CURRENT_TIMESTAMP)
            """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS income (
                user_id INTEGER PRIMARY KEY,
                amount REAL)
            """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS savings(
                user_id INTEGER PRIMARY KEY,
                amount REAL)
            """)
        
        await db.commit()
        
        
async def get_income(user_id):
    
    async with aiosqlite.connect(DB_NAME) as db:
        cur = await db.execute(
            "SELECT amount FROM income WHERE user_id=?", (user_id,)
        )
        row = await cur.fetchone()
        return row[0] if row else 0
    
    
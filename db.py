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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                date TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS savings(
                user_id INTEGER PRIMARY KEY,
                amount REAL)
            """)
        
        await db.commit()
        
        

async def add_expense(user_id, amount, category):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO expenses (user_id, amount, category) VALUES (?, ?, ?)",
            (user_id, amount, category)
        )
        await db.commit()
        
async def get_sum(user_id, period_sql=""):
    async with aiosqlite.connect(DB_NAME) as db:
        cur = await db.execute(
            f"SELECT SUM(amount) FROM expenses WHERE user_id=? {period_sql}",
            (user_id,)
        )
        return (await cur.fetchone())[0] or 0
    
async def get_by_category(user_id, period_sql=""):
    async with aiosqlite.connect(DB_NAME) as db:
        cur = await db.execute(f"""
            SELECT category, SUM(amount) 
            FROM expenses
            WHERE user_id=? {period_sql}
            GROUP BY category""", (user_id,))
        return await cur.fetchall() 
        
async def get_expenses_by_days(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cur = await db.execute("""
            SELECT date(date), SUM(amount)
            FROM expenses
            WHERE user_id=?
            GROUP BY date(date)
            ORDER BY date(date)
        """, (user_id,))
        return await cur.fetchall()
        

async def get_income(user_id):
    
    async with aiosqlite.connect(DB_NAME) as db:
        cur = await db.execute(
            "SELECT amount FROM income WHERE user_id=?", (user_id,)
        )
        row = await cur.fetchone()
        return row[0] if row else 0
    
async def get_income_by_days(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cur = await db.execute("""
            SELECT date(date), SUM(amount)
            FROM income
            WHERE user_id=?
            GROUP BY date(date)
            ORDER BY date(date)
        """, (user_id,))
        return await cur.fetchall()
    
async def set_income(user_id, amount):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO income (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount=excluded.amount",
            (user_id, amount)
        )
        await db.commit()
        
async def add_income(user_id, amount):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO income (user_id, amount)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE
            SET amount = amount + excluded.amount
        """, (user_id, amount))
        await db.commit()

async def get_savings(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cur = await db.execute(
            "SELECT amount FROM savings WHERE user_id=?", (user_id,)
        )
        row = await cur.fetchone()
        return row[0] if row else 0

async def set_savings(user_id, amount):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR REPLACE INTO savings (user_id, amount) VALUES (?, ?)",
            (user_id, amount)
        )
        await db.commit()

async def add_savings(user_id, amount):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO savings (user_id, amount)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE
            SET amount = amount + excluded.amount
        """, (user_id, amount))
        await db.commit()
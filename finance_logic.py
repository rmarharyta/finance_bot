from db import get_income, get_sum, get_savings, set_savings

async def calculate(user_id, period_sql=""):
    income = await get_income(user_id)
    expenses = await get_sum(user_id, period_sql)
    savings = await get_savings(user_id),
    
    balance = income - expenses
    
    if balance < 0:
        savings += balance
        balance=0
        
        if savings < 0:
            savings = 0
        
        await set_savings(user_id, savings)
        
    return savings
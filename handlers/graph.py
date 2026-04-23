import matplotlib.pyplot as plt
from io import BytesIO

async def generate_finance_chart(income_data, expense_data):
    income_dates = [x[0] for x in income_data]
    income_vals = [x[1] for x in income_data]

    expense_dates = [x[0] for x in expense_data]
    expense_vals = [x[1] for x in expense_data]

    plt.figure(figsize=(8, 4))

    plt.plot(income_dates, income_vals, label="Дохід", marker="o")
    plt.plot(expense_dates, expense_vals, label="Витрати", marker="o")

    plt.title("Фінансовий баланс")
    plt.xlabel("Дата")
    plt.ylabel("Сума")
    plt.legend()
    plt.grid(True)

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    return buffer
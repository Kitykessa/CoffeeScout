import pandas as pd
import json

# Відкриваємо Excel
xls = pd.ExcelFile("coffee.xlsx")

# Завантажуємо всі аркуші
coffee_df = pd.read_excel(xls, "coffee")
store_df = pd.read_excel(xls, "store")
coffee_store_df = pd.read_excel(xls, "coffee_store")

# Конвертуємо у список словників
coffee = coffee_df.to_dict(orient="records")
store = store_df.to_dict(orient="records")
coffee_store = coffee_store_df.to_dict(orient="records")

# Записуємо в один JSON
with open("coffee.json", "w", encoding="utf-8") as f:
    json.dump(
        {"coffee": coffee, "store": store, "coffee_store": coffee_store},
        f,
        ensure_ascii=False,
        indent=2
    )

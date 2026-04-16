import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

categories = ["Food", "Transport", "Rent", "Entertainment", "Health", "Shopping"]

descriptions = {
    "Food": ["Grocery store", "Restaurant", "Coffee shop", "Takeaway", "Bakery"],
    "Transport": ["Uber", "Gas station", "Bus pass", "Parking", "Train ticket"],
    "Rent": ["Monthly rent", "Utilities", "Internet bill", "Water bill", "Electricity"],
    "Entertainment": ["Netflix", "Cinema", "Concert ticket", "Spotify", "Video game"],
    "Health": ["Pharmacy", "Gym membership", "Doctor visit", "Vitamins", "Dentist"],
    "Shopping": ["Amazon", "Clothing store", "Electronics", "Home decor", "Bookstore"]
}

amount_ranges = {
    "Food": (5, 120),
    "Transport": (3, 80),
    "Rent": (400, 1500),
    "Entertainment": (5, 100),
    "Health": (10, 200),
    "Shopping": (10, 300)
}

start_date = datetime(2024, 1, 1)
rows = []

for _ in range(200):
    category = random.choice(categories)
    description = random.choice(descriptions[category])
    amount = round(random.uniform(*amount_ranges[category]), 2)
    date = start_date + timedelta(days=random.randint(0, 365))
    rows.append({"Date": date.strftime("%Y-%m-%d"), "Category": category,
                 "Description": description, "Amount": amount})

df = pd.DataFrame(rows)
df = df.sort_values("Date").reset_index(drop=True)
df.to_csv("transactions.csv", index=False)
print("transactions.csv created with 200 rows!")
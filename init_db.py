import sqlite3
import json
from werkzeug.security import generate_password_hash

# ---------------- Load JSON ----------------
with open("coffee.json", encoding="utf-8") as f:
    data = json.load(f)

coffee_data = data["coffee"]
store_data = data["store"]
coffee_store_data = data["coffee_store"]

# ---------------- Connect DB ----------------
conn = sqlite3.connect("coffee.db")
c = conn.cursor()

# ---------------- USERS ----------------
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

# ---------------- COFFEE ----------------
c.execute("""
CREATE TABLE IF NOT EXISTS coffee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    origin TEXT,
    roast TEXT,
    beans TEXT,
    description TEXT,
    image TEXT
)
""")

# ---------------- STORES ----------------
c.execute("""
CREATE TABLE IF NOT EXISTS store (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store TEXT
)
""")

# ---------------- COFFEE ↔ STORES ----------------
c.execute("""
CREATE TABLE IF NOT EXISTS coffee_store (
    coffee_id INTEGER,
    store_id INTEGER,
    FOREIGN KEY (coffee_id) REFERENCES coffee(id),
    FOREIGN KEY (store_id) REFERENCES store(id)
)
""")

# ---------------- REVIEWS ----------------

c.execute("""
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coffee_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    rating INTEGER,
    aroma INTEGER,
    acidity INTEGER,
    bitterness INTEGER,
    body INTEGER,
    finish INTEGER,
    roast INTEGER,
    notes TEXT,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (coffee_id) REFERENCES coffee(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

# ---------------- USERS SEED ----------------
users = [
    {"username": "admin", "password": "adminpass"},
    {"username": "user1", "password": "coffee123"}
]

for user in users:
    hashed = generate_password_hash(user["password"])
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user["username"], hashed))
    except sqlite3.IntegrityError:
        print(f"User {user['username']} already exists")

# ---------------- COFFEE SEED ----------------
for row in coffee_data:
    c.execute("""
    INSERT OR IGNORE INTO coffee (id, name, origin, roast, beans, description, image)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        row["id"],
        row["name"],
        row["origin"],
        row["roast"],
        row["beans"],
        row["description"],
        row["image"]
    ))

# ---------------- STORE SEED ----------------
for row in store_data:
    c.execute("INSERT OR IGNORE INTO store (id, store) VALUES (?, ?)", (row["id"], row["store"]))

# ---------------- COFFEE_STORE SEED ----------------
for row in coffee_store_data:
    c.execute("INSERT OR IGNORE INTO coffee_store (coffee_id, store_id) VALUES (?, ?)", (row["coffee_id"], row["store_id"]))

conn.commit()
conn.close()

print("Database initialized successfully 🚀")

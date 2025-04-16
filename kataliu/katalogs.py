import pandas as pd
import sqlite3

# Load Excel
df = pd.read_excel("C:/Users/op2604/Desktop/KvitsSIA/kataliu/s.xls")
print(df.columns)  # 👈 check actual column names
# exit()  # uncomment this if just testing columns

# Connect to SQLite
conn = sqlite3.connect("katalogs.db")
cursor = conn.cursor()

# Fix the CREATE TABLE syntax
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ean TEXT,
    kods TEXT,
    bilde TEXT,
    apraksts TEXT,
    cena REAL
)
""")

# Now use the correct column names
for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO products (ean, kods, bilde, apraksts, cena) VALUES (?, ?, ?, ?, ?)",
        (
            row['EAN13'],               # ✅ Replace with actual column name
            row['Pasūtījuma_kods'],     # ✅ Replace with actual column name
            row['Bilde'],
            row['Apraksts'],
            row['Cena']
        )
    )

conn.commit()
conn.close()

print("✅ Data imported successfully!")

import pandas as pd
import sqlite3
import os

# Make sure to use raw string or forward slashes for file paths to avoid unicode escape errors
excel_path = r"C:/Users/Oskar/Desktop/kvits.lv/kataliu/katalogs_2024.xls"
image_base_url = "C:/Users/Oskar/Desktop/kvits.lv/static/images"  # Or use full domain like 'https://kvits.lv/images/'

# Read Excel file
df = pd.read_excel(excel_path)

# Fix column names (strip whitespace, just in case)
df.columns = df.columns.str.strip()

# Connect to SQLite
conn = sqlite3.connect("katalogs.db")
cursor = conn.cursor()

# Create table
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

# Insert data
for _, row in df.iterrows():
    # Handle missing or NaN values
    ean = row.get('EAN13', '')
    kods = row.get('Pasūtījuma_kods', '')
    apraksts = row.get('Apraksts', '')
    cena = row.get('Cena', 0)

    # Handle image
    bilde_raw = row.get('Bilde')
    if pd.isna(bilde_raw) or not str(bilde_raw).strip():
        bilde = image_base_url + "no-image.png"  # fallback image
    else:
        bilde = image_base_url + str(bilde_raw).strip()

    cursor.execute("""
        INSERT INTO products (ean, kods, bilde, apraksts, cena)
        VALUES (?, ?, ?, ?, ?)
    """, (ean, kods, bilde, apraksts, cena))

# Save and close
conn.commit()
conn.close()

print("✅ Data imported successfully!")

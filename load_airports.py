"""
load_airports.py

This script reads airport information from an Excel file (e.g., country, city, and IATA code)
and loads it into a SQLite database. It normalizes column names, ensures the destination
table ('airports_lookup') exists, and inserts the data for use in lookups or joins with
flight data.

Usage:
    python load_airports.py  # Make sure 'Final Airports List.xlsx' is in the same directory
"""

import sqlite3
import pandas as pd
import os

# Path to your Excel file
excel_path = "Final Airports List.xlsx"  # Update if the filename is different

# Load Excel data
df = pd.read_excel(excel_path)

# Normalize column names just in case
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Connect to your existing SQLite database
db_path = os.path.join(os.path.dirname(__file__), "flights.db")
with sqlite3.connect(db_path) as conn:
    # Create the airports_lookup table if not exists
    conn.execute("""
        CREATE TABLE IF NOT EXISTS airports_lookup (
            country TEXT,
            city TEXT,
            iata_code TEXT PRIMARY KEY
        )
    """)
    # Insert data
    df.rename(columns={"location": "city"}, inplace=True)
    df.to_sql("airports", conn, if_exists="replace", index=False)

print("Airports table loaded into flights.db as 'airports_lookup'")


import pandas as pd
from db import get_connection
import numpy as np

# Load CSV
df = pd.read_csv("synthetic_client_queries.csv")

# Rename columns to match MySQL schema
df = df.rename(columns={
    "client_email": "mail_id",
    "client_mobile": "mobile_number",
    "date_raised": "query_created_time",
    "date_closed": "query_closed_time"
})

# Convert NaN to None (VERY IMPORTANT)
df = df.where(pd.notnull(df), None)

# Connect to MySQL
conn = get_connection()
cursor = conn.cursor()

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO queries
        (mail_id, mobile_number, query_heading, query_description,
        status, query_created_time, query_closed_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        row["mail_id"],
        row["mobile_number"],
        row["query_heading"],
        row["query_description"],
        row["status"],
        row["query_created_time"],
        row["query_closed_time"]   # None → NULL
    ))

conn.commit()
conn.close()

print("CSV data successfully inserted into MySQL")

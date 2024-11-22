import csv
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mytable (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Category TEXT,
        Question TEXT,
        Answer TEXT
    )
''')

# Read CSV file and insert data into table
with open('data.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    # Insert data
    for row in reader:
        cursor.execute('''
            INSERT INTO mytable (Category, Question, Answer)
            VALUES (?, ?, ?)
        ''', (row['Category'], row['Question'], row['Answer']))

# Commit changes and close connection
conn.commit()
conn.close()

print("CSV data imported successfully.")

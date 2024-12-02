import csv
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('../app/testing_trivia_qa.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS jeopardy (
        ShowNumber int,
        AirDate TEXT,
        Round TEXT,
        Category TEXT,
        Value int,
        Question TEXT,
        Answer TEXT,
        MockHumanAnswer TEXT
    )
''')

# Read CSV file and insert data into table
with open('../data/test/mock_data.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    # Insert data
    for row in reader:
        cursor.execute('''
            INSERT INTO jeopardy (ShowNumber, AirDate, Round, Category, Value, Question, Answer, MockHumanAnswer)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (row['ShowNumber'], row['AirDate'], row['Round'], row['Category'], row['Value'], row['Question'], row['Answer'], row['MockHumanAnswer']))

# Commit changes and close connection
conn.commit()
conn.close()

print("CSV data imported successfully.")

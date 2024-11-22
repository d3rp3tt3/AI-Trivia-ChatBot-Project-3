import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# Run a SELECT query
cursor.execute('''
    SELECT Category, Question, Answer 
    FROM mytable 
    LIMIT 5
''')

# Fetch and display the results
results = cursor.fetchall()
for row in results:
    print(f"Category: {row[0]}")
    print(f"Question: {row[1]}")
    print(f"Answer: {row[2]}")
    print("---")

# Close the connection
conn.close()

print("Query executed successfully.")

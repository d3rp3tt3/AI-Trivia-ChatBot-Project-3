import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('../app/testing_trivia_qa.db')
cursor = conn.cursor()

# Run a SELECT query
cursor.execute('''
    SELECT ShowNumber, AirDate, Round, Category, Value, Question, Answer 
    FROM jeopardy 
    LIMIT 7
''')

# Fetch and display the results
results = cursor.fetchall()
for row in results:
    print(f"ShowNumber: {row[0]}")
    print(f"AirDate: {row[1]}")
    print(f"Round: {row[2]}")
    print(f"Category: {row[3]}")
    print(f"Value: {row[4]}")
    print(f"Question: {row[5]}")
    print(f"Answer: {row[6]}")
    print("---")

# Close the connection
conn.close()

print("Query executed successfully.")

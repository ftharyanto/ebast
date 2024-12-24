import sqlite3
import csv

def import_csv_to_db(csv_file, db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            column1 TEXT,
            column2 TEXT,
            column3 TEXT
        )
    ''')

    # Open the CSV file and read its contents
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Skip the header row

        # Insert CSV data into the database
        for row in reader:
            cursor.execute('''
                INSERT INTO data (column1, column2, column3)
                VALUES (?, ?, ?)
            ''', (row[0], row[1], row[2]))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

csv_file = 'data.csv'  # Path to your CSV file
db_file = 'db.sqlite3'  # Path to your SQLite database file
import_csv_to_db(csv_file, db_file)
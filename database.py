import sqlite3

# Connect to SQLite database (or create if it doesn't exist)
conn = sqlite3.connect('my_database.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create table for battery information
cursor.execute('''CREATE TABLE IF NOT EXISTS batteries (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    capacity REAL,
                    voltage REAL
                )''')

# Create table for location information
cursor.execute('''CREATE TABLE IF NOT EXISTS locations (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    latitude REAL,
                    longitude REAL
                )''')

# Create table for time information
cursor.execute('''CREATE TABLE IF NOT EXISTS times (
                    id INTEGER PRIMARY KEY,
                    time_stamp TEXT
                )''')

# Example of inserting data into the tables
cursor.execute("INSERT INTO batteries (name, capacity, voltage) VALUES (?, ?, ?)", ('Battery A', 1000, 3.7))
cursor.execute("INSERT INTO batteries (name, capacity, voltage) VALUES (?, ?, ?)", ('Battery B', 1500, 3.7))

cursor.execute("INSERT INTO locations (name, latitude, longitude) VALUES (?, ?, ?)", ('Location X', 40.7128, -74.0060))
cursor.execute("INSERT INTO locations (name, latitude, longitude) VALUES (?, ?, ?)", ('Location Y', 34.0522, -118.2437))

cursor.execute("INSERT INTO times (time_stamp) VALUES (?)", ('2024-04-05 08:00:00',))
cursor.execute("INSERT INTO times (time_stamp) VALUES (?)", ('2024-04-05 09:00:00',))

# Commit changes and close connection
conn.commit()
conn.close()

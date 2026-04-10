import sqlite3
import os

# Find all database files
db_files = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.db'):
            db_files.append(os.path.join(root, file))

print('Database files found:', db_files)

for db_file in db_files:
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Check if table exists and count records
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='air_quality'")
        table_exists = cursor.fetchone()

        if table_exists:
            cursor.execute('SELECT COUNT(*) FROM air_quality')
            count = cursor.fetchone()[0]
            print(f'Database {db_file}: {count} records')

            # Get sample data
            cursor.execute('SELECT DISTINCT state FROM air_quality LIMIT 5')
            states = cursor.fetchall()
            print(f'Sample states: {[state[0] for state in states]}')

            # Get pollutant types
            cursor.execute('SELECT DISTINCT pollutant_id FROM air_quality LIMIT 5')
            pollutants = cursor.fetchall()
            print(f'Sample pollutants: {[pollutant[0] for pollutant in pollutants]}')

        conn.close()

    except Exception as e:
        print(f'Error with {db_file}: {e}')

if not db_files:
    print('No database files found. Make sure to run load_data.py first.')

import sqlite3

conn = sqlite3.connect("DB/mydatabase.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE vacancy
                  (title text, link text, salary_min integer, salary_max integer,
                   employer text, sfere text, city text, description text)
               """)
print("Data Base create successfully!")
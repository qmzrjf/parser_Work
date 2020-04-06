import sqlite3

conn = sqlite3.connect("DB/mydatabase.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE vacancy
                  (id integer, 
                  title text, 
                  link text, 
                  salary_min integer, 
                  salary_max integer, 
                  employer text, 
                  sfere text, 
                  city text, 
                  education text, 
                  experience text, 
                  description text)
               """)
conn.close()

print("Data Base create successfully!")

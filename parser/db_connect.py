import sqlite3

from config import config


def create_db():
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE vacancy
                      (id integer, 
                      title text, 
                      link text, 
                      salary_min integer, 
                      salary_max integer, 
                      employer text, 
                      employer_href text, 
                      sfere text, 
                      city text, 
                      education text, 
                      experience text, 
                      description text)
                   """)
    conn.close()

    print("Data Base create successfully!")

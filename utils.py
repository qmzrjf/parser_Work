import random
from time import sleep
import json
import sqlite3

conn = sqlite3.connect("DB/mydatabase.db")
cursor = conn.cursor()


def save_info_txt(array: list) -> None:
    with open('TEXT/workua.txt', 'a') as file:
        for line in array:
            file.write(' | '.join(str(line)) + '\n')


def save_info_json(dict: dict, page) -> None:
    with open(f'JSON_DATA/json_file_for_page_{page}.json', 'w') as f:
        json.dump(dict, f, ensure_ascii=False, indent=2)


def seve_info_to_db (array:list) -> None:
    cursor.execute(f"""INSERT INTO vacancy
                      VALUES ('{array[0]}', '{array[1]}','{array[2]}',
                        '{array[3]}','{array[4]}', '{array[5]}', '{array[6]}', '{array[7]}')"""
                   )
    conn.commit()


def random_sleep():
    sleep(random.randint(1, 4))
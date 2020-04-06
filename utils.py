import random
from time import sleep
import json
import sqlite3




def save_info_txt(array: list) -> None:
    with open('TEXT/workua.txt', 'a') as file:
        for line in array:
            file.write(' | '.join(line) + '\n')


def save_info_json(dict_json:dict, page) -> None:
    with open(f'JSON_DATA/json_file_for_page_{page}.json', 'w') as f:
        json.dump(dict_json, f, ensure_ascii=False, indent=2)


def save_info_to_db(array: list) -> None:
    conn = sqlite3.connect("DB/mydatabase.db")
    cursor = conn.cursor()

    cursor.executemany('INSERT INTO vacancy VALUES (?,?,?,?,?,?,?,?,?,?,?)', array)

    conn.commit()
    conn.close()

def random_sleep():
    sleep(random.randint(1, 4))

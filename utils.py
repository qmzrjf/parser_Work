import random
from time import sleep
import json
import sqlite3


def write_json(dict_js):
    try:
        data = json.load(open('JSON_DATA/json_file.json'))
    except:
        data = []

    data.append(dict_js)

    with open('JSON_DATA/json_file.json', 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_info_txt(array: list) -> None:
    with open('TEXT/workua.txt', 'a') as file:
        for line in array:
            file.write(' | '.join(line) + '\n')


def save_info_to_db(array: list) -> None:
    conn = sqlite3.connect("DB/mydatabase.db")
    cursor = conn.cursor()

    cursor.executemany('INSERT INTO vacancy VALUES (?,?,?,?,?,?,?,?,?,?,?)', array)

    conn.commit()
    conn.close()


def random_sleep():
    sleep(random.randint(1, 4))

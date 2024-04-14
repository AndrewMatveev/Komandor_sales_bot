import sqlite3
from random import randint, uniform
from datetime import datetime, timedelta

import values as v



def create_table(): # создать таблицу в базе данных (локальная функция)
    connect = sqlite3.connect(v.db_name)
    cursor = connect.cursor()
    cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS {v.table_name}(
                        sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR(100),
                        count FLOAT,
                        price FLOAT,
                        date DATETIME)
    """)
    connect.commit()
    connect.close()

create_table()



def db_row_coutn(): # извлечь количество строк из таблицы
    connect = sqlite3.connect(v.db_name)
    cursor = connect.cursor()
    cursor.execute(f"SELECT COUNT('sale_id') FROM {v.table_name}")
    ctn_rows = cursor.fetchall()[0][0]
    connect.commit()
    connect.close()
    return ctn_rows



def generate_data(count, ctn_rows=db_row_coutn()): # генерация и вставка случайных данных (локальная функция)
    connect = sqlite3.connect(v.db_name)
    cursor = connect.cursor()
    if ctn_rows < count:
        for _ in range(count):
            sale_data = {
                'name': 'prod_' + str(randint(1, 500)),
                'count': round(uniform(1, 100), 0),
                'price': round(uniform(10, 1000), 2),
                'date': (datetime.now() - timedelta(days=randint(1, 365*5),
                                                    hours=randint(0, 23),
                                                    minutes=randint(0, 59))
                        ).strftime('%Y-%m-%d %H:%M')
            }
            cursor.execute(f"""INSERT INTO {v.table_name} (name, count, price, date)
                            VALUES (:name, :count, :price, :date)""", sale_data)
        connect.commit()
    connect.close()

generate_data(v.count_row_to_generate)



def add_to_db(input_data): # добавить внесённые данные о продаже в базу 
    connect = sqlite3.connect(v.db_name)
    cursor = connect.cursor()
    cursor.execute(f'''INSERT INTO {v.table_name} (name, count, price, date)
                  VALUES (:name, :count, :price, :date)''', input_data['values'])
    connect.commit()
    connect.close()



def select_between_date(start_d, final_d): # выбрать данные из таблицы, с начальной по конечную дату, для отчёта
    connect = sqlite3.connect(v.db_name)
    cursor = connect.cursor()
    cursor.execute(f"""
                SELECT * FROM {v.table_name}
                WHERE date BETWEEN '{start_d}' AND '{final_d}'
    """)
    selected_data = cursor.fetchall()
    connect.commit()
    connect.close()
    return selected_data



def get_column_names(): # получить список с названиями столбцов таблицы из базы
    connect = sqlite3.connect(v.db_name)
    cursor = connect.cursor()
    cursor.execute(f"PRAGMA table_info({v.table_name})")
    columns = cursor.fetchall()
    connect.close()
    return [column[1] for column in columns]
import requests # библиотека для запросов к серверу телеграм
import values as v
import dbconnector as db

from prettytable import PrettyTable

def send_message(chat_id, text, parse_mode=None, reply_markup=None): # выводит сообщения в мессенджер
    method = "sendMessage"
    url = f"https://api.telegram.org/bot{v.token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    if parse_mode:
        data["parse_mode"] = parse_mode
    if reply_markup:
        data["reply_markup"] = reply_markup.to_json()
    requests.post(url, json=data)


def format_to_table(col_names, data): # форматировать данные в формате списка строк в табличный формат ASCII
    table = PrettyTable(col_names)
    for row in data:
        table.add_row(row)
    return table.get_string()



def get_input_table(input_data): # получить введенные данные табличном формате ASCII для наглядности
    data_row = [{**{db.get_column_names()[0]: int(db.db_row_coutn() + 1)},
                 **input_data['values']}.values()]
    data_table = format_to_table(col_names=db.get_column_names(), data=data_row)
    return data_table



def chunk_lst(lst, chunk_size=v.limit_rows_for_tg_message): # разделить большой список для вывода по разным сообщениям
    result = []
    for i in range(0, len(lst), chunk_size):
        result.append(lst[i:i + chunk_size])
    return result
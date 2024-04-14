import copy
import os


from dotenv import dotenv_values

token = dotenv_values().get('TELEGRAM_BOT_TOKEN') # счтывание токена из скрытого файла

table_name = 'sales' # название таблице в базе данных

db_name = f'{os.path.dirname(__file__)}\db.db' # путь к базе данных

count_row_to_generate = 5000 # количество генерируемых данных

limit_rows_for_tg_message = 55 # 4096 символов за 1 сообщение в боте - максимум, это примерно 64 строки, 55 взято с запасом





sale_data = {'values': copy.deepcopy(default_sd_val := {'name': None, # Словарь для хранения вводимых данных о продаже
                                                        'count': None,
                                                        'price': None,
                                                        'date': None}),
            'filling': 0} # два положения: 0 - пусто или заполнено, 1 - в процессе заполнения



report_period = {'values': copy.deepcopy(default_rp_val := {'start': None, # Словарь для хранения данных о периоде отчёта
                                                            'final': None}),
                'filling': 0} # два положения: 0 - пусто или заполнено, 1 - в процессе заполнения
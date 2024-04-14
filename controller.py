import dbconnector as db
import values as v
import outputter as o
import menu as m


from flask import Flask, request
from telegram import ReplyKeyboardRemove
from datetime import datetime
import copy





app = Flask(__name__)

@app.route('/', methods=["POST"])

def process():

    update = request.json
    if 'message' in update and 'text' in update['message']: # часть "and 'text' in update['message']" -  проверка наличия ключа 'text' в вашем запросе перед его использованием:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]
        



        # ________________________________________________________Отработка меню____________________________________________________________________
        if text == "/start":
            o.send_message(chat_id=chat_id,
                           text="*Привет! Я бот для учета продаж.*\n\nНадеюсь я достаточно функциональный, чтобы вам понравиться! 😉",
                           parse_mode="Markdown")
            
            o.send_message(chat_id=chat_id,
                           text="Приступим! Что выхотите сделать?", reply_markup=m.menu_keyboard)
            

        elif text == m.insrt_btn_txt:
            o.send_message(chat_id=chat_id,
                           text="Напишите название товара 👇",
                           reply_markup=ReplyKeyboardRemove())
            
            v.sale_data['filling'] = 1 # отрытие режима заполнения массива с информацией для внесения в базу данных


        elif text == m.reprt_btn_txt:
            o.send_message(chat_id=chat_id, text="Введите начальную дату для отчёта ➡️📃\n\n_Подсказка: формат ДД.ММ.ГГГГ, ЧЧ:MM_",
                           parse_mode="Markdown",
                           reply_markup=ReplyKeyboardRemove())

            v.report_period['filling'] = 1 # отрытие режима заполнения массива датами для запроса отчета о продажах за период из базы


        elif text == m.tomenu_btn_txt:
            o.send_message(chat_id=chat_id, text="Вы в главном меню! Выберите действие.", reply_markup=m.menu_keyboard)
        # _____________________________________________________________________________________________________________________________________________




        # ________________________________________Обработка сообщений для ввода данных о продаже_______________________________________________________
        elif v.sale_data['filling'] == 1:
            

            # Ввод названия товара
            if v.sale_data['values']['name'] == None: 
                try:
                    v.sale_data['values']["name"] = str(text)  # преобразование в нужный формат

                    o.send_message(chat_id=chat_id,
                                   text="Введите количество проданных единиц 👇",
                                   reply_markup=ReplyKeyboardRemove())
                
                except ValueError: # отработка неправильного внесения данных
                    v.sale_data['values']["name"] = None
                    o.send_message(chat_id=chat_id,
                                   text=f"Хмм... что введено что-то не так 🤔\n")
                    print(f'Ошибка, тип переменной "name" {type(text)}')


            # Ввод количества товара
            elif v.sale_data['values']['count'] == None:
                try:
                    v.sale_data['values']['count'] = float(text.replace(",", ".")) # преобразование в нужный формат

                    o.send_message(chat_id=chat_id,
                                   text="Теперь введите цену единицы товара 👇",
                                   reply_markup=ReplyKeyboardRemove())
                    
                except ValueError:
                    v.sale_data['values']['count'] = None
                    o.send_message(chat_id=chat_id,
                                   text=f"Хмм... что введено что-то не так 🤔\n_Подсказка: тут должно быть целое или десятичное число_",
                                   parse_mode="Markdown")
                    print(f'Ошибка, тип переменной "count" {type(text)}')


            # Ввод цены единицы товара
            elif v.sale_data['values']['price'] == None:
                try:
                    v.sale_data['values']["price"] = float(text.replace(",", ".")) # преобразование в нужный формат

                    o.send_message(chat_id=chat_id,
                                   text="Почти всё! Осталоль написать дату и время продажи 👇\n\n_Подсказка: формат ДД.ММ.ГГГГ, ЧЧ:MM_",
                                   reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")
                    
                except ValueError: # отработка неправильного внесения данных
                    v.sale_data['values']['price'] = None
                    
                    o.send_message(chat_id=chat_id,
                                   text=f"Хмм... что введено что-то не так 🤔\n_Подсказка: тут должно быть целое или десятичное число_",
                                   parse_mode="Markdown")
                    print(f'Ошибка, тип переменной "price" {type(text)}')


            # Ввод даты продажи товара + логика завершения ввода + логика внесения в базу
            elif v.sale_data['values']['date'] == None:
                try:
                    v.sale_data['values']['date'] = datetime.strptime(text, "%d.%m.%Y, %H:%M").strftime('%Y-%m-%d %H:%M') # преобразование в нужный формат

                    v.sale_data['filling'] = 0 # выход из режима ввода

                    o.send_message(chat_id=chat_id,
                                 text=f"Круто, теперь в базу добавлена запись 👍\n\n<pre>{o.get_input_table(v.sale_data)}</pre>",
                                 parse_mode='HTML',
                                 reply_markup=m.go_to_menu_keyboard)
                    
                    db.add_to_db(v.sale_data) # внесение в базу данных

                    v.sale_data['values'] = copy.deepcopy(v.default_sd_val) # сброс на дефолтные значения

                except ValueError: # отработка неправильного внесения данных
                    v.sale_data['values']["date"] = None
                    o.send_message(chat_id=chat_id,
                                   text=f"Хмм... что введено что-то не так 🤔\n_Может вы упустили какой-то символ? Например, точку, запятую или пробел._",
                                   parse_mode="Markdown")
                    print(f'Ошибка, тип переменной "date" {type(text)}')
        # ________________________________________________________________________________________________________________________________________________
  


        

        # ____________________________________________Обработка сообщений для вывода отчёта_______________________________________________________________
        elif v.report_period['filling'] == 1:


            # Ввод начальной даты для отчёта
            if v.report_period['values']['start'] == None:
                try:
                    v.report_period['values']["start"] = datetime.strptime(text, "%d.%m.%Y, %H:%M").strftime('%Y-%m-%d %H:%M') # преобразование в нужный формат

                    o.send_message(chat_id=chat_id,
                                   text="Введите конечную дату для отчёта 📃⬅️\n\n_Подсказка: формат ДД.ММ.ГГГГ, ЧЧ:MM_",
                                   reply_markup=ReplyKeyboardRemove(),
                                   parse_mode="Markdown")
                    
                except ValueError: # отработка неправильного внесения данных
                    v.report_period['values']["start"] = None
                    o.send_message(chat_id=chat_id, text=f"Хмм... что введено что-то не так 🤔\n_Может вы упустили какой-то символ? Например, точку, запятую или пробел._", parse_mode="Markdown")
                    print(f'Ошибка, тип переменной "start" {type(text)}')
            

            # Ввод конечной даты для отчёта + логика завершения ввода + логика вывода отчета
            elif v.report_period['values']['final'] == None:
                try:
                    v.report_period['values']["final"] = datetime.strptime(text, "%d.%m.%Y, %H:%M").strftime('%Y-%m-%d %H:%M') # преобразование в нужный формат

                    v.report_period['filling'] = 0 # выход из режима ввода

                    o.send_message(chat_id=chat_id,
                                   text=f"Отчет о продажах за период c {v.report_period['values']['start']} по {v.report_period['values']['final']} сформирован 🫡")

                    column_names = db.get_column_names()
                    united_select_data = db.select_between_date(v.report_period['values']["start"],
                                                                v.report_period['values']['final'])

                    for chunk in o.chunk_lst(united_select_data): # цикл для отправки отчета c обходом ограничения символов в одном сообщении
                        o.send_message(chat_id=chat_id,
                                    text=f"<pre>{o.format_to_table(column_names, chunk)}</pre>",
                                    parse_mode="HTML",
                                    reply_markup=m.go_to_menu_keyboard)

                    v.report_period['values'] = copy.deepcopy(v.default_rp_val) # сброс на дефолтные значения

                except ValueError: # отработка неправильного внесения данных
                    v.report_period['values']["final"] = None
                    o.send_message(chat_id=chat_id,
                                   text=f"Хмм... что введено что-то не так 🤔\n_Может вы упустили какой-то символ? Например, точку, запятую или пробел._",
                                   parse_mode="Markdown")
                    print(f'Ошибка, тип переменной "start" {type(text)}')

                
        else: # отработка несогласованной команды
            o.send_message(chat_id=chat_id,
                           text="Ничего не понятно, но очень интересно! 🤨\n_Попробуйте воспользоваться меню ❤️_",
                           parse_mode="Markdown",
                           reply_markup=m.go_to_menu_keyboard)


    return {"ok": True}





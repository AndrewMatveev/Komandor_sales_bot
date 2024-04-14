from telegram import ReplyKeyboardMarkup, KeyboardButton

# Кнопки меню
menu_keyboard = ReplyKeyboardMarkup([[KeyboardButton(insrt_btn_txt:="⌨️ Внести данные о продаже")],
                                     [KeyboardButton(reprt_btn_txt:="📃 Получить отчет о продажах за период")]],
                                     resize_keyboard=True)

go_to_menu_keyboard = ReplyKeyboardMarkup([[KeyboardButton(tomenu_btn_txt:="🔙 Отлично, пошли в меню")]],
                                            resize_keyboard=True)
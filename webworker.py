import subprocess
import os
import time
import requests

from values import token


# запуск ngrok
def run_ngrok():
    current_path = os.path.dirname(__file__) # Получаем текущий путь файла

    command = [ # В этой строке формируется команда для запуска ngrok.exe
                'start', # указывает командной оболочке (cmd) на запуск нового процесса в новом окне терминала.
                'cmd', # указывает на использование командной оболочки (cmd)
                '/c', # сообщает командной оболочке, что после выполнения команды нужно закрыть окно терминала
                f'{current_path}\\ngrok.exe http 5000'] # команда, в которой указывается путь к ngrok.exe и его аргументы

    subprocess.Popen( # вызывает Popen для выполнения команды в новом процессе
                    command, # команда, которую нужно выполнить
                    shell=True, # указывает, что команда будет выполняться через оболочку (shell)
                    text=True # указывает, что вывод будет в текстовом формате (используется для обработки вывода)
                    ).stdout # атрибут возвращает стандартный вывод (stdout) процесса
    time.sleep(15) # таймер задержки чтобы ngrok успел прогрузиться



 

# запрос публичного URL у ngrok
def get_ngrok_public_url():
    run_ngrok()

    response = requests.get("http://localhost:4040/api/tunnels") # Запрос к API ngrok для получения информации о туннеле

    if response.status_code == 200: # Проверка успешности запроса
        data = response.json() # Получение JSON данных из ответа
        public_url = data['tunnels'][0]['public_url'] # Извлечение public URL из данных
        print("Public URL:", public_url)
        return public_url
    else:
        print("Ошибка при получении информации о туннеле")



# вебхук для взаимодействия с API TG
def run_tg_webhook(webhook_url=get_ngrok_public_url()):
    api_url = f"https://api.telegram.org/bot{token}/setWebhook"
    data = {"url": webhook_url}
    headers = {"Content-Type": "application/json"}

    response = requests.post(api_url, json=data, headers=headers)

    if response.status_code == 200:
        print("Вебхук успешно установлен!")
    else:
        print(f"Ошибка при установке вебхука: {response.status_code} - {response.text}")
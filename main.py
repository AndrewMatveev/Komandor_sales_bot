"""Модуль main - точка входа. Нужен для вызова из этого файла из консоли для начала взаимодействия с программой"""
from webworker import run_tg_webhook
from controller import app


if __name__ == '__main__':
    run_tg_webhook()
    app.run()
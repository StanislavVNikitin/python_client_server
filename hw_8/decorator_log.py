import sys
import logging
import time
import inspect
import logs.client_log_config
import logs.server_log_config


def log(func):
    def logger(*args, **kwargs):
        func_args = func(*args, **kwargs)
        log_name = "server" if "server.py" in sys.argv[0] else "client"
        log_save = logging.getLogger(log_name)
        log_save.debug(f"\nОтчёт о вызове функции:\n"
                       f"Время вызова функции: {time.asctime()}\n"
                       f"Имя функции: {func.__name__}\n"
                       f"Аргументы функции: {args}, {kwargs}\n"
                       f"Функция вызвана из функции: {inspect.stack()[1][3]}\n"
                       f"Функция вызвана из модуля: {func.__module__}\n")
        return func_args
    return logger

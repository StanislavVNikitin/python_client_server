import json
import logging
import sys
import argparse
from decorator_log import log
import logs.client_log_config
from socket import socket, AF_INET, SOCK_STREAM
from common.config import default_port, default_ip_address
from common.mylib import get_message, send_message, jim_presence, check_response, \
    msgs_from_server, user_interaction

client_logger = logging.getLogger("client")


@log
def client_connect_func():
    client_logger.info(f"Происходит соединение с сервером\n"
                       f"Порт сервера: {default_port}\n"
                       f"Адрес сервера: {default_ip_address}")

    client_parser = argparse.ArgumentParser()
    client_parser.add_argument("addr", default=default_ip_address, nargs="?")
    client_parser.add_argument("port", default=default_port, type=int, nargs="?")
    client_parser.add_argument("-m", "--mode", default="send", nargs="?")
    namespace = client_parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    if not 1023 < server_port < 65536:
        client_logger.critical(f"Попытка запуска клиента с неподходящим номером порта: {server_port}\n"
                               f"В качестве порта может быть указано только число в диапазоне от 1024 до 65535")
        sys.exit(1)
    if client_mode not in ["send", "listen"]:
        client_logger.critical(f"Указан неизвестный режим работы клиента: {client_mode}")
        sys.exit(1)

    print(f"Консольный менеджер запущен\n"
          f"Имя пользователя: Guest\n"
          f"Режим работы: {client_mode}")
    client_logger.info(f"Запущен клиент с параметрами:\n"
                       f"Адрес сервера: {server_address}\n"
                       f"Порт сервера: {server_port}\n"
                       f"Режим работы: {client_mode}")
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((server_address, server_port))
        send_message(client_socket, jim_presence())
        client_logger.info(f"Отправлено сообщение:\n"
                           f"{jim_presence()}")
        server_msg = check_response(get_message(client_socket))
        client_logger.info(f"Установлено соединение с сервером\n"
                           f"Ответ сервера: {server_msg}")
        print("Установлено соединение с сервером")
    except json.JSONDecodeError:
        print("Не удалось декодировать сообщение от сервера!")
        client_logger.error("Не удалось декодировать сообщение от сервера!")
        sys.exit(1)
    except Exception as err:
        print(f"Ошибка сервера: {err}")
        client_logger.error(f"Ошибка сервера: {err}")
    except (ConnectionRefusedError, ConnectionError):
        client_logger.critical(f"Не удалось подключиться к серверу {server_address}:{server_port}")
        sys.exit(1)
    else:
        while True:
            if client_mode == "send":
                try:
                    send_message(client_socket, user_interaction(client_socket))
                except (ConnectionRefusedError, ConnectionError, ConnectionAbortedError):
                    client_logger.error(f"Ошибка соединения с сервером: {server_address}")
                    sys.exit(1)
            if client_mode == "listen":
                try:
                    msgs_from_server(get_message(client_socket))
                except (ConnectionRefusedError, ConnectionError, ConnectionAbortedError):
                    client_logger.error(f"Ошибка соединения с сервером: {server_address}")
                    sys.exit(1)


if __name__ == "__main__":
    client_connect_func()

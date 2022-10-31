"""
1. Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant messaging):
клиент отправляет запрос серверу; сервер отвечает соответствующим кодом результата.
Клиент и сервер должны быть реализованы в виде отдельных скриптов, содержащих соответствующие функции.
Функции клиента: сформировать presence-сообщение; отправить сообщение серверу; получить ответ сервера;
разобрать сообщение сервера; параметры командной строки скрипта client.py <addr> [<port>]: addr — ip-адрес сервера;
port — tcp-порт на сервере, по умолчанию 7777. Функции сервера: принимает сообщение клиента; формирует ответ клиенту;
отправляет ответ клиенту; имеет параметры командной строки: -p <port> — TCP-порт для работы (по умолчанию использует 7777);
-a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
"""

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from common.config import DEFAULT_SERVER_PORT, DEFAULT_SERVER_ADDRESS, LISTEN_COUNT, MAX_PACKAGE_LENGTH, ENCODING, ACTION, PRESENCE, USER, ACCOUNT_NAME, TIME, RESPONSE, ERROR
from common.mylib import send_msg, get_msg
import json
import sys
import logging
import logs.server_log_config

server_logger = logging.getLogger("server")

def out_client_msg(message):

    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

def main():
        try:
                if '-p' in sys.argv:
                        listen_port = int(sys.argv[sys.argv.index('-p') + 1])
                else:
                        listen_port = DEFAULT_SERVER_PORT
                if listen_port < 1024 or listen_port > 65535:
                        raise ValueError
        except IndexError:
                server_logger.error('После параметра -\'p\' необходимо указать номер порта.')
                sys.exit(1)
        except ValueError:
                server_logger.error('Номер порта может быть указано только в диапазоне от 1024 до 65535.')
                sys.exit(1)

        try:
                if '-a' in sys.argv:
                        listen_server_address = sys.argv[sys.argv.index('-a') + 1]
                else:
                        listen_server_address = DEFAULT_SERVER_ADDRESS

        except IndexError:
                server_logger.error('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
                sys.exit(1)

        SERV_SOCK = socket(AF_INET, SOCK_STREAM)
        SERV_SOCK.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        SERV_SOCK.bind((listen_server_address, listen_port))
        SERV_SOCK.listen(LISTEN_COUNT)

        while True:
                CLIENT_SOCK, ADDR = SERV_SOCK.accept()
                try:
                        server_logger.info(f"Происходит подключение клиента {ADDR}")
                        msg_client = get_msg(CLIENT_SOCK)
                        server_logger.debug(f"Принятое сообщенеи от клиента {msg_client}")
                        response = out_client_msg(msg_client)
                        send_msg(CLIENT_SOCK, response)
                        CLIENT_SOCK.close()
                except (ValueError, json.JSONDecodeError):
                        server_logger.error("Принято некорректное сообщение от клиента.")
                        CLIENT_SOCK.close()

if __name__ == '__main__':
        main()

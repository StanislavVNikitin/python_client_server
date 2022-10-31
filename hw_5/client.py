""" Клменская программа запускается с параметрами [Host]:[Port]"""

import sys
import json
import time
import logging
import logs.client_log_config

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from common.config import DEFAULT_SERVER_PORT, DEFAULT_SERVER_ADDRESS, LISTEN_COUNT, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR
from common.mylib import send_msg, get_msg

client_logger = logging.getLogger("client")

def process_ans(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError

def connect_msg(account_name='Guest'):
    return {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }

def main():

    try:
        if sys.argv[1]:
            connect_argument = str(sys.argv[1]).split(':')
            print(connect_argument)
            if len(connect_argument) == 2:
                server_address = connect_argument[0]
                server_port = int(connect_argument[1])
                if server_port < 1024 or server_port > 65535:
                    client_logger.critical(f"Указан неподходящий порт для запуска сервера")
                    raise ValueError
            elif len(connect_argument) == 1:
                server_address = connect_argument[0]
                server_port = DEFAULT_SERVER_PORT
            else:
                if DEFAULT_SERVER_ADDRESS == '':
                    server_address = '127.0.0.1'
                else:
                    server_address = DEFAULT_SERVER_ADDRESS
                server_port = DEFAULT_SERVER_PORT

    except IndexError:
        client_logger.debug("Установлены значения адреса и порта по умолчанию")
        if DEFAULT_SERVER_ADDRESS == '':
            server_address = '127.0.0.1'
        else:
            server_address = DEFAULT_SERVER_ADDRESS
        server_port = DEFAULT_SERVER_PORT
    except ValueError:
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    CLIENT_SOCK = socket(AF_INET, SOCK_STREAM)
    client_logger.info(f"Происходит соединение с сервером {server_address} порт {server_port}")
    CLIENT_SOCK.connect((server_address, server_port))
    message_to_server = connect_msg()
    send_msg(CLIENT_SOCK, message_to_server)
    try:
        answer = process_ans(get_msg(CLIENT_SOCK))
        client_logger.debug(f"Ответ сервера: {answer}")
    except (ValueError, json.JSONDecodeError):
        client_logger.error("Не удалось декодировать сообщение от сервера!")


if __name__ == '__main__':
        main()

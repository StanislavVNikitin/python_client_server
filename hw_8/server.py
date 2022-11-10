import logging
import sys
import argparse
from select import select
from decorator_log import log
import logs.server_log_config
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from common.config import default_port, connections, to_user
from common.mylib import get_message, client_message, msg_to_client

server_logger = logging.getLogger("server")


@log
def server_connect_func():
    server_logger.debug(f"Происходит соединение с портом {default_port}")
    server_parser = argparse.ArgumentParser()
    server_parser.add_argument("-p", default=default_port, type=int, nargs="?")
    server_parser.add_argument("-a", default="", nargs="?")
    namespace = server_parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    if not 1023 < listen_port < 65536:
        server_logger.critical(f"Попытка запуска сервера с указанием неподходящего порта {listen_port}\n"
                               f"В качестве порта может быть указано только число в диапазоне от 1024 до 65535")
        sys.exit(1)

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind((listen_address, listen_port))
    server_socket.settimeout(0.5)
    server_socket.listen(connections)

    clients = []
    messages = []
    names = {}
    while True:
        try:
            client, client_address = server_socket.accept()
        except OSError:
            pass
        else:
            server_logger.info(f"Установлено соединение с клиентом: {client_address}")
            clients.append(client)

        rec_data = []
        send_data = []
        try:
            if clients:
                rec_data, send_data, _ = select(clients, clients, [], 0)
        except OSError:
            pass

        if rec_data:
            for client_with_msg in rec_data:
                try:
                    client_message(get_message(client_with_msg), messages, client_with_msg, clients, names)
                    server_logger.info(f"Сообщение от {client_with_msg.getpeername()} принято")
                except Exception:
                    server_logger.info(f"{client_with_msg.getpeername()} отключился от сервера")
                    clients.remove(client_with_msg)
        for msg in messages:
            try:
                msg_to_client(msg, names, send_data)
            except Exception:
                server_logger.info(f"Связь с клиентом {msg[to_user]} была потеряна")
                clients.remove(names[msg[to_user]])
                del names[msg[to_user]]
        messages.clear()


if __name__ == "__main__":
    server_connect_func()

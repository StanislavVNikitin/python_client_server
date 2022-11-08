import logging
import sys
import argparse
import time
from select import select
from decorator_log import log
import logs.server_log_config
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from common.config import default_port, connections, action, msg_time
from common.mylib import get_message, client_message, send_message

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
    server_socket.settimeout(1)
    server_socket.listen(connections)

    clients = []
    messages = []

    while True:
        try:
            client, client_address = server_socket.accept()
        except OSError:
            pass
        else:
            server_logger.info(f"Установлено соединение с клиентом: {client_address}")
            clients.append(client)

        recv_data = []
        send_data = []
        try:
            if clients:
                recv_data, send_data, _ = select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data:
            for client_recv in recv_data:
                try:
                    client_message(get_message(client_recv), messages, client_recv)
                    server_logger.info(f"Сообщение от {client_recv.getpeername()} принято")
                except Exception:
                    server_logger.info(f"{client_recv.getpeername()} отключился от сервера")
                    clients.remove(client_recv)

        if messages and send_data:
            message = \
                {
                    action: "message",
                    "from": messages[0][0],
                    msg_time: time.time(),
                    "message_text": messages[0][1]
                }
            del messages[0]
            for w_client in send_data:
                try:
                    send_message(w_client, message)
                except:
                    server_logger.info(f"Соединение с клиентом {w_client.getpeername()} было прервано")
                    w_client.close()
                    clients.remove(w_client)


if __name__ == "__main__":
    server_connect_func()

import json
import logging
import sys
import time
from decorator_log import log
from common.config import action, account_name, response, connections, presence, msg_time, user, \
    error, default_port, package_length, my_encoding, to_user, sender, msg_text

client_logger = logging.getLogger("client")
server_logger = logging.getLogger("server")


@log
def get_message(client):
    encoded_response = client.recv(package_length)
    if isinstance(encoded_response, bytes):
        response = json.loads(encoded_response.decode(my_encoding))
        if isinstance(response, dict):
            return response
        else:
            raise ValueError
    else:
        raise ValueError


@log
def send_message(sock, message):
    if not isinstance(message, dict):
        raise TypeError
    sock.send(json.dumps(message).encode(my_encoding))


@log
def create_msg(sock, account_name):
    user_receiver = input("Введите имя получателя: ")
    message = input("Введите сообщение для отправки: ")
    jim_msg = \
        {
            action: "message",
            sender: account_name,
            to_user: user_receiver,
            msg_time: time.time(),
            msg_text: message
        }
    client_logger.debug(f"Сформировано сообщение формата JIM: {jim_msg}")
    try:
        send_message(sock, jim_msg)
        client_logger.info(f"Для пользователя {user_receiver} отправлено сообщение: "
                           f"{jim_msg[msg_text]} от {jim_msg[sender]}")
    except Exception:
        client_logger.critical("Ошибка отправки сообщения")
        sys.exit(1)


@log
def user_interaction(sock, username):
    print(f"Поддерживаемые команды программы:\n"
          f"message - отправить сообщение\n"
          f"exit - завершить соединение\n")
    while True:
        command = input("Введите команду: ")
        if command == "message":
            create_msg(sock, username)
        elif command == "exit":
            print("Завершение соединения")
            time.sleep(1)
            break
        else:
            print("Команда не распознана")


@log
def client_message(message, msg_list, client, clients, names):
    server_logger.info(f"Проверка сообщения от клиента: {message}")
    if action in message and message[action] == presence and msg_time in message \
            and user in message:
        if message[user][account_name] not in names.keys():
            names[message[user][account_name]] = client
            send_message(client, {response: 200})
        else:
            send_message(client, {response: 400, error: "Это имя пользователя уже используется"})
            clients.remove(client)
            client.close()
        return
    elif action in message and message[action] == "message" and to_user in message and msg_time in message \
            and sender in message and msg_text in message:
        msg_list.append(message)
        return
    elif action in message and message[action] == "exit" and account_name in message:
        clients.remove(names[message[account_name]])
        names[message[account_name]].close()
        del names[message[account_name]]
        return
    else:
        send_message(client, {response: 400, error: "Некорректный запрос"})
        return


@log
def msgs_from_server(sock, username):
    while True:
        try:
            message = get_message(sock)
            if action in message and message[action] == "message" and sender in message and to_user in message \
                    and msg_text in message and message[to_user] == username:
                print(f"\nПолучено сообщение от {message[sender]}:\n"
                      f"{message[msg_text]}\n"
                      f"Введите команду: ")
                client_logger.info(f"Получено сообщение от {message[sender]}:\n"
                                   f"{message[msg_text]}")
            else:
                client_logger.error(f"Получено некорректное сообщение с сервера: {message}")
        except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError):
            client_logger.critical("Потеряно соединение с сервером")
            break


@log
def msg_to_client(message, names, listen_socks):
    if message[to_user] in names and names[message[to_user]] in listen_socks:
        send_message(names[message[to_user]], message)
        server_logger.info(f"Сообщение {message} отправлено {message[to_user]} от {message[sender]}")
    elif message[to_user] in names and names[message[to_user]] not in listen_socks:
        raise ConnectionError
    else:
        server_logger.error(f"Ошибка отправки сообщения от {message[sender]}")


@log
def jim_presence(acc_name):
    msg = \
        {
            action: presence,
            msg_time: time.time(),
            user: {account_name: acc_name}
        }
    client_logger.debug(f"Готово к отправке {presence} для пользователя {acc_name}")
    return msg


@log
def check_response(message):
    client_logger.debug(f"Проверка сообщения: {message}")
    if response in message:
        if message[response] == 200:
            return "200: OK"
        elif message[response] == 400:
            raise Exception(f"400: {message[error]}")
    raise ValueError

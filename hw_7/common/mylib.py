import json
import logging
import sys
import time
from decorator_log import log
from common.config import action, account_name, response, connections, presence, msg_time, user, \
    error, default_port, package_length, encoding

client_logger = logging.getLogger("client")
server_logger = logging.getLogger("server")


@log
def get_message(client):
    encoded_response = client.recv(package_length)
    if isinstance(encoded_response, bytes):
        response = json.loads(encoded_response.decode(encoding))
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


@log
def send_message(sock, message):
    if not isinstance(message, dict):
        raise TypeError
    js_msg = json.dumps(message).encode(encoding)
    sock.send(js_msg)
    client_logger.info(f"Отправлено сообщение: {js_msg}")


@log
def create_msg(acc_name="User"):
    message = input("Введите сообщение для отправки: ")
    jim_msg = \
        {
            action: "message",
            msg_time: time.time(),
            account_name: acc_name,
            "message_text": message
        }
    client_logger.debug(f"Сформировано сообщение формата JIM: {jim_msg}")
    return jim_msg


@log
def user_interaction(sock, username="User"):
    print(f"Поддерживаемые команды программы:\n"
          f"message - отправить сообщение\n"
          f"exit - завершить соединение\n")
    while True:
        command = input("Введите команду: ")
        if command == "message":
            create_msg()
        elif command == "exit":
            exit_msg = \
                {
                    action: "exit",
                    msg_time: time.time(),
                    account_name: username
                }
            send_message(sock, exit_msg)
            print("Завершение соединения")
            time.sleep(1)
            break
        else:
            print("Команда не распознана")


@log
def client_message(message, msg_list, client):
    server_logger.debug(f"Проверка сообщения от клиента: {message[user][account_name]}")
    if action in message and message[action] == presence and msg_time in message \
            and user in message and message[user][account_name] == "User":
        send_message(client, {response: 200})
        return
    elif action in message and message[action] == "message" and msg_time in message \
            and "message_text" in message:
        msg_list.append((message[account_name], message["message_text"]))
        return
    else:
        send_message(client, {response: 400, error: "Некорректный запрос"})
        return


@log
def msgs_from_server(message):
    if action in message and message[action] == "message" and "from" in message \
            and "message_text" in message:
        print(f"Получено сообщение от {message['from']}:\n"
              f"{message['message_text']}")
        client_logger.info(f"Получено сообщение от {message['from']}:\n"
                           f"{message['message_text']}")
    else:
        client_logger.error(f"Получено некорректное сообщение с сервера: {message}")


@log
def jim_presence(acc_name="User"):
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

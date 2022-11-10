# Проверка функций сервера
import json
import unittest
import sys
import os

sys.path.append(os.path.join(os.getcwd(), '..'))
from server_content.variables import action, account_name, response, connections, presence, msg_time, user, \
    error, default_port, response_ip_address, package_length, encoding
from server_content.functions import get_message, send_message, client_message, jim_presence, check_response


class TestClientMessage(unittest.TestCase):
    error_msg = {response_ip_address: 400, error: "Ошибка отправки сообщения"}
    ok_msg = {response: 200}

    def test_client_message(self):  # правильное сообщение
        self.assertEqual(client_message({action: presence, msg_time: 1.1, user: {account_name: "User"}}), self.ok_msg)

    def test_missing_user(self):  # нет имени клиента
        self.assertEqual(client_message({action: presence, msg_time: 1.1}), self.error_msg)

    def test_missing_action(self):  # нет действия
        self.assertEqual(client_message({msg_time: 1.1, user: {account_name: "User"}}), self.error_msg)

    def test_missing_time(self):  # нет времение
        self.assertEqual(client_message({action: presence, user: {account_name: "User"}}), self.error_msg)

    def test_only_action(self):  # есть только действие
        self.assertEqual(client_message({action: presence}), self.error_msg)

    def test_only_time(self):  # есть только время
        self.assertEqual(client_message({msg_time: 1.1}), self.error_msg)

    def test_only_user(self):  # есть только имя клиента
        self.assertEqual(client_message({user: {account_name: "User"}}), self.error_msg)


class TestSocket:
    def __init__(self, test_msg):
        self.test_msg = test_msg
        self.encoded_msg = None
        self.received_msg = None

    def send(self, msg):
        self.encoded_msg = json.dumps(self.test_msg).encode(encoding)
        self.received_msg = msg

    def recv(self, msg_len):
        return json.dumps(self.test_msg).encode(encoding)


class TestSendGetMessages(unittest.TestCase):
    test_send_msg = \
        {
            action: presence,
            msg_time: 1.1,
            user: {account_name: "test_user"}
        }
    test_received_ok_msg = {response: 200}
    test_received_error_msg = {response_ip_address: 400, error: "Ошибка отправки сообщения"}

    def test_send_message(self):  # проверка схожести сообщений
        test_socket = TestSocket(self.test_send_msg)
        self.assertEqual(test_socket.encoded_msg, test_socket.received_msg)

    def test_type_msg(self):  # разные типы сообщений
        test_socket = TestSocket(self.test_send_msg)
        self.assertRaises(TypeError, send_message, test_socket)

    def test_get_message_ok(self):  # правильные сообщения
        test_socket_ok = TestSocket(self.test_received_ok_msg)
        self.assertEqual(get_message(test_socket_ok), self.test_received_ok_msg)

    def test_get_message_error(self):  # неправильные сообщения
        test_socket_error = TestSocket(self.test_received_error_msg)
        self.assertEqual(get_message(test_socket_error), self.test_received_error_msg)


if __name__ == '__main__':
    unittest.main()

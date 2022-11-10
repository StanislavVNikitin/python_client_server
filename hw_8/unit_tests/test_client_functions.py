# Проверка функций клиента
# Функции get_message и send_message уже проверены в файле с проверками функций сервера
import unittest
import sys
import os

sys.path.append(os.path.join(os.getcwd(), '..'))
from server_content.variables import action, account_name, response, connections, presence, msg_time, user, \
    error, default_port, response_ip_address, package_length, encoding
from server_content.functions import jim_presence, check_response


class TestJimPresence(unittest.TestCase):
    test_jim_msg = jim_presence()
    test_jim_msg[msg_time] = 1.1
    test_not_func_jim_msg_ok = \
        {
            action: presence,
            msg_time: 1.1,
            user: {account_name: "User"}
        }
    test_not_func_jim_msg_error = \
        {
            action: presence,
            msg_time: 1.1,
        }
    # not_func - сообщение сделано не функцией
    # в test_not_func_jim_msg_error нет имени клиента
    test_jim_msg_list = [{action: presence, msg_time: 1.1, user: {account_name: "User"}}]

    def test_jim_ok_presence(self):  # сравнение двух сообщений формата jim
        self.assertEqual(self.test_jim_msg, self.test_not_func_jim_msg_ok)

    def test_jim_error_presence(self):  # сравнение двух сообщений формата jim, одно ошибочное
        self.assertNotEqual(self.test_jim_msg, self.test_not_func_jim_msg_error)

    def test_type_jim_presence(self):  # сравнение типов сообщений формата jim
        self.assertRaises(TypeError, self.test_jim_msg, self.test_jim_msg_list)

    def test_jim_type(self):   # проверка сообщения на тип dict
        self.assertIsInstance(self.test_jim_msg, dict)

    def test_not_dict_jim_type(self):  # проверка неправильного сообщения на тип dict
        self.assertNotIsInstance(self.test_jim_msg_list, dict)


class TestCheckResponse(unittest.TestCase):
    def test_response_200(self):  # проверка положительного результата check_response
        self.assertEqual(check_response({response: 200}), "200: OK")

    def test_response_400(self):  # проверка отрицательного результата check_response
        self.assertEqual(check_response({response: 400, error: "Ошибка отправки сообщения"}),
                         "400: Ошибка отправки сообщения")

    def test_response_empty(self):  # проверка на полноту содержимого check_response
        self.assertRaises(ValueError, check_response, {error: "Ошибка отправки сообщения"})

    def test_responses_not_equal(self):  # сравнение положительного и отрицательного результатов check_response
        self.assertNotEqual(check_response({response: 200}), "400: Ошибка отправки сообщения")


if __name__ == '__main__':
    unittest.main()

""" Библиотека общих функций """

import json
import time
from common.config import MAX_PACKAGE_LENGTH, ENCODING, DEFAULT_SERVER_PORT, DEFAULT_SERVER_ADDRESS, LISTEN_COUNT, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR

def get_msg(sock):
    bytes_response = sock.recv(MAX_PACKAGE_LENGTH)
    json_response = bytes_response.decode(ENCODING)
    response = json.loads(json_response)
    return response

def send_msg(sock, message):
    json_message = json.dumps(message)
    encoded_message = json_message.encode(ENCODING)
    sock.send(encoded_message)


def test_func():
    print('test')

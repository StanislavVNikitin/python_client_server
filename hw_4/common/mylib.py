""" Библиотека общих функций """

import json
import time
from common.config import MAX_PACKAGE_LENGTH, ENCODING, DEFAULT_SERVER_PORT, DEFAULT_SERVER_ADDRESS, LISTEN_COUNT, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR

def get_msg(sock):
    bytes_response = sock.recv(MAX_PACKAGE_LENGTH)
    if isinstance(bytes_response, bytes):
        json_response = bytes_response.decode(ENCODING)
        if isinstance(json_response, str):
            response = json.loads(json_response)
            if isinstance(response, dict):
                return response
            raise ValueError
        raise ValueError
    raise ValueError

def send_msg(sock, message):
    if not isinstance(message, dict):
        raise TypeError
    json_message = json.dumps(message)
    encoded_message = json_message.encode(ENCODING)
    sock.send(encoded_message)


def test_func():
    print('test')

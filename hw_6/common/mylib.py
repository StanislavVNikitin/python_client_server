""" Библиотека общих функций """

import logging
import json
import time
from common.config import MAX_PACKAGE_LENGTH, ENCODING, DEFAULT_SERVER_PORT, DEFAULT_SERVER_ADDRESS, LISTEN_COUNT, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR
from decorator_log import log
client_logger = logging.getLogger("client")
server_logger = logging.getLogger("server")

@log
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

@log
def send_msg(sock, message):
    if not isinstance(message, dict):
        raise TypeError
    json_message = json.dumps(message)
    encoded_message = json_message.encode(ENCODING)
    sock.send(encoded_message)

@log
def test_func():
    print('test')

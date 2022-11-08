import logging.handlers
import os
import sys

server_log = logging.getLogger("server")
server_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")

server_path = os.path.dirname(os.path.abspath(__file__))
server_path = os.path.join(server_path, "server.log")

server_stream = logging.StreamHandler(sys.stdout)
server_stream.setFormatter(server_formatter)
server_stream.setLevel(logging.WARNING)

server_rotate = logging.handlers.TimedRotatingFileHandler(server_path, encoding="utf-8", interval=1, when="midnight")
server_rotate.setFormatter(server_formatter)

server_log.addHandler(server_stream)
server_log.addHandler(server_rotate)
server_log.setLevel(logging.DEBUG)

if __name__ == "__main__":
    server_log.debug("Отладочная информация")
    server_log.info("Информационное сообщение")
    server_log.warning("Предупреждение")
    server_log.error("Ошибка")
    server_log.critical("Критическая ошибка/сообщение")

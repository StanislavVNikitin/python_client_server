import logging
import os
import sys

clien_log = logging.getLogger("client")
client_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")

client_path = os.path.dirname(os.path.abspath(__file__))
client_path = os.path.join(client_path, "client.log")

client_stream = logging.StreamHandler(sys.stdout)
client_stream.setFormatter(client_formatter)
client_stream.setLevel(logging.WARNING)

client_file = logging.FileHandler(client_path, encoding="utf-8")
client_file.setFormatter(client_formatter)

clien_log.addHandler(client_stream)
clien_log.addHandler(client_file)
clien_log.setLevel(logging.DEBUG)

if __name__ == "__main__":
    clien_log.debug("Отладочная информация")
    clien_log.info("Информационное сообщение")
    clien_log.warning("Предупреждение")
    clien_log.error("Ошибка")
    clien_log.critical("Критическая ошибка/сообщение")

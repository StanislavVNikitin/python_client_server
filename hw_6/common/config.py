""" Константы - настройки """


DEFAULT_SERVER_PORT = 7777
DEFAULT_SERVER_ADDRESS = ''
LISTEN_COUNT = 5
MAX_PACKAGE_LENGTH = 2048
ENCODING='utf-8'

# Протокол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
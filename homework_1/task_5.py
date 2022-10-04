"""
5. Написать код, который выполняет пинг веб-ресурсов yandex.ru, youtube.com
и преобразовывает результат из байтовового типа данных в строковый без ошибок
для любой кодировки операционной системы.
"""

import subprocess
import platform
from chardet import detect

params = '-n' if platform.system().lower() == 'windows' else '-c'

site_list = ['yandex.ru', 'youtube.com']

for site in site_list:
    args = ['ping', params, '4', site]
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in process.stdout:
        result = detect(line)
        print('result = ', result)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8'))



"""
5. Написать код, который выполняет пинг веб-ресурсов yandex.ru, youtube.com
и преобразовывает результат из байтовового типа данных в строковый без ошибок
для любой кодировки операционной системы.
Вариант с модулем locale и получением кодировки через метод getpreferredencoding не работает в Windows
так как метод getpreferredencoding получает кодировку текста в файах которая в Windows cp1251, а кодировка консоли
отличается ibm866(эта кодировка еще с консоли DOS для поддержки так и осталась). В результате вывод в Windows
из за неправильного перекодирования из кодировки cp1251 в место кодировки консоли ibm866 в utf-8 кривой:
#####

ЋЎ¬Ґ­ Ї ЄҐв ¬Ё б yandex.ru [77.88.55.77] б 32 Ў ©в ¬Ё ¤ ­­ле:
ЋвўҐв ®в 77.88.55.77: зЁб«® Ў ©в=32 ўаҐ¬п=9¬б TTL=248
ЋвўҐв ®в 77.88.55.77: зЁб«® Ў ©в=32 ўаҐ¬п=12¬б TTL=248

#####

"""

import subprocess
import platform
from locale import getpreferredencoding


params = '-n' if platform.system().lower() == 'windows' else '-c'
encoding = getpreferredencoding()
site_list = ['yandex.ru', 'youtube.com']

for site in site_list:
    args = ['ping', params, '4', site]
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in process.stdout:
        line = line.decode(encoding).encode('utf-8')
        print(line.decode('utf-8'))



"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».
Далее забыть о том, что мы сами только что создали этот файл и исходить из того,
что перед нами файл в неизвестной кодировке. Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости от того,
в какой кодировке он был создан.
"""
from chardet import detect

str_list = ['сетевое программирование','сокет','декоратор']
f = open('string_file.txt', 'w', encoding='utf-8')
for str in str_list:
    f.write(str+'\n')
f.close()

with open('string_file.txt', 'rb') as f:
    content = f.read()
    encoding = detect(content)['encoding']

with open('string_file.txt', encoding=encoding) as f_n:
    f_n.seek(0)
    for el_str in f_n:
        print(el_str, end='')
    print()


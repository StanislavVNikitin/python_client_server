"""
3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата.
Для этого: Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список,
второму — целое число, третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом,
отсутствующим в кодировке ASCII (например, €); Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью параметра default_flow_style,
а также установить возможность работы с юникодом: allow_unicode = True;
"""

import yaml

MY_LIST = ['Иванов', 'Петров', 'Сидоров']
TO_NUM = 3
AS_SET = {1:'€', 2:'€', 3:'€'}
DATA_TO_YAML = {'List': MY_LIST, 'Number': TO_NUM, 'Dict': AS_SET}

with open('file.yaml', 'w', encoding='utf-8') as f_n:
    yaml.dump(DATA_TO_YAML, f_n, default_flow_style=False, allow_unicode=True)
"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных
из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:
Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание
данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения
параметров «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра
поместить в соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список для хранения данных отчета — например,
main_data — и поместить в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС»,
«Код продукта», «Тип системы». Значения для этих столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла); Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(), а также сохранение подготовленных данных
в соответствующий CSV-файл; Проверить работу программы через вызов функции write_to_csv().
"""

from chardet import detect
import re
import csv



def reg_ex_search(el_str, reg_exp):
    if re.search(reg_exp, el_str):
        result = re.sub(reg_exp + ':', '', el_str)
        return re.findall(r'\b.+',result)[0]

def get_data(filescan_list):
    reg_ex = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data = []
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []

    for file in filescan_list:
        with open(file, 'rb') as f:
            content = f.read()
            encoding = detect(content)['encoding']
        with open(file, encoding=encoding) as f_n:
            for el_str in f_n:
                for reg in reg_ex:
                    result = reg_ex_search(el_str, reg)
                    if result:
                        if (reg == reg_ex[0]):
                            os_prod_list.append(result)
                        elif (reg == reg_ex[1]):
                            os_name_list.append(result)
                        elif (reg == reg_ex[2]):
                            os_code_list.append(result)
                        elif (reg == reg_ex[3]):
                            os_type_list.append(result)
    main_data.append(reg_ex)
    for i in [0,1,2]:
        main_data.append([os_prod_list[i],os_name_list[i], os_code_list[i], os_type_list[i]])
    return main_data

def write_to_csv(cvsfile):
    file_list = ['info_1.txt', 'info_2.txt', 'info_3.txt']
    main_data = get_data(file_list)
    with open(csvfile, 'w', encoding='utf-8') as f_n:
        F_N_WRITER = csv.writer(f_n)
        for row in main_data:
            F_N_WRITER.writerow(row)



csvfile = 'file.csv'
write_to_csv(csvfile)



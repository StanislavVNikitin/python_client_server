"""
1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип
 и содержание соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые
  представление в формат Unicode и также проверить тип и содержимое переменных.
"""
def print_value_type(my_list):
    my_generic_iterable = map(str.upper, my_list)
    for i in my_generic_iterable:
        print(i)
        print(type(i))

var_1 = 'разработка'
var_2 = 'сокет'
var_3 = 'декоратор'

print_value_type([var_1, var_2, var_3])

var_unicode_list = ['\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430']
var_unicode_list.append('\u0441\u043e\u043a\u0435\u0442')
var_unicode_list.append('\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440')
print_value_type(var_unicode_list)
"""
4. Преобразовать слова «разработка», «администрирование», «protocol»,
 «standard» из строкового представления в байтовое и выполнить обратное
  преобразование (используя методы encode и decode).
"""
var_list = ['разработка', 'администрирование', 'protocol','standard']

for i in var_list:
        var_tmp_encode = i.encode('utf-8')
        print(f" '{var_tmp_encode}' тип: '{type(var_tmp_encode)}'")
        var_tmp_decode = var_tmp_encode.decode('utf-8')
        print(f" '{var_tmp_decode}' тип: '{type(var_tmp_decode)}'")



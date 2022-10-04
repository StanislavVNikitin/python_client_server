"""
2. Каждое из слов «class», «function», «method» записать в байтовом типе. Сделать это необходимо в автоматическом,
 а не ручном режиме, с помощью добавления литеры b к текстовому значению, (т.е. ни в коем случае не используя
  методы encode, decode или функцию bytes) и определить тип, содержимое и длину соответствующих переменных.
"""

var_1 = 'class'
var_2 = 'function'
var_3 = 'method'

for i in [var_1,var_2,var_3]:
    var_str_byte = eval(f"b'{i}'")
    print(f" {var_str_byte} type: {type(var_str_byte)} len: {len(var_str_byte)}")


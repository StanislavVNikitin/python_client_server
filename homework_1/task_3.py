"""
3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
Важно: решение должно быть универсальным, т.е. не зависеть от того, какие конкретно слова мы исследуем.
"""

var_1 = 'attribute'
var_2 = 'класс'
var_3 = 'функция'
var_4 = 'type'

for word in [var_1,var_2,var_3,var_4]:
    try:
        bytes(word,'ascii')
    except UnicodeEncodeError:
        print(f"Слово '{word}' не возможно преобразовать в вид bytes")


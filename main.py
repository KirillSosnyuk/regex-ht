# Импорт библиотек
import re
import csv

#Чтение из файла
with open("phonebook_raw.csv", encoding='utf-8') as file:
    rows = csv.reader(file, delimiter=",")
    contacts_list = list(rows)

# Формирование текста из списка
res = ','.join(contacts_list[0]) + '\n'

# 1) Если есть пропуски - проваливаемся в блок if
# 2) Активируем флаг и создаем ссылку на инициалы
# 3,4,5) Во втором цикле производим поиск совпадения по инициалам, если таковое имеется
#        Если есть - добавляем в переменную res из двух списков(текущего и совпадения) непустые значения; если они в обоих пустые, то будет ""
#        Деактивируем флаг
# 6) Если совпадений нет, тогда флаг активирован - определяем инициалы и добавляем в res
for index, employee in enumerate(contacts_list):
    if '' in employee:
        flag = True
        employee_initials = ' '.join(employee[0:3]).split()
        for match in contacts_list[index+1:]:
            match_initials = ' '.join(match[0:3]).split()
            if match_initials[0:2] == employee_initials[0:2]:
                initials = ','.join(match_initials) if len(match_initials) > len(employee_initials) else ','.join(employee_initials)
                res += initials + ',' + ','.join([match[position] if match[position] != '' else employee[position] for position in range(3, len(contacts_list[0]))]) + '\n'
                flag = False
                break
        if flag and not ','.join(employee_initials) in res:
            res += ','.join(employee_initials) + ',' + ','.join(employee[3:]) + '\n'

# Определяем паттерн и производим замену через re
pattern = r'(\+7|8)?[\s\-\(]*([\d+]{3,3})[\s\-\)]*([\d+]{3,3})[\s\-]*([\d+]{2,2})?[\s\-]*([\d+]{2,2})?( *\(?[дД][а-я|А-Я]*[\. :-]*)?([\d+]{2,4}\)?)?'
result = re.sub(pattern, r'+7(\2)\3-\4-\5', res)

# Формируем список для записи в файл
final_list = map(lambda el: el.split(','), result.split('\n')[:-1])

# Записываем в файл
with open("phonebook.csv", "w", encoding='utf-8', newline='') as file:
    datawriter = csv.writer(file, delimiter=',')
    datawriter.writerows(final_list)
"""

Домашнее задание №1

Цикл for: Оценки

* Создать список из словарей с оценками учеников разных классов 
  школы вида [{'school_class': '4a', 'scores': [3,4,4,5,2]}, ...]
* Посчитать и вывести средний балл по всей школе.
* Посчитать и вывести средний балл по каждому классу.
"""
import string
import random


def main(classes):
    """
    Эта функция вызывается автоматически при запуске скрипта в консоли
    В ней надо заменить pass на ваш код
    """
    sum_by_school = 0
    for school_class in classes:
        average_by_class = sum(school_class['scores']) / len(school_class['scores'])
        print(f"Класс {school_class['school_class']}: {average_by_class}")
        sum_by_school += average_by_class
    average_by_school = round(sum_by_school / len(classes), 1)
    print(f'Средняя оценка по школе: {average_by_school}')


if __name__ == "__main__":
    school = [{
        'school_class': str(random.randint(1, 11)) + random.choice(string.ascii_lowercase[:5]),
        'scores': [random.randint(1, 5) for i in range(5)]
    } for i in range(5)]
    main(school)

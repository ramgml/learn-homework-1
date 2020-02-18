"""

Домашнее задание №1

Исключения: KeyboardInterrupt

* Перепишите функцию ask_user() из задания while2, чтобы она 
  перехватывала KeyboardInterrupt, писала пользователю "Пока!" 
  и завершала работу при помощи оператора break
    
"""

def ask_user():
    """
    Замените pass на ваш код
    """
    dialog = {"Как дела": "Хорошо!", "Что делаешь?": "Программирую"}
    while True:
        try:
            question = input()
            if question in dialog:
                print(dialog[question])
        except KeyboardInterrupt:
            print('Пока!')
            break

if __name__ == "__main__":
    ask_user()

"""
Домашнее задание №1

Использование библиотек: ephem

* Установите модуль ephem
* Добавьте в бота команду /planet, которая будет принимать на вход 
  название планеты на английском, например /planet Mars
* В функции-обработчике команды из update.message.text получите 
  название планеты (подсказка: используйте .split())
* При помощи условного оператора if и ephem.constellation научите 
  бота отвечать, в каком созвездии сегодня находится планета.

"""
import logging
import ephem
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from collections import defaultdict

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
)


PROXY = {
    'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {
        'username': 'learn', 
        'password': 'python'
    }
}


def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)


def talk_to_me(bot, update):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)


def get_planet_constellation(bot, update):
    message = update.message.text.split()

    if len(message) < 1:
        update.message.reply_text("Name of planet is missing")
        return

    planet_name = message[1]

    planet = getattr(ephem, planet_name, None)

    if planet is None:
        update.message.reply_text(f"I know nothing about {planet_name}")
        return

    short, full = ephem.constellation(planet(datetime.now()))
    update.message.reply_text(full)


def calculate(bot, update):
    message = update.message.text.split()

    if len(message) < 1:
        update.message.reply_text("Забыли указать пример")
        return

    expression = ''.join(message[1:])
    decomposed_expression = defaultdict(str)
    index = 0
    for symbol in expression:
        if symbol.isdigit():
            decomposed_expression[index] += symbol
        else:
            index += 1
            decomposed_expression[index] += symbol
            index += 1

    try:
        if len(decomposed_expression) < 3:
            raise ValueError("Неправильное выражение")

        num1, sign, num2 = decomposed_expression.values()
        num1 = float(num1)
        num2 = float(num2)

        if sign == '+':
            result = num1 + num2
        elif sign == '-':
            result = num1 - num2
        elif sign == '*':
            result = num1 * num2
        elif sign == '/':
            result = num1 / num2
        else:
            raise ValueError("Неправильное выражение")

        answer = result if result - int(result) != 0 else int(result)
    except ZeroDivisionError:
        answer = 'Нельзя делить на ноль'
    except ValueError as e:
        answer = str(e)

    update.message.reply_text(answer)


def main():
    mybot = Updater("КЛЮЧ, КОТОРЫЙ НАМ ВЫДАЛ BotFather", request_kwargs=PROXY)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", get_planet_constellation))
    dp.add_handler(CommandHandler("calc", calculate))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    mybot.start_polling()
    mybot.idle()
       

if __name__ == "__main__":
    main()

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
from cities_game import Game, GameOverException

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


def cities_game(bot, update):
    user_id = update.message.from_user.id
    message = update.message.text.split(maxsplit=1)

    if len(message) < 2:
        update.message.reply_text('Укажите название города')
        return

    try:
        answer = Game(user_id, message[1]).start()
        update.message.reply_text(answer)
    except Exception as e:
        update.message.reply_text("Что-то пошло не так")
        raise e


def main():
    mybot = Updater("КЛЮЧ, КОТОРЫЙ НАМ ВЫДАЛ BotFather", request_kwargs=PROXY)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", get_planet_constellation))
    dp.add_handler(CommandHandler("cities", cities_game))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()
       

if __name__ == "__main__":
    main()

import json
import os.path
import random
from pathlib import Path

CITIES_FILE = 'cities.json'


class GameOverException(Exception):
    pass


class City:
    def __init__(self, city: str):
        self.__city = city

    def get_name(self):
        return self.__city

    def get_first_letter(self):
        return self.__city[0].lower()

    def select_last_letter(self, allowed_letters):
        for letter in reversed(self.__city):
            if letter in allowed_letters:
                return letter


class UserFile:
    def __init__(self, filepath):
        self.__filepath = Path(filepath)

    def get_filepath(self):
        return self.__filepath

    def get_data(self):
        cities = {}
        if os.path.exists(self.__filepath):
            with open(self.__filepath, 'r') as user_file:
                cities = json.load(user_file)
            return cities

        with open(CITIES_FILE, 'r') as cities_file:
            cities['cities'] = json.load(cities_file)
        return cities

    def remove(self):
        if os.path.exists(self.__filepath):
            os.remove(self.__filepath)

    def save(self, data):
        with open(self.__filepath, 'w') as user_file:
            json.dump(data, user_file, ensure_ascii=False)


class User:
    def __init__(self, user_id):
        self.__user_id = user_id
        self.__file = UserFile(Path().cwd() / 'users' / f'{self.__user_id}.json')
        self.__data = self.__file.get_data()

    def get_file(self):
        return self.__file

    def check_city(self, city: City):
        first_letter = city.get_first_letter()
        last_city = self.__data.get('last_city')
        if last_city is not None:
            last_city_selected_letter = City(last_city).select_last_letter(self.__data['cities'].keys())
            if last_city_selected_letter != first_letter:
                return False

        cities_by_letter = self.__data['cities'].get(first_letter)
        return city.get_name() in cities_by_letter

    def find_city(self, city: City):
        letter = city.select_last_letter(self.__data['cities'].keys())
        cities_by_letter = self.__data['cities'].get(letter)

        if not isinstance(cities_by_letter, list) or len(cities_by_letter) < 1:
            raise GameOverException('Игра окончена! Вы победили!')

        return random.choice(cities_by_letter)

    def delete_city(self, city: City):
        letter = city.get_first_letter()
        cities_by_letter = self.__data['cities'].get(letter)
        if cities_by_letter is not None:
            self.__data['cities'][letter] = [word for word in cities_by_letter if word != city.get_name()]

    def change_last_city(self, city: City):
        self.__data['last_city'] = city.get_name()

    def update_file(self):
        self.__file.save(self.__data)


class Game:
    def __init__(self, user_id, city):
        self.__user = User(user_id)
        self.__city = City(city)

    def start(self):
        try:
            if not self.__user.check_city(self.__city):
                raise GameOverException('Город не подходит! Вы проиграли!')
            self.__user.delete_city(self.__city)
            answer_city = City(self.__user.find_city(self.__city))
            self.__user.delete_city(answer_city)
            self.__user.change_last_city(answer_city)
            self.__user.update_file()
            return f'{answer_city.get_name()}, ваш ход!'
        except GameOverException as e:
            self.stop()
            return str(e)

    def stop(self):
        self.__user.get_file().remove()

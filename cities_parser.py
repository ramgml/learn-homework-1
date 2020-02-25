import requests
from bs4 import BeautifulSoup
import json


def parse_cities():
    url = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BE%D0%B2_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8'
    response = requests.get(url)
    wiki_html = response.text
    parser = BeautifulSoup(wiki_html, 'html.parser')

    table = parser.find("table", {"class": "standard"})
    cities_dict = {}
    for tr in table.find_all('tr')[2:]:
        city = tr.find_all('td')[2].find('a').text.strip()
        first_letter = city[0].lower()
        if first_letter in cities_dict:
            cities_dict[first_letter].append(city)
        else:
            cities_dict[first_letter] = list()
            cities_dict[first_letter].append(city)

    with open('cities.json', 'w') as cities_file:
        json.dump(cities_dict, cities_file, ensure_ascii=False)


if __name__ == '__main__':
    parse_cities()


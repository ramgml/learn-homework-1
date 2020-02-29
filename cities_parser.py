from collections import defaultdict
import requests
from bs4 import BeautifulSoup
import json


def parse_cities():
    url = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BE%D0%B2_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8'
    response = requests.get(url)
    wiki_html = response.text
    parser = BeautifulSoup(wiki_html, 'html.parser')

    table = parser.find("table", {"class": "standard"})
    cities = defaultdict(list)
    city_name_column_idx = 2
    without_header_rows = table.find_all('tr')[2:]
    for tr in without_header_rows:
        city = tr.find_all('td')[city_name_column_idx].find('a').text.strip()
        first_letter = city[0].lower()
        cities[first_letter].append(city)

    with open('cities.json', 'w') as cities_file:
        json.dump(cities, cities_file, ensure_ascii=False)


if __name__ == '__main__':
    parse_cities()


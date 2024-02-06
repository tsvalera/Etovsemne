import requests
from bs4 import BeautifulSoup as BS
import random as rnd
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Error(Exception):
    pass


class Animal:
    def __init__(self, page):
        self.page = page
        self.kinds = {}
        self.winner_info = None
        self.winner_picture = None
        self.winner_names = None

    def types_of_animals(self):
        for k in self.page:
            response = requests.get(k, verify=False)
            soup = BS(response.text, 'html.parser')
            quotes = soup.find_all('a', class_='sp-block-item')
            for x in quotes:
                key = x.find('div', {'class': 'title'}).text.strip()
                meaning = x.get('href')
                pict_list = [x.find('img')]
                for j in pict_list:
                    picture = j.get('src')
                    self.kinds[key] = {f'https://moscowzoo.ru{meaning}': f'https://moscowzoo.ru{picture}'}
        return self.kinds

    def random_animals(self):
        self.kinds = self.types_of_animals()
        name_of_animals = []
        for j in self.kinds.keys():
            name_of_animals.append(j)
        return rnd.choice(name_of_animals)

    def win_info(self):
        start_time = time.time()
        self.winner_names = self.random_animals()

        if self.winner_names == 'Большая панда':
            self.win_info()

        else:
            info = self.kinds.get(self.winner_names)
            for j in info.keys():
                self.winner_info = j
            for k in info.values():
                self.winner_picture = k
        end_time = time.time()
        response_time = end_time - start_time
        print(f'{response_time}')
        return self.winner_names, self.winner_info, self.winner_picture

    pass


class Mammals(Animal):
    pass


class Birds(Animal):
    pass


class Reptiles(Animal):
    pass


class Amphibians(Animal):
    pass


class Fish(Animal):
    pass


class Invertebrates(Animal):
    pass




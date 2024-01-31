import requests
import json
from config import keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}!')

        if base == quote:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f'https://api.currencyapi.com/v3/latest?apikey=cur_live_dVzdZ7dOGdGyn9IQAj7ubMp7r0lCn8aayf956olY&currencies={keys[quote]}&base_currency={keys[base]}')
        total_base = round(json.loads(r.content)["data"][f'{keys[quote]}']['value'], 3) * float(amount)

        return total_base
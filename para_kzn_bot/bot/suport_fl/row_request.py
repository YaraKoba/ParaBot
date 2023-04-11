import requests
import telebot


class RowReq:
    def __init__(self, token: str, base_url: str):
        self.TOKEN = token
        self.base_url = base_url

    def prepare_url(self, method: str):
        result_url = f'{self.base_url}/bot{self.TOKEN}/'
        if method:
            result_url += method
        return result_url

    def post(self, method: str = None, params: dict = None, data: dict = None):
        url = self.prepare_url(method)
        pos = requests.post(url, data=data, params=params)
        return pos.json()


class MyBot(telebot.TeleBot):
    def __init__(self, row_req: RowReq, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row_req = row_req

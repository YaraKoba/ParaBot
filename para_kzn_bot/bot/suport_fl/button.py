from aiogram import types
from suport_fl.suport import amdate
from datetime import date, timedelta, datetime


def c_d(numb: int):
    delta = timedelta(days=numb)
    return date.today() + delta


def day_btn():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton(amdate(str(c_d(0))))
    btn2 = types.KeyboardButton(amdate(str(c_d(1))))
    btn3 = types.KeyboardButton(amdate(str(c_d(2))))
    btn4 = types.KeyboardButton(amdate(str(c_d(3))))
    btn5 = types.KeyboardButton(amdate(str(c_d(4))))
    btn6 = types.KeyboardButton(f'Все летные дни!')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup


def spots_btn(spots):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for spot in spots:
        markup.add(types.InlineKeyboardButton(spot['name'], callback_data=spot['name']))
    return markup


def cities_btn(cities):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for city in cities:
        data = f'{city["id"]} {city["name"]}'
        markup.add(types.InlineKeyboardButton(city['name'], callback_data=data))
    return markup


def step_btn():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Да')
    btn2 = types.KeyboardButton('Нет')
    markup.add(btn1, btn2)
    return markup


def day_5():
    return [str(c_d(0)), str(c_d(1)), str(c_d(2)), str(c_d(3)), str(c_d(4))]


def cheng_format_utc(time_utc):
    tilda = timedelta(hours=3)
    return str(datetime.utcfromtimestamp(time_utc) + tilda)

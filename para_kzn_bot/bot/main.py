#!/usr/bin/env python3
from suport_fl import mess, button, suport
from dotenv import load_dotenv
import os

import logging
from aiogram import Bot, Dispatcher, types, executor
from db.manager import ManagerDjango

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
dip = Dispatcher(bot=bot)
manager = ManagerDjango(bot)


@dip.message_handler(commands='start')
async def start_help(message: types.Message):
    print(f'{message.from_user.first_name} - command: {message.text}')
    mes = mess.header_mess(message)
    print(await manager.create_user(message))
    await message.answer(mes, parse_mode='html')
    await change_city(message)
    await show_days(message)


@dip.message_handler(commands='help')
async def get_help(message: types.Message):
    print(f'{message.from_user.first_name} - command: {message.text}')
    mes = mess.help_mess()
    await message.answer(mes, parse_mode='html')


@dip.message_handler(commands=['days'])
async def show_days(message: types.Message):
    print(f'{message.from_user.first_name} - command: {message.text}')
    markup = button.day_btn()
    await message.answer("Даты обновлены", parse_mode='html', reply_markup=markup)


@dip.message_handler(regexp=r'Все летные дни!')
async def all_date_fly(message: types.Message):
    print(f'{message.from_user.first_name} - command: {message.text}')
    date_all = button.day_5()
    user_inf, spots = await manager.get_user_and_spots(message)
    res = await manager.create_meteo_message(city=user_inf['city'], chat_id=user_inf['user_id'], lst_days=date_all)
    await message.answer(res, parse_mode='html')


@dip.message_handler(regexp=r"[А-Я][а-я]\s\d{2}\s[а-я]+\b")
async def one_day_fly(message: types.Message):
    print(f'{message.from_user.first_name} - command: {message.text}')
    try:
        date_f = [suport.re_amdate(message.text)]
        user_inf, spots = await manager.get_user_and_spots(message)
        res = await manager.create_meteo_message(city=user_inf['city'], chat_id=user_inf['user_id'], lst_days=date_f)
        await message.answer(res, parse_mode='html')
    except (IndexError, Exception):
        await show_days(message)


@dip.message_handler(commands=['go', 'stop'])
async def go_start_reminder(message: types.Message):
    print(f'{message.from_user.first_name} - command: {message.text}')
    if message.text in '/go':
        update_inf = {'get_remainder': True}
        await manager.update_user(message, update_inf)
        await message.answer('Теперь вы будете получать уведомления')
    else:
        update_inf = {'get_remainder': False}
        await manager.update_user(message, update_inf)
        await message.answer('Теперь вы НЕ будете получать уведомления')


@dip.message_handler(commands=['city'])
async def change_city(message: types.Message):
    cities = await manager.get_all_city()
    btn_cities = button.cities_btn(cities)
    user_inf, _ = await manager.get_user_and_spots(message)
    await message.answer(f'Текущее место: {user_inf["city_name"]}', reply_markup=btn_cities)


@dip.message_handler(commands=['get_spot'])
async def get_spot(message: types.Message):
    print(f'{message.from_user.first_name} - command: {message.text}')
    user, spots = await manager.get_user_and_spots(message)
    markup = button.spots_btn(spots)
    await message.answer(f'Все добавленные горки города {user["city_name"]}', reply_markup=markup)


@dip.callback_query_handler(lambda c: c.data)
async def process_callback_handler(callback_query: types.CallbackQuery):
    user, spots = await manager.get_user_and_spots(callback_query)
    spot_dict = None
    for spot in spots:
        if callback_query.data == spot['name']:
            spot_dict = spot

    if spot_dict is not None:
        res = mess.mess_get_spot(spot_dict)
        await bot.send_message(user['user_id'], text=res, parse_mode='html')
    else:
        city_inf = callback_query.data.split()
        update_inf = {'city': city_inf[0], 'city_name': city_inf[1]}
        await manager.update_user(callback_query, update_inf)
        await bot.send_message(user['user_id'], text=f"Текущее место изменено на: {city_inf[1]}")


def ran_server():
    executor.start_polling(dip)


if __name__ == '__main__':
    ran_server()

#!/usr/bin/env python3
import asyncio

from dotenv import load_dotenv
from suport_fl import button
import os

import logging
from aiogram import Bot
from db.manager import ManagerDjango

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
manager = ManagerDjango(bot)


async def send_mess(user_id, mess):
    try:
        await bot.send_message(chat_id=user_id, text=mess, parse_mode='html')
    except Exception as err:
        print(err)
        print(f'del user id: {user_id}')
        await manager.del_user(user_id)


async def _main():
    date_all = button.day_5()
    cities = await manager.get_all_city()
    users = await manager.get_all_users()
    res = await asyncio.gather(*(manager.create_meteo_message(city_id['id'], date_all) for city_id in cities))
    city_name = [s['id'] for s in cities]
    result_spots_dict = {t: r for (t, r) in zip(city_name, res)}
    for user in users:
        if user['get_remainder']:
            await send_mess(user['user_id'], result_spots_dict[user['city']])



if __name__ == '__main__':
    asyncio.run(_main())
    # res = manager.create_meteo_message()
    # for user in pull_chat_id():
    #     print(user)
    #     if user[2] in 'Yes':
    #         bot.send_message(user[1], mess.repost(res), parse_mode='html')

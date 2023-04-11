from db.async_requests import RequestToDjango
from bot.suport_fl.mess import get_lst_spots_from_txt
from suport_fl.set_up import *
import asyncio
import json


def add_spots_to_json():
    total = []
    with open('spot_list.txt') as file:
        for line in file:
            d = {
                "url_forecast": "",
                "url_map": "",
                "city_name": "Kazan",
                "city": 1
            }

            gen = ['description',
                   "url_forecast",
                   "wind_max",
                   'wind_min',
                   "wind_degree_r",
                   "wind_degree_l",
                   "lon",
                   "lat",
                   "name",
                   ]
            try:
                line = get_lst_spots_from_txt(line.rstrip())
                for i in line:
                    name = gen.pop()
                    d[name] = i

                total.append(d)

            except IndexError:
                break

    with open('./spots.json', 'w') as j_file:
        json.dump(total, j_file, indent=6, ensure_ascii=False)


async def push_spots():
    req = RequestToDjango(LOCAL_HOST, OPEN_API_HOST)
    with open('./spots.json', 'r') as file:
        spots = json.load(file)

    for spot in spots:
        spot['city'] = 1

    total = spots

    with open('./spots.json', 'w') as j_file:
        json.dump(total, j_file, indent=6, ensure_ascii=True)

    with open('./spots.json', 'r') as file:
        spots = json.load(file)
        for spot in spots:
            print(await req.post_spots(spot))


if __name__ == '__main__':
    asyncio.run(push_spots())


from suport_fl.suport import *
import re


def header_mess(message):
    return (f'<b>Привет, {message.from_user.first_name}!</b>\n'
            f'Бот позволяет узнать где и когда <b>можно полетать</b>.\n'
            f'Каждый день вы будете получать уведомления о погоде,\n'
            f'<b>Команды:</b>\n'
            f'/days - обновить дни\n'
            f'/city - выбрать другой город\n'
            f'/get_spot - Посмотреть добавленные горки\n'
            f'/stop - <b>отключить</b> уведомления\n'
            f'/go - <b>включить</b> уведомления\n'
            f'/help - получить доп. информацию\n\n'
            f'<b>Обозначения в прогнозе:</b>\n'
            f'Ч - Время в часах\n'
            f'В - Ср. скорость ветра в м/с\n'
            f'Пор - Порывы ветра в м/с\n'
            f'Нап - Направление ветра в градусах\n'
            f'% - Оценка погодных условий (Сила и Направление ветра), чем больше процентов, тем лучше условия\n\n'
            f'<b>Выберете город и нажмите на дату, чтобы узнать где полетать</b> &#128526;\n'
            f'p.s. Если вашего города нет в списке, напишите мне @Kobyakov_Yaroslav')


def help_mess():
    return (f'Бот позволяет узнать где и когда <b>можно полетать</b>.\n'
            f'Каждый день вы будете получать уведомления о погоде,\n'
            f'<b>Команды:</b>\n'
            f'/days - обновить дни\n'
            f'/city - выбрать другой город\n'
            f'/get_spot - Посмотреть добавленные горки\n'
            f'/stop - <b>отключить</b> уведомления\n'
            f'/go - <b>включить</b> уведомления\n'
            f'/help - получить доп. информацию\n\n'
            f'<b>Обозначения в прогнозе:</b>\n'
            f'Ч - Время в часах\n'
            f'В - Ср. скорость ветра в м/с\n'
            f'Пор - Порывы ветра в м/с\n'
            f'Нап - Направление ветра в градусах\n'
            f'% - Оценка погодных условий (Сила и Направление ветра), чем больше процентов тем лучше условия\n\n'
            f'Данный бот был создан пилотом из Казани в 2022 году.\n\n'
            f'Дорогой пользователь, \n'
            f'Я хотел бы выразить свою искреннюю благодарность за то, что воспользовались моим чат-ботом. '
            f'Надеюсь, он был вам полезен\n\n'
            f'Бот полностью бесплатный и продолжает развиваться, если вы нашли ошибку или баг, '
            f'пожалуйста, сообщите мне об этом @Kobyakov_Yaroslav.\n\n'
            f'Если вы хотите добавить собственные летные места, напишите мне и я дам вам доступ '
            f'к админ-панели, где можно будет добавлять свои горки.\n\n'
            f'Побольше летных дней и удачи &#128521;\n'
            f'Ваш Кобяков Ярослав')


def err_mess(err):
    now = datetime.now()
    return f"Type:  {str(type(err))[7:-1]}\n"\
           f"Error:  {err}\n"\
           f"Date:  {now.strftime('%d-%m-%Y %H:%M')}"


def meteo_message(all_spot, spots, d):
    str_post = ''
    data = ''

    if type(all_spot) == dict:
        message = amdate(d[0]) if len(d) == 1 else 'В ближайшие 5 дней'
        str_post += f'\n--- <b>{message}</b> ---\n\n'
        str_post += '<u><b>Летная погода не найдена</b></u> &#128530;\n\n'\
                    f'{easy_meteo(all_spot["time"])}'
        return str_post

    for dct in all_spot:
        if data != dct['meteo']['date']:
            data = dct['meteo']['date']
            str_post += f'\n--- <b>{amdate(data)}</b> ---\n\n'
        str_post += f'<u><b>{dct["meteo"]["city"]}</b></u>\n'
        str_post += meteo(dct, spots)

    return str_post


def meteo(a, spots):
    sp_dc = {}
    for sp in spots:
        if sp['name'] == a['meteo']['city']:
            sp_dc = sp
            break

    degree = [(i["win_l"], i["win_r"]) for i in a["fly_time"]]
    fly_hour = [tm['time'][1:-3] for tm in a["fly_time"]]
    only_fly_hour = [tm['time'] for tm in a["fly_time"] if tm['wdg'] > 0 and tm['w_s'] > 0]
    prognoz = sp_dc['url_forecast']
    fly_meteo = [one_hour for one_hour in a['meteo']['time'] if one_hour['time'][1:-3] in fly_hour]

    lst_header = ['Ч', 'В', 'Пор', 'Нап', '%']
    point = (str(int((tm['w_s'] + tm['wdg']) * 100)) for tm in a["fly_time"])
    table_meteo = create_table(lst_header, fly_meteo, point)

    return (f'Направление ветра:  <b>{degree[0][0]}°-{degree[0][1]}°</b>\n'
            f'<u>Общая оценка: <b>{int((a["time_point"] + a["wind_point"]) * 0.5)}%</b></u>\n'
            f'Оценка ветра:  <b>{a["wind_point"]}%</b>\n'
            f'Летные часы:  <b>{a["time_point"]}%</b> \n({" ".join(only_fly_hour)} )\n\n'
            f'&#127777;  {int(middle_temp(a["meteo"]["time"]))}\n'
            f'&#127782;  {ampop(a["meteo"]["time"])}\n'
            f'<pre>{table_meteo}</pre>\n'
            f'<a href="{prognoz}">Подробнее...</a>\n\n\n')


def easy_meteo(a):
    fly_meteo = [one_hour for one_hour in a if str(one_hour['time'][1:-3]) in ['09', '15', '18']]
    lst_header = ['Час', 'Вет', 'Пор', 'Нап']
    table_meteo = create_table(lst_header, fly_meteo)
    return (f'&#127777;  {int(middle_temp(a))}\n'
            f'&#127782;  {ampop(a)}\n'
            f'<pre>{table_meteo}</pre>\n')


def get_lst_spots_from_txt(message):
    reg = r'(\w+\b).+?(\d{2}[\.\,]\d{4}).+?(\d{2}[\.\,]\d{4}).+?(\d+).+?(\d+).+?(\d+).+?(\d+).+?(https?.+?)\s.+?(\w+.+)'
    return re.findall(reg, message)[0]


def mess_get_spot(spot_dict):
    return f'\n\n<b>Название:</b>  {spot_dict["name"]}\n'\
           f'<b>Координаты:</b>  с.ш "{spot_dict["lat"][:7]}", в.д "{spot_dict["lon"][:7]}"\n'\
           f'<b>Направление ветра:</b>  {spot_dict["wind_degree_l"]}°-{spot_dict["wind_degree_r"]}°\n'\
           f'<b>Ветер:</b>  мин - "{spot_dict["wind_min"]} м/с", макс - "{spot_dict["wind_max"]} м/с"\n\n' \
           f'<b><a href="{spot_dict["url_forecast"]}">Windy прогноз</a></b>\n' \
           f'<b><a href="{spot_dict["url_map"]}">Google map</a></b>  \n\n' \
           f'<b>Описание:</b>  {spot_dict["description"]}\n\n\n\n'


if __name__ == '__main__':
    pass

from suport_fl.button import cheng_format_utc as uts
import re


def oneday_meteo(day, j_info, city):
    # print(city, j_info)
    reg = r'(\d{4})(.)(\d{2})(.)(\d{2})(\s.{5})(.+)'
    sun_up = j_info['city']['sunrise']
    sun_down = j_info['city']['sunset']
    oneday_dict = {'city': city, 'date': day, 'sun_up': sun_up, 'sun_down': sun_down, 'time': []}
    for n in j_info['list']:
        day_hour = n
        if day_hour['dt_txt'][:-9] == day:
            time_data = re.sub(reg, r'\6', day_hour['dt_txt'])
            temp = day_hour['main']['temp']
            wind_speed = day_hour['wind']['speed']
            wind_gust = day_hour['wind']['gust']
            wind_degree = day_hour['wind']['deg']
            pop = day_hour['pop']
            try:
                rain = day_hour['rain']['3h']
            except KeyError:
                rain = 0
            oneday_dict['time'] += [{'time': time_data, 'temp': temp, 'wind_speed': wind_speed, 'wind_gust': wind_gust,
                                     'wind_degree': wind_degree, 'pop': pop, 'rain': rain}]
            if time_data == '21:00':
                break
    return oneday_dict


def analytics_main(lst_day: list, meteo_spot_dict, spots):
    meteo_all_days = [oneday_meteo(one_day, meteo_spot_dict[spot], spot)
                      for one_day in lst_day for spot in meteo_spot_dict]

    total_res = ([add_point_to_spot(one_day, spots) for one_day in meteo_all_days
                  if add_point_to_spot(one_day, spots)['time_point'] +
                  add_point_to_spot(one_day, spots)['wind_point'] > 50])

    total_res = sorted(total_res, key=lambda j: j['time_point'] + j['wind_point'], reverse=True)
    total_res = sorted(total_res, key=lambda j: j['meteo']['date'], reverse=False)

    return total_res if len(total_res) > 0 else meteo_all_days[0]


def add_point_to_spot(meteo_one_days, spots):
    spot = meteo_one_days['city']
    sp_d = {}
    for s in spots:
        if s['name'] == spot:
            sp_d = s
    sun_up = uts(meteo_one_days['sun_up'])[11:-3]
    sun_down = uts(meteo_one_days['sun_down'])[11:-3]
    one_day_points = [get_point(tree_h, spot, sp_d) for tree_h in meteo_one_days['time']]
    return analytics_data_point(one_day_points, sun_up, sun_down, meteo_one_days)


def analytics_data_point(o_d_p, sun_up, sun_down, meteo_one_days):
    int_up = int(sun_up[:-3])
    int_down = int(sun_down[:-3])
    sort_hours = [t_h for t_h in o_d_p if int_up - 1 <= int(t_h['time'][:-3]) <= int_down + 1]
    try:
        point_fly_time = int(len([t_h for t_h in sort_hours if t_h['wdg'] > 0
                                  and t_h['w_s'] > 0]) / len(sort_hours) * 100)
        if point_fly_time != 0:
            point_ws_wdg = int(sum([(point['w_s'] + point['wdg']) for point in sort_hours]) / len(sort_hours) * 100)
        else:
            point_ws_wdg = 0
    except ZeroDivisionError:
        point_ws_wdg, point_fly_time = 0, 0
    result = {'time_point': point_fly_time, 'wind_point': point_ws_wdg,
              'fly_time': sort_hours, 'meteo': meteo_one_days}
    return result


def get_point(m_t, spot, spots):
    pop = m_t['pop']
    rain = m_t['rain']
    w_g = m_t['wind_gust']
    w_s = m_t['wind_speed']
    wdg = m_t['wind_degree']
    wdg_l = int(spots['wind_degree_l'])
    wdg_r = int(spots['wind_degree_r'])
    w_min = int(spots['wind_min'])
    w_max = int(spots['wind_max'])
    point_dict = {'time': m_t['time'], 'wdg': 0, 'w_s': 0, 'win_dg': wdg, 'win_l': wdg_l, 'win_r': wdg_r}
    if pop < 0.6 and rain < 0.6 and w_g < 10 and (w_g - w_s) < 7:
        if wdg_l < wdg_r:
            if wdg_l + middle(wdg_l, wdg_r) - 5 <= wdg <= wdg_r - middle(wdg_l, wdg_r) + 5:
                point_dict['wdg'] += 0.25
            if wdg_l <= wdg <= wdg_r:
                point_dict['wdg'] += 0.25
        else:
            if mid_wdg_h(wdg_l, wdg, wdg_r):
                point_dict['wdg'] += 0.25
            if wdg_l <= wdg or wdg_r >= wdg:
                point_dict['wdg'] += 0.25
        if w_min + middle(w_min, w_max) <= w_g <= w_min + middle(w_min, w_max) + 2:
            point_dict['w_s'] += 0.25
        if w_min < w_g <= w_max:
            point_dict['w_s'] += 0.25
    return point_dict


def middle(mn, mx):
    return (mx - mn) / 2


def mid_wdg_h(lef, w, r):
    mid = ((360 - lef) + r) / 2
    if lef + mid - 5 > 360 and r - mid + 5 < 0:
        if lef + mid - 5 - 360 <= w <= lef + mid + 5 - 360:
            return True
    elif lef + mid - 5 < 360 and r - mid + 5 > 0:
        if lef + mid - 5 <= w or r - mid + 5 >= w:
            return True
    else:
        if lef + mid - 5 <= w <= lef + mid + 5:
            return True


if __name__ == '__main__':
    # pass
    for i in analytics_main(['2022-11-22', '2022-11-23', '2022-11-24', '2022-11-25']):
        # print(f't_p - {i["time_point"]}, w_p - {i["wind_point"]} ' + i['meteo']['city'], i['fly_time'])
        print(i)
    # print(analytics_main(['2022-11-20']))
    # spot_dict = get_weather('spot_weather.json')
    # print(add_point_to_spot(oneday_meteo('2022-11-22', spot_dict['Монастырь'], 'Монастырь')))

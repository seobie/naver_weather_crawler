import requests
import csv
from datetime import datetime
from bs4 import BeautifulSoup as bs

isAbroad = False
weather_dic_combined = {}


def today_weather():
    weather_dic = {}
    search_fail = False
    print(datetime.now().strftime('%m월 %d일 %H시 %M분 %S초'))
    weather_dic['시간'] = datetime.now().strftime('%m월 %d일 %H시 %M분 %S초')

    try:
        location_name = soup.find('span', 'btn_select').text
        print(location_name+'의 날씨는 다음과 같습니다.')
        weather_dic['지역명'] = location_name
        global isAbroad
        isAbroad = False
    except:
        try:
            location_name = soup.select('.btn_select > em')[0].text
            isAbroad = True
            print(location_name+'의 날씨는 다음과 같습니다.')
            weather_dic['지역명'] = location_name
        except:    # 모든 예외의 에러 메시지를 출력할 때는 Exception을 사용
            print('해당 지역을 찾을 수 없습니다.')
            search_fail = True
            return True  # for the if statement in the while statement
    try:
        min_temp = soup.find('span', {'class': 'min'}).text
        max_temp = soup.find('span', {'class': 'max'}).text
        min_max_temp = '최저/최고 기온 : '+min_temp+'/'+max_temp
        # print(min_max_temp)
    except:
        isAbroad = True
        # print('no min/max temp exist')

    if search_fail == False and isAbroad == True:
        current_temp = soup.find('span', {'class': 'todaytemp'}).text
        print('현재 온도 : '+current_temp+'℃')
        weather_dic['현재 온도'] = current_temp+'℃'
        cast_text = soup.find('p', 'cast_txt').text
        print(cast_text)
        weather_dic['비고'] = cast_text
        wind_info = soup.find_all('span', 'sensible')
        print('바람 : ' + wind_info[0].text[3:])
        weather_dic['바람'] = wind_info[0].text[3:]
        print('습도 : ' + wind_info[1].text[3:])
        weather_dic['습도'] = wind_info[1].text[3:]
        abroad_uv = soup.select(
            '.info_data > .info_list:nth-child(2) > li:nth-child(3)')[0].text[5:]
        print('자외선 : ' + abroad_uv)
        weather_dic['자외선'] = abroad_uv

    elif search_fail == False and isAbroad == False:
        current_temp = soup.find('span', {'class': 'todaytemp'}).text
        cast_text = soup.find('p', 'cast_txt').text
        feel_like_temp = soup.select('.sensible > em > .num')[0].text
        print('현재 온도 : '+current_temp+'℃')
        weather_dic['현재 온도'] = current_temp+'℃'
        print(cast_text)
        weather_dic['비고'] = cast_text
        print('체감온도 : ' + feel_like_temp + '℃')
        weather_dic['체감온도'] = feel_like_temp + '℃'
        print(min_max_temp)
        weather_dic['최저기온'] = min_temp
        weather_dic['최고기온'] = max_temp

        try:
            uv_index = soup.select('.indicator > span > .num')
            uv_index_info = soup.find(
                'span', 'indicator').find('span').text[1:]
            print('자외선 : ' + uv_index[0].text + ' ' + uv_index_info)
            weather_dic['자외선'] = uv_index[0].text + ' ' + uv_index_info
        except:
            rainfall = soup.select('.rainfall > em')[0].text[0:1]
            print('시간당 강수량 : ' + rainfall + ' mm')
            weather_dic['시간당 강수량'] = rainfall + ' mm'

        try:
            data = soup.find('div', 'detail_box')
            fine_dust = data.find_all('dd')[0].text
            ultra_fine_dust = data.find_all('dd')[1].text
            ozone = data.find_all('dd')[2].text
            dust_info = '미세먼지 : '+str(fine_dust)+'\n' + '초미세먼지 : ' + \
                str(ultra_fine_dust)+'\n' + '오존지수 : ' + str(ozone)
            print(dust_info)
            weather_dic['미세먼지'] = str(fine_dust)
            weather_dic['초미세먼지'] = str(ultra_fine_dust)
            weather_dic['오존지수'] = str(ozone)
        except:
            print('no fine dust info exist')

    global weather_dic_combined
    weather_dic_combined.update(weather_dic)


def tmr_weather():
    print('내일 오전 :' + str(tmr_morning[0].text) + '℃' + ' ' +
          str(tmr_info[1].text) + '\n' + '미세먼지 : ' + tmr_indicator[0].text)
    print('내일 오후 :' + str(tmr_morning[1].text) + '℃' + ' ' +
          str(tmr_info[2].text) + '\n' + '미세먼지 : ' + tmr_indicator[1].text)

    weather_dic = {}
    weather_dic['내일 오전'] = str(tmr_morning[0].text) + \
        '℃' + ' ' + str(tmr_info[1].text)
    weather_dic['내일 오전 미세먼지'] = tmr_indicator[0].text
    weather_dic['내일 오후'] = str(tmr_morning[1].text) + \
        '℃' + ' ' + str(tmr_info[2].text)
    weather_dic['내일 오후 미세먼지'] = tmr_indicator[1].text

    global weather_dic_combined
    weather_dic_combined.update(weather_dic)


def abroad_tmr_weather():
    print('내일 오전 :' + str(tmr_morning[0].text) + '℃' + ' ' +
          str(tmr_info[1].text) + '\n' + '강수확률 : ' + tmr_indicator[1].text + '\n' + '바람 : ' + tmr_indicator[3].text)
    print('내일 오후 :' + str(tmr_morning[1].text) + '℃' + ' ' +
          str(tmr_info[2].text) + '\n' + '강수확률 : ' + tmr_indicator[5].text + '\n' + '바람 : ' + tmr_indicator[7].text)

    weather_dic = {}
    weather_dic['내일 오전'] = str(tmr_morning[0].text) + \
        '℃' + ' ' + str(tmr_info[1].text)
    weather_dic['내일 오전 강수확률'] = tmr_indicator[1].text
    weather_dic['내일 오전 바람'] = tmr_indicator[3].text
    weather_dic['내일 오후'] = str(tmr_morning[1].text) + \
        '℃' + ' ' + str(tmr_info[2].text)
    weather_dic['내일 오후 강수확률'] = tmr_indicator[5].text
    weather_dic['내일 오후 바람'] = tmr_indicator[7].text

    global weather_dic_combined
    weather_dic_combined.update(weather_dic)


def the_day_after_tmr():
    print('모레 오전 :' + str(tmr_morning[2].text) + '℃' + ' ' +
          str(tmr_info[3].text) + '\n' + '미세먼지 : ' + tmr_indicator[2].text)
    print('모레 오후 :' + str(tmr_morning[3].text) + '℃' + ' ' +
          str(tmr_info[4].text) + '\n' + '미세먼지 : ' + tmr_indicator[3].text)

    weather_dic = {}
    weather_dic['모레 오전'] = str(tmr_morning[2].text) + \
        '℃' + ' ' + str(tmr_info[3].text)
    weather_dic['모레 오전 미세먼지'] = tmr_indicator[2].text
    weather_dic['모레 오후'] = str(tmr_morning[3].text) + \
        '℃' + ' ' + str(tmr_info[4].text)
    weather_dic['모레 오후 미세먼지'] = tmr_indicator[3].text

    global weather_dic_combined
    weather_dic_combined.update(weather_dic)


def ask_save():
    global weather_dic_combined
    wanna_save = input('위의 데이터를 저장하시겠습니까? y/n : ')
    if wanna_save == 'y':
        with open('weather.csv', 'a') as f:
            w = csv.writer(f)
            w.writerow(weather_dic_combined.keys())
            w.writerow(weather_dic_combined.values())
            # for k, v in weather_dic_combined.items():
            # w.writerow([k, v])
        print('saved')

    weather_dic_combined.clear()


def ask_keep_going():
    keep_going = input('계속 하시겠습니까? y/n : ')
    if keep_going == 'n':
        return True
    else:
        return False

# def save_csv():


while True:
    where = input('어디 날씨를 알아볼까요? ex) 국가/도시/구/동/면/읍/동 : ')
    html = requests.get(
        'https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query='+where+' 날씨')
    soup = bs(html.text, 'html.parser')

    tmr_morning = soup.select('.morning_box > .info_temperature > .todaytemp ')
    tmr_info = soup.find_all('p', 'cast_txt')
    tmr_indicator = soup.select('.detail_box > .indicator > span')
    if today_weather():
        continue
    answer = input('내일 날씨도 불러올까요? (y/n) : ')
    if answer == 'y' and isAbroad == True:
        abroad_tmr_weather()
        ask_save()
        if ask_keep_going():
            break
    elif answer == 'y' and isAbroad == False:
        tmr_weather()
        ask_the_day_after_tmr = input('모레 날씨도 불러올까요? (y/n) : ')
        if ask_the_day_after_tmr == 'y':
            the_day_after_tmr()
            ask_save()
            if ask_keep_going():
                break
        else:
            ask_save()
            if ask_keep_going():
                break
    else:
        ask_save()
        if ask_keep_going():
            break

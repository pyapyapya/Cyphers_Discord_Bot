from bs4 import BeautifulSoup
import discord
import requests
import json
import random

header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
         '(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
client = discord.Client()


def find_profile(nickname):

    req = requests.get('http://cyphers.nexon.com/cyphers/game/record/search/1/' + nickname + '/1')
    html = req.content
    soup = BeautifulSoup(html, 'lxml')

    info1_head = soup.find('div', class_='info info1').find('thead').find_all('th')
    info1_body = soup.find('div', class_='info info1').find('tbody').find_all('td')

    write_profile = soup.find('div', class_='info info1').find('h2').text + '\n'
    name = info1_head[0].text.strip() + ' : ' + info1_body[0].text + '\n'
    grade = info1_head[1].text.strip() + ' : ' + info1_body[1].text + '\n'
    clan = info1_head[2].text.strip() + ' : ' + info1_body[2].text + '\n'

    result = write_profile + name + grade + clan
    return result


def find_ranking(nickname):

    req2 = requests.get('http://cyphers.nexon.com/cyphers/game/record/search/1/' + nickname + '/1')
    html = req2.content
    soup = BeautifulSoup(html, 'lxml')

    info2_head = soup.find('div', class_='info info2').find('thead').find_all('th')
    info2_body = soup.find('div', class_='info info2').find('tbody').find_all('td')
    write_record = soup.find('div', class_='info info2').find('h2').text + '\n'

    if len(info2_body) == 1:
        return write_record + info2_body[0].text

    elif len(info2_body) == 4:
        win = info2_head[0].text.strip() + ' : ' + info2_body[0].text + '\n'
        rp = info2_head[1].text.strip() + ' : ' + info2_body[1].text + '\n'
        top_rp = info2_head[2].text.strip() + ' : ' + info2_body[2].text + '\n'
        tier = info2_head[3].text.strip() + ' : ' + info2_body[3].text + '\n'
        result2 = write_record + win + rp + top_rp + tier
        return result2

    else:
        return '검색 결과가 없습니다.'


def ask_help():

    answer = '!전적 (닉네임), !ㅈㅈ (닉네임) : (닉네임)의 전적 및 rp를 출력합니다.\n ' \
             '!헬프, !도움, !help: 명령어의 이름과 기능을 설명합니다. \n'\
             '!템셋팅 (캐릭터), !템세팅 (캐릭터), !ㅌㅅㅌ : 조커등급 유저들의 아이템 셋팅을 알 수 있습니다. \n'\
             '!랜덤, !ㄹㄷ : 랜덤한 캐릭터 하나를 추천합니다. \n'\
             '!승률, !ㅅㄹ : 조커등급 유저들의 캐릭터 TOP3의 캐릭터 승률을 알 수 있습니다.'
    return answer


url_json = 'http://cyphers.nexon.com/cyphers/game/stat/charac/item/list.json'
url_bs4 = 'http://cyphers.nexon.com/cyphers/game/stat/charac/item'


req = requests.get(url_bs4)
html = req.content
soup = BeautifulSoup(html, 'lxml')


def matching_character_name(charactor_name):

    char_kor_eng_map = {}
    for lst in soup.find('ul', class_='char_lst').find_all('li')[:-1]:
        char_href = lst.find('a', href=True)['href'][24:-2].replace("'", '').replace(' ', '')
        char_eng, char_kor = char_href.split(',')
        char_kor_eng_map[char_kor] = char_eng
    return char_kor_eng_map[charactor_name]


def character_item_ranking(nickname):

    parts_list = ['HAND', 'HEAD', 'CHEST', 'WAIST', 'LEG', 'FOOT', 'ITEM_RECOVERY', 'ITEM_MOVE', 'ITEM_ATTACK',
        'ITEM_DEFENSE', 'ITEM_SPECIAL', 'NECK', 'ACCESSORY_1', 'ACCESSORY_2', 'ACCESSORY_3', 'ACCESSORY_4']
    item_name = []
    rate = []

    char_eng = matching_character_name(nickname)
    for lst in parts_list:
        data = {
            'dayType': 'WEEK',
            'grade': 'JOKER',
            'characName': char_eng,
            'partsName': lst
        }
        resp = requests.post(url_json, data=data)
        resp_json = json.loads(resp.text)
        for idx, content in enumerate(resp_json['searchList']):
            eqPartsRate = content['eqPartsRate']
            eqPartsRate = int(eqPartsRate)
            itemName = content['itemName']
            if (eqPartsRate >= 50):
                item_name.append(str(itemName))
                rate.append(str(eqPartsRate))
    return item_name, rate


def random_pick():
    character_list = ['로라스', '휴톤', '루이스', '타라', '트리비아', '카인', '레나', '드렉슬러', '도일', '토마스', '나이오비'
                      , '시바', '스텔라', '앨리셔', '클레어', '다이무스', '이글', '마를렌', '샬럿','윌라드', '레이튼',
                      '미쉘', '린', '빅터', '웨슬리', '카를로스', '호타루', '트릭시', '히카르도', '까미유', '자네트', '피터',
                      '아이작', '레베카', '엘리', '마틴', '브루스', '미아', '드니스', '제레온', '루시', '티엔', '하랑', '제이'
                      , '벨져', '리첼', '리사', '릭', '제키엘', '탄야', '캐럴', '라이센더', '루드빅', '멜빈', '디아나',
                      '클리브', '헬레나', '에바', '론', '레오노르', '시드니', '테이', '티모시']

    rand_num = random.randint(0, 63)
    return character_list[rand_num]


def character_win_rate(message):
    url_json = 'http://cyphers.nexon.com/cyphers/game/stat/charac/winrate/list.json'

    data = {
        'dayType': 'WEEK',
        'grade': 'JOKER',
        'selecType': 'SELEC_ALL',
        'totalCntType': 'LEVEL_1'
    }
    resp = requests.post(url_json, data=data)
    resp_load = json.loads(resp.text)
    character_name = []
    win_rate = []
    for i in range(3):
        character_name.append((resp_load['searchList'][i]['chName']))
        win_rate.append(str(round(resp_load['searchList'][i]['winrate'])))
    return character_name, win_rate

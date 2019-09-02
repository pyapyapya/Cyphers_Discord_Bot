import requests
import json
import datetime
from bs4 import BeautifulSoup
from urllib import parse
from urllib import request


# 01. 플레이어 검색
# nickname: URL encoding 필요
# wordType: match->동일한 닉네임 full->글자를 포함한 모든 닉네임의 유저
# limit: 반환 row의 수
def search_player():
    nickname = input()
    nickname = parse.quote(nickname.encode('utf-8'))
    req = requests.get('https://api.neople.co.kr/cy/players?nickname=' + nickname +'&wordType=rating&apikey=YDMj0zBFAmlexrJSzvIIQh6GlwNR0Ec5')
    html = req.content
    soup = BeautifulSoup(html, 'lxml').text
    playerid, nickname, grade = soup.split(",")
    playerid = playerid[22:-1]
    # print(soup)
    # print(playerid[22:-1])
    # print(nickname)
    # print(grade[:-3])
    return playerid


# 02. 플레이어 '정보' 조회

def player_information_search(input_playerid):
    json_url = 'https://api.neople.co.kr/cy/players/'+input_playerid+'?apikey=YDMj0zBFAmlexrJSzvIIQh6GlwNR0Ec5'
    data = request.urlopen(json_url)
    resq_data = json.loads(data.read())
    # print(resq_data)
    print('아이디 : ', resq_data['playerId'])
    print('급수:', resq_data['grade'])
    print('클랜이름: ', resq_data['clanName'])
    print('RP: ', resq_data['ratingPoint'])
    print('최고 RP: ', resq_data['maxRatingPoint'])
    print('티어: ', resq_data['tierName'])
    #
    # print(resq_data['records'][0])
    # print(resq_data['records'][1])
    #
    print('공식전: ' + resq_data['records'][0]['gameTypeId'])
    print('승', resq_data['records'][0]['winCount'])
    print('패', resq_data['records'][0]['loseCount'])
    print('중단', resq_data['records'][0]['stopCount'])

    print('일반전: ' + resq_data['records'][1]['gameTypeId'])
    print('승', resq_data['records'][1]['winCount'])
    print('패', resq_data['records'][1]['loseCount'])
    print('중단', resq_data['records'][1]['stopCount'])


# 03. 플레이어 '매칭 기록' 조회
def player_matching_record_search(input_playerid):
    now = datetime.datetime.now()
    this_time = now.strftime('%Y-%m-%d')
    # old_time = this_time.replace(day=12)
    json_url = 'https://api.neople.co.kr/cy/players/'+input_playerid+''\
                '/matches?gameTypeId=rating&startDate=20190701T0000&endDate=201907016T0000&limit=5&next=<next>' \
                                                                     '&apikey=YDMj0zBFAmlexrJSzvIIQh6GlwNR0Ec5'
    # json_url = 'https://api.neople.co.kr/cy/players/' + input_playerid + '' \
    #             '/matches?gameTypeId=rating&startDate='+this_time+'&endDate='+this_time+'&limit=5&next=<next>' \
    #                                                                      '&apikey=YDMj0zBFAmlexrJSzvIIQh6GlwNR0Ec5'
    data = request.urlopen(json_url)
    resq_json = json.loads(data.read())
    # print(resq_json)
    # print(resq_json['matches'])
    print(resq_json['matches'])


# 04. 매칭 상세 조회


# 05. 통합 랭킹 조회
# 기존에 있는 'playerid' 'nickname' 'ratingPoint' 'clanName'은 생략합니다.
def player_ranking_search(input_playerid):
    json_url = 'https://api.neople.co.kr/cy/ranking/ratingpoint?playerId=36cab6354d1758c1d02c389ea948f099&' \
               'offset=<offset>&limit=<limit>&apikey=YDMj0zBFAmlexrJSzvIIQh6GlwNR0Ec5'
    data = request.urlopen(json_url)
    resq_json = json.loads(data.read())
    rank = resq_json['rows'][0]['rank']
    # print(resq_json['rows'][0]['rank'])
    return rank


# 06. 아이템 검색
def item_search():
    item_name = input()
    item_name = parse.quote(item_name.encode('utf-8'))
    json_url = 'https://api.neople.co.kr/cy/battleitems?itemName='+item_name + \
               '&wordType=<wordType>&limit=<limit>&q=characterId:<characterId>;slotCode:<slotCode>,' \
               'rarityCode:<rarityCode>,seasonCode:<seasonCode>&apikey=YDMj0zBFAmlexrJSzvIIQh6GlwNR0Ec5'
    data = request.urlopen(json_url)
    resq_json = json.loads(data.read())
    # print(resq_json)
    print(resq_json['rows'][0]['itemId'])
    print(resq_json['rows'][0]['itemName'])
    print(resq_json['rows'][0]['characterName'])
    print(resq_json['rows'][0]['slotName'])
    print(resq_json['rows'][0]['seasonName'])
    print(resq_json['rows'][0]['itemId'])
    return resq_json['rows'][0]['itemId']


# 07. 아이템 검색
def item_inquire(input_item_name):
    image_url = 'https://img-api.neople.co.kr/cy/items/'+input_item_name
    file = request.urlopen(image_url).read()
    with open(input_item_name+'.png', mode='wb') as f:
        f.write(file)
        print('finish')
    json_url = 'https://api.neople.co.kr/cy/battleitems/'+input_item_name+'?apikey=YDMj0zBFAmlexrJSzvIIQh6GlwNR0Ec5'
    data = request.urlopen(json_url)
    resq_json = json.loads(data.read())
    print(resq_json)
    return resq_json['characterId']


# playerid = search_player()
# player_information_search(playerid)
# player_matching_record_search(playerid)
# player_ranking_search(playerid)

# 08. 캐릭터 정보
# 아이템 검색에서 나온 characterId를 사용
item_name = item_search()
character_id = item_inquire(item_name)


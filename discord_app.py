import discord
import asyncio
import os
from Methods import find_profile
from Methods import find_ranking
from Methods import ask_help
from Methods import character_item_ranking
from Methods import random_pick
from Methods import character_win_rate

path = os.getcwd()
f = open('./token.txt')
token = f.readline()
f.close()

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    ask_help()


@client.event
async def on_message(message):
    if __name__ == '__main__':
        if message.content.startswith('!sleep'):
            await asyncio.sleep(5)
            await client.send_message(message.channel, 'Done sleeping')

        elif message.content.startswith('!전적') or message.content.startswith('!ㅈㅈ'):
            nickname = message.content[3:]
            get_profile = find_profile(nickname)
            get_ranking = find_ranking(nickname)
            await client.send_message(message.channel, get_profile)
            await client.send_message(message.channel, get_ranking)

        elif message.content.startswith('!help') or message.content.startswith('!도움') or \
                message.content.startswith('!헬프'):
            answer = ask_help()
            await client.send_message(message.channel, answer)

        elif message.content.startswith('!템셋팅') or message.content.startswith('!템세팅') or \
            message.content.startswith('!ㅌㅅㅌ'):
            character_Name = message.content[5:]
            await client.send_message(message.channel, "1주일간 조커등급의 아이템 부위별 장착율 1위입니다.")
            item_rate, rate = character_item_ranking(character_Name)
            for i in range(len(item_rate)):
                await client.send_message(message.channel, item_rate[i] + " " + rate[i] + "%")

        elif message.content.startswith('!랜덤') or message.content.startswith('!ㄹㄷ'):
            select = random_pick()
            await client.send_message(message.channel, "이 캐릭터는 어떠세요?")
            await client.send_message(message.channel, select)

        elif message.content.startswith('!승률') or message.content.startswith('!ㅅㄹ'):
            character_name, win_rate = character_win_rate(message)
            await client.send_message(message.channel, "1주일간 조커등급의 캐릭터 승률 TOP3 캐릭터입니다.")
            for i in range(3):
                await client.send_message(message.channel, character_name[i] + " " + win_rate[i] + "%")

client.run(token)

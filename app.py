#!/usr/bin/python3
import discord
import asyncio
import logging
import os
import random
from random import randint
import datetime
from datetime import date
import time
import psutil

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='log.txt', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#Strings
bot_ver = '1.5.6'

#해당 기능은 봇 재부팅 시 재설정이 필요함
doing = ""
doing_enabled = 0

def checkIfProcessRunning(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

client = discord.Client()

@client.event
async def on_ready():
    print('name : ' + client.user.name)
    print('id   : ' + client.user.id)
    await client.change_presence(game=discord.Game(name='#기계식루냥이_사용법 ㄱ | ' + bot_ver))

@client.event
async def on_message(message):
    global doing_enabled
    global doing
    if message.content.startswith('루냥아 도와줘'):
        await client.send_message(message.channel, "#기계식루냥이_사용법 ㄱ")
    elif message.content.startswith('루냥이 따먹을래'):
        await client.send_message(message.channel, "루따먹 씹가능 ㅗㅜㅑ")
    elif message.content.startswith('루냥이 섹스하자'):
        await client.send_message(message.channel, "꼬추 존나작네 안함 ㅅㄱㄹ")
    elif message.content.startswith('luna admin execute '):
        if message.author.id =='(Owner ID here)':
            shl_str = message.content
            shl_str = shl_str.replace('luna admin execute ','')
            await client.send_message(message.channel, "```" + str(os.popen(shl_str).read()) + "```")
        else:
            await client.send_message(message.channel, ":thinking:")
    elif message.content.startswith('luna admin presence change '):
        if message.author.id =='(Owner ID here)':
            doing_enabled = 1
            doing_sanitize = message.content
            doing_sanitize = doing_sanitize.replace('luna admin presence change ', '')
            doing = doing_sanitize
            await client.send_message(message.channel, ":ok_hand:")
        else:
            await client.send_message(message.channel, ":thinking:")
    elif message.content.startswith('luna admin presence disable'):
        if message.author.id =='(Owner ID here)':
            doing_enabled = 0
            await client.send_message(message.channel, ":ok_hand:")
        else:
            await client.send_message(message.channel, ":thinking:")
    elif message.content.startswith('루냥아 무슨담배 피니'):
        await client.send_message(message.channel, "에쎄 체인지 업\n인데요 갈수록 맛대가리가 병신되어가고있네여 비추천")
    elif message.content.startswith('루냥아 무슨맥주 좋아하니'):
        await client.send_message(message.channel, "버지 미스터")
    elif message.content.startswith('루냥아 뭐하니'):
        global doing_enabled
        global doing
        now = datetime.datetime.now()
        lw_h = now.hour
        lw_w = date.isoweekday(date.today())
        if lw_w == 1: #월요일
            if lw_h >= 3 and lw_h <= 10:
                lw_string = "자고있음"
            elif lw_h >= 13 and lw_h <= 17:
                lw_string = "무인항공기운영실습 강의시간임"
            elif lw_h >= 18 and lw_h <= 20:
                lw_string = "근무중임 방해ㄴㄴ"
            else:
                lw_string = "한가하거나 이지투하고있거나 둘중하나임"
        elif lw_w == 2: #화요일
            if lw_h >= 2 and lw_h <= 7:
                lw_string = "자고있음"
            elif lw_h >= 9 and lw_h <= 12:
                lw_string = "항공전기전자 강의시간임"
            elif lw_h == 13:
                lw_string = "학식먹는중"
            else:
                lw_string = "한가함 어쨌든 한가함"
        elif lw_w == 3: #수요일
            if lw_h >= 3 and lw_h <= 11:
                lw_string = "자고있음"
            elif lw_h >= 14 and lw_h <= 16:
                lw_string = "항공역학 강의시간임"
            elif lw_h == 17 or lw_h == 18:
                lw_string = "근무중임 방해ㄴㄴ"
            else:
                lw_string = "지금 얘기하면 받아줄거같음"
        elif lw_w == 4: #목요일
            if lw_h >= 2 and lw_h <= 11:
                lw_string = "자고있음"
            else:
                lw_string = "우주공강임 개꿀"
        elif lw_w == 5: #금요일
            if lw_h >= 2 and lw_h <= 10:
                lw_string = "자고있음"
            elif lw_h >= 11 and lw_h <= 14:
                lw_string = "항공기상 강의시간임"
            elif lw_h == 16 and lw_h == 17:
                lw_string = "근무시간임 방해ㄴㄴ"
            else:
                lw_string = "존나즐거움 메챠쿠챠 타노시쟝"
        else: #주말
            lw_string = "니가 물어보셈"
        if doing_enabled == 1:
            lw_string = doing
        await client.send_message(message.channel, lw_string)
    elif message.content.startswith('루냥이 실력 어느정도니'):
        lg_string = ["옵치 딜힐위주 골드정도",
                     "이지투 5키온리 14 조무사",
                     "이지투 5키스탠 쌍오토걸고 15 조무사",
                     "펌프 DR걸고 11렙 깸",
                     "테트리스 쌉고수임",
                     "사볼안해요 꺼지셈"]
        await client.send_message(message.channel, random.choice(lg_string) + "\n떡치기 실력을 기대하셨습니까? 그런거 없습니다 ㅅㄱ")
    elif message.content.startswith('루냥아 배고파'):
        lf_string = ["메가맥 세트에서 야채 다 빼고 ㄱ",
                     "이마트24 가서 속풀라면 ㄱ",
                     "고씨네 가서 소고기카레 1고 ㄱ",
                     "단지네 가서 콩나물국밥 ㄱ",
                     "맘스터치 치킨 좋음",
                     "김치킨 짜긴한데 맛있음",
                     "지정환피자 크런치골드 라지 ㄹㅇ 갓피자임",
                     "BBQ 황금올리브 ㄹㅇ 갓치킨임 꼭먹으셈",
                     "상문이두마리 간장치킨 ㄱ 교촌보다는 **싸서** 맛있음",
                     "옛날통닭 맛있음 개추",
                     "이마트 치킨 맛있는데 왜 아무도 관심을 안주죠",
                     "교촌 간장치킨 비싼데 맛있음 ㅇㅇ",
                     "굽네 볼케이노 개맛있음",
                     "저 갱상도 새럼이라서 냉면에다 식초랑 겨자 오지게 많이넣음",
                     "이마트 피코크 군만두 개맛있는데 왜 아무도 안사죠",
                     "배고프면 뭘 먹어도 맛있음 ㅇㅇ"]
        await client.send_message(message.channel, random.choice(lf_string))
    elif message.content.startswith('루냥이 귀여워'):
        if message.author.id =='(Owner ID here)':
            await client.send_message(message.channel, '**process check**\n444d : ' + str(checkIfProcessRunning('444d.sh')) + '\nhauzen : ' + str(checkIfProcessRunning('444d2.sh')))
        else:
            lc_string = ["그쵸 루냥이 진짜 너무 귀여워요 ㅠㅜ",
                         "아웅 루냥이 너무 큐트뽀쟉해 지구뿌셔ㅠㅠㅜ",
                         "저 루냥이 꼬리 잡아당겨본 적 있는데 그때 진짜 심장멎을뻔했어요ㅠㅠ:heart_eyes:",
                         "루냥이 쓰다듬다가 좋아하는 표정 보고 심쿵:heart_eyes: 골골송 하는것도 너무 큐트해ㅠㅜ",
                         "아웅 어뜩행 ㅠㅜ 너무 귀여워 ㅠㅜ",
                         "루냥이 너무 귀여워! :heart_eyes:"]
            await client.send_message(message.channel, random.choice(lc_string))

client.run('?_?')

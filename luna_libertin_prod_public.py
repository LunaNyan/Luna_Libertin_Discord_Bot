#!/usr/bin/python3

import sys

if sys.version_info[0] != 3 or sys.version_info[1] < 5:
    print("This script requires Python version 3.5")
    sys.exit()

import re, traceback, discord, datetime, asyncio, os, random, configparser, m_food
from m_seotda import *
from m_wolframalpha import wa_calc, wa_img
from m_etc import *

#imoort logging
#logger = logging.getLogger('discord')
#logger.setLevel(logging.DEBUG)
#handler = logging.FileHandler(filename='log.txt', encoding='utf-8', mode='w')
#handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#logger.addHandler(handler)

bot_ver = "1.9.5m"

db_path = "luna_config.txt"

db = configparser.ConfigParser()
db.read(db_path)
print("successfully loaded configuration file. connecting to Discord server. please wait.")

test_glyph = ""
if db.get("config", "IsThisBotTesting") == "1":
    test_glyph = "_"
    print("This bot is in test range. you must insert '_' before command.")
else:
    print("This bot is not in test range.")

client = discord.Client()

@client.event
async def bgjob_change_playing():
    while True:
        members_sum = 0
        for s in client.servers:
            members_sum += len(s.members)
        await asyncio.sleep(10)
        await client.change_presence(game=discord.Game(name='루냥아 도와줘 → 도움말'))
        await asyncio.sleep(10)
        await client.change_presence(game=discord.Game(name=str(len(client.servers)) +'개의 서버에서 귀여움받는 중'))
        await asyncio.sleep(10)
        await client.change_presence(game=discord.Game(name=str(members_sum) + '명의 유저들에게 귀여움받는 중'))
        await asyncio.sleep(10)
        await client.change_presence(game=discord.Game(name='v' + bot_ver))
        await asyncio.sleep(10)
        await client.change_presence(game=discord.Game(name='루냥아 업데이트내역 → 업데이트 내역 보기'))
        await asyncio.sleep(10)
        await client.change_presence(game=discord.Game(name='이 메시지는 10초 마다 바뀌어요!'))

@client.event
async def on_ready():
    print('Bot is ready to use.')
    print('name    : ' + str(client.user.name))
    print('id      : ' + str(client.user.id))
    print('version : ' + bot_ver)
    client.loop.create_task(bgjob_change_playing())

@client.event
async def on_message(message):
    global test_glyph
    if message.author == client.user:
        return
    elif message.author.bot:
        return
    if message.content.startswith(test_glyph + '루냥아 도와줘'):
        a = message.content
        a = a.replace('루냥아 도와줘', '')
        if a == '':
            embed=discord.Embed(title="기계식 루냥이를 초대해주셔서 감사합니다!", description="[민원창구](https://discordapp.com/invite/yyS9x5V) [봇 초대하기](https://discordapp.com/oauth2/authorize?client_id=598080777565241354&scope=bot&permissions=388160)", color=0xff0080)
            embed.set_author(name="기계식 루냥이 사용 방법",icon_url=client.user.avatar_url)
            embed.add_field(name="도움말", value="루냥아 도와줘 (항목), 루냥아 업데이트내역", inline=False)
            embed.add_field(name="일상", value="루냥아 배고파, 루냥이 귀여워, 루냥이 쓰담쓰담, 루냥아 짖어봐, 루냥아 손, 루냥아 주사위, 와! 샌즈!", inline=False)
            embed.add_field(name="게임", value="루냥아 섯다", inline=False)
            embed.add_field(name="유용한 기능", value="루냥아 계산해줘 (계산식), 루냥아 계산해줘 이미지 (계산식), 루냥아 확성기, 루냥아 골라줘", inline=False)
            embed.set_footer(text="Copyright (C) 2017 - 2019 libertin | v" + bot_ver)
        elif a == ' 일상':
            embed=discord.Embed(title="도움말", description="일상 항목", color=0x8080ff)
            embed.add_field(name="루냥아 배고파", value="랜덤으로 음식을 추천해줍니다 (음식을 사주지는 않습니다!)", inline=False)
            embed.add_field(name="루냥이 귀여워", value="자기 자신을 귀여워합니다 (루냥이 커여워, 귀냥이 루여워, 커냥이 루여워 도 가능합니다)", inline=False)
            embed.add_field(name="루냥이 쓰담쓰담", value="자기 자신한테 사이버(?) 쓰다듬을 선물해줍니다", inline=False)
            embed.add_field(name="루냥아 짖어봐", value="멍", inline=False)
            embed.add_field(name="루냥아 손", value=":raised_hand:", inline=False)
            embed.add_field(name="와! 샌즈!", value="언더테일 아시는구나!", inline=False)
        elif a == ' 게임':
            embed=discord.Embed(title="도움말", description="게임", color=0xffff00)
            embed.set_author(name="게임 사용 방법 보기 : 루냥아 도와줘 게임 (게임이름)")
            embed.add_field(name="섯다", value="CPU와 두장섯다를 진행합니다", inline=False)
            embed.add_field(name="제비뽑기", value="CPU가 제비뽑기를 실행합니다", inline=False)
            embed.add_field(name="루냥아 주사위", value="1부터 6까지 무작위의 숫자를 출력합니다", inline=False)
        elif a == ' 게임 섯다':
            embed=discord.Embed(title="두장섯다 사용 방법", description="명령어 : 루냥아 섯다 (숫자1) (숫자2), 0~9까지의 숫자 두개를 입력해 진행합니다", color=0xffff00)
            embed.add_field(name="족보 순위", value="땡 > 삥 > 끗", inline=False)
            embed.add_field(name="땡", value="두 패가 같은 경우 (장땡 ~ 삥땡)", inline=False)
            embed.add_field(name="삥", value="알리(1+2), 독사(1+4), 구삥(1+9), 장삥(1+10), 장사(4+10), 세륙(4+6)", inline=False)
            embed.add_field(name="끗", value="두 패 합의 일의 자리 숫자 (갑오 ~ 망통)", inline=False)
        elif a == ' 게임 제비뽑기':
            embed=discord.Embed(title="제비뽑기 사용 방법", description="명령어 : 루냥아 제비뽑기 (선택지1) (선택지2) ... , (결과1) (결과2) ...", color=0xffff00)
            embed.add_field(name="사용 방법", value="각 항목은 띄어쓰기로 구분, 선택지와 결과는 쉼표(,)로 구분!", inline=False)
            embed.add_field(name="주의사항", value="선택지와 결과의 개수는 동일해야 합니다", inline=True)
        elif a == ' 게임 주사위':
            embed=discord.Embed(title="주사위 사용 방법", description="명령어 : 루냥아 주사위", color=0xffff00)
        elif a == ' 유용한 기능':
            embed=discord.Embed(title="도움말", description="유용한 기능", color=0x00ff00)
            embed.add_field(name="루냥아 계산해줘 (계산식)", value="Wolfram|Alpha 계산 쿼리를 제공합니다", inline=False)
            embed.add_field(name="루냥아 계산해줘 이미지 (계산식)", value="Wolfram|Alpha 플롯 계산 쿼리를 제공합니다(실험적인 기능입니다!)", inline=False)
            embed.add_field(name="루냥아 골라줘 (선택지1) (선택지2) ...", value="어느것을 고를까요 알아맞춰 봅시다", inline=False)
            embed.add_field(name="루냥아 확성기 (할 말)", value="루냥이가 대신 말해줍니다 (혐오 단어가 감지되는 경우 거부됩니다)", inline=False)
        else:
            embed=discord.Embed(title='전체 도움말을 원하신다면 그냥 "루냥아 도와줘"라고만 입력해주세요!')
        await client.send_message(message.channel, embed=embed)
    elif message.content == test_glyph + '루냥아 업데이트내역':
        await client.send_message(message.channel, ret_changelog())
    elif message.content == test_glyph + '루냥아 배고파':
        await client.send_message(message.channel, m_food.return_food())
    elif message.content == test_glyph + '루냥이 귀여워' or message.content == test_glyph + '루냥이 커여워' or message.content == test_glyph + '귀냥이 루여워' or message.content == test_glyph + '커냥이 루여워':
        await client.send_message(message.channel, imcute())
    elif message.content == test_glyph + '와! 샌즈!':
        await client.send_message(message.channel, sans())
    elif message.content == test_glyph + '루냥이 쓰담쓰담':
        await client.send_message(message.channel, pat())
    elif message.content.startswith(test_glyph + '루냥아 섯다 '):
        result = seotda_init(message.content)
        if result == "e_duplicated":
            await client.send_message(message.channel, ":thinking: 같은 카드를 중복해서 고를 수 없습니다")
        elif result == "e_outofrange":
            await client.send_message(message.channel, ":thinking: 0에서 9까지의 숫자를 입력해주세요")
        elif result == "e_value":
            await client.send_message(message.channel, ":thinking: 잘못된 입력입니다")
        else:
            result_player = ret_player()
            result_cpu = ret_cpu()
            await client.send_message(message.channel, ret_player_selection() + " (" + ret_player_card() + ")을 골랐습니다\n상대방 패 : " + ret_cpu_selection() + " (" + ret_cpu_card() + ")\n" + result_player + " VS " + result_cpu + " : **" + result + "**\n" + ret_deck())
    elif message.content.startswith(test_glyph + '루냥아 확성기 '):
        if re.search(db.get("string", "hatespeech"), message.content):
            await client.delete_message(message)
            await client.send_message(message.channel, "사용 금지된 단어가 포함되어 있습니다")
        else:
            say_str = message.content
            say_str = say_str.replace(test_glyph + '루냥아 확성기 ','')
            await client.delete_message(message)
            await client.send_message(message.channel, say_str)
    elif message.content.startswith(test_glyph + "루냥아 계산해줘 이미지 "):
        message_temp = await client.send_message(message.channel, "잠시만 기다려주세요!")
        bci_str = message.content
        bci_str = bci_str.replace(test_glyph + "루냥아 계산해줘 이미지 ", "")
        await client.send_file(message.channel, wa_img(bci_str))
        await client.delete_message(message_temp)
    elif message.content.startswith(test_glyph + "루냥아 계산해줘 "):
        try:
            bc_str = message.content
            bc_str = bc_str.replace(test_glyph + "루냥아 계산해줘 ","")
            if bc_str == "":
                await client.send_message(message.channel, "연산식을 입력해주세요")
            elif bc_str == "1+1":
                await client.send_message(message.channel, "귀요미! 난 귀요미! :two_hearts:")
            else:
                bc_tmp = await client.send_message(message.channel, "잠시만 기다려주세요!")
                await client.send_message(message.channel, wa_calc(bc_str))
                await client.delete_message(bc_tmp)
        except:
            await client.send_message(message.channel, "연산식을 다시 확인해주세요")
    elif message.content.startswith(test_glyph + '루냥아 골라줘 '):
        await client.send_message(message.channel, "**" + selectr(message.content) + "**(이)가 선택되었습니다")
    elif message.content == test_glyph + '루냥아':
        await client.send_message(message.channel, l_ping())
    elif message.content == test_glyph + '루냥아 짖어봐':
        await client.send_message(message.channel, l_dog())
    elif message.content == test_glyph + '루냥아 손':
        await client.send_message(message.channel, ':raised_hand:')
    elif message.content == test_glyph + '루냥아 주사위':
        await client.send_message(message.channel, '(쫑긋) (데구르르) ' + l_dice() + '!')
    elif message.content.startswith(test_glyph + '루냥아 제비뽑기 '):
        await client.send_message(message.channel, l_ticket(message.content))
    elif message.content == test_glyph + '루냥아 자가진단':
        permcheck_message_manage = ":green_heart: 정상"
        permcheck_links = ":green_heart: 정상"
        try:
            embed=discord.Embed(title='test')
            permcheck_link_test = await client.send_message(message.channel, embed=embed)
        except:
            permcheck_links = ":broken_heart: 오류"
        await client.delete_message(permcheck_link_test)
        try:
            await client.delete_message(message)
        except:
            permcheck_message_manage = ":broken_heart: 오류"
        await client.send_message(message.channel, "봇 권한 자가진단 결과\n봇 버전 : " + bot_ver + "\n메시지 읽기, 쓰기 : :green_heart: 정상\n링크 첨부 : " + permcheck_links + "\n메시지 관리 : " + permcheck_message_manage + "\n**봇 역할의 권한을 임의로 수정하지 마세요! 오류가 발생할 수 있습니다!**")
    elif message.content.startswith('루냥아 실행해줘 ') and message.author.id == '280306700324700160':
        if message.content == 'cputemp':
            await client.send_message(message.channel, str(os.popen('/opt/vc/bin/vcgencmd measure_temp').read()))
        else:
            shl_str = message.content
            shl_str = shl_str.replace('루냥아 실행해줘 ','')
            try:
                await client.send_message(message.channel, str(os.popen(shl_str).read()))
            except:
                await client.send_message(message.channel, ':facepalm:')
    with open(db_path, 'w') as configfile:
        db.write(configfile)

client.run(db.get("config", "bot_token"))

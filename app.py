#!/usr/bin/python3
import discord
import asyncio
import logging
import os
import random
import configparser

import m_etc, m_lifetime, m_food
from m_rps import rps_run
from m_seotda import *

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='log.txt', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot_ver = "1.7.2"

db_path = "luna_config.txt"

db = configparser.ConfigParser()
db.read(db_path)

#해당 기능은 봇 재부팅 시 재설정이 필요함
precense = ""

test_glyph = ""
if db.get("config", "IsThisBotTesting") == "1":
    test_glyph = "_"

client = discord.Client()

@client.event
async def on_ready():
    print('name : ' + client.user.name)
    print('id   : ' + client.user.id)
    await client.change_presence(game=discord.Game(name='#기계식루냥이_사용법 ㄱ | ' + bot_ver))

@client.event
async def on_message(message):
    global precense_enabled
    global precense
    global test_glyph
    if message.server.id == db.get("config", "server_id"):
        try:
            temp_point = int(db.get("user_point", str(message.author.id)))
            temp_point = temp_point + int(db.get("config", "point_increment"))
            db.set("user_point", str(message.author.id), str(temp_point))
        except:
            db.set("user_point", str(message.author.id), "0")
        if message.content.startswith(test_glyph + '루냥아 도와줘'):
            await client.send_message(message.channel, "#기계식루냥이_사용법 ㄱ")
        elif message.content.startswith(test_glyph + 'luna admin execute '):
            if message.author.id == str(db.get("config", "owner_id")):
                shl_str = message.content
                shl_str = shl_str.replace(test_glyph + 'luna admin execute ','')
                await client.send_message(message.channel, "```" + str(os.popen(shl_str).read()) + "```")
            else:
                await client.send_message(message.channel, ":thinking:")
        elif message.content.startswith(test_glyph + 'luna admin presence change '):
            if message.author.id == str(db.get("config", "onwer_id")):
                precense_sanitize = message.content
                precense_sanitize = precense_sanitize.replace(test_glyph + 'luna admin presence change ', '')
                precense = precense_sanitize
                await client.send_message(message.channel, ":ok_hand:")
            else:
                await client.send_message(message.channel, ":thinking:")
        elif message.content.startswith(test_glyph + 'luna admin presence disable'):
            if message.author.id == str(db.get("config", "owner_id")):
                precense = ""
                await client.send_message(message.channel, ":ok_hand:")
            else:
                await client.send_message(message.channel, ":thinking:")
        elif message.content.startswith(test_glyph + '루냥아 뭐하니'):
            await client.send_message(message.channel, return_lifetime(precense))
        elif message.content.startswith(test_glyph + '루냥이 실력 어느정도니'):
            lg_string = ["옵치 딜힐위주 골드정도",
                         "이지투 5키온리 14 조무사",
                         "이지투 5키스탠 쌍오토걸고 15 조무사",
                         "펌프 DR걸고 11렙 깸",
                         "테트리스 쌉고수임",
                         "사볼안해요 꺼지셈"]
            await client.send_message(message.channel, random.choice(lg_string) + "\n떡치기 실력을 기대하셨습니까? 그런거 없습니다 ㅅㄱ")
        elif message.content.startswith(test_glyph + '루냥아 배고파'):
            await client.send_message(message.channel, return_food())
        elif message.content.startswith(test_glyph + '루냥이 귀여워'):
            await client.send_message(message.channel, imcute())
        elif message.content.startswith(test_glyph + '루냥아 내포인트'):
            temp_point = db.get("user_point", str(message.author.id))
            await client.send_message(message.channel, str(temp_point) + " 점입니다")
        elif message.content.startswith(test_glyph + '와! 샌즈!'):
            await client.send_message(message.channel, sans())
        elif message.content.startswith(test_glyph + '루냥이 쓰담쓰담'):
            await client.send_message(message.channel, pat())
        elif message.content.startswith(test_glyph + '루냥아 가위바위보 '):
            await client.send_message(message.channel, rps_run(message.content))
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
                await client.send_message(message.channel, ret_player_selection() + " (" + ret_player_card() + ")을 골랐습니다")
                await client.send_message(message.channel, "상대방 패 : " + ret_cpu_selection() + " (" + ret_cpu_card() + ")")
                await client.send_message(message.channel, result_player + " VS " + result_cpu + " : **" + result + "**\n" + ret_deck())
        elif message.content.startswith(test_glyph + '루냥아 UUID'):
            await client.send_message(message.channel, str(os.popen("uuidgen -r").read()))
        elif message.content.startswith(test_glyph + '루냥아 현재시각'):
            await client.send_message(message.channel, str(os.popen("date -Iseconds").read()))
        with open(db_path, 'w') as configfile:
            db.write(configfile)
    else:
        await client.send_message(message.channel, "**STOP!**\n\nRunning this bot out of owner's server is prohibited.\n**PLEASE KICK ME.**\n\nIf you can understand what are you doing, you can pork my source repository!\nhttps://github.com/LunaNyan/Luna_Libertin_Discord_Bot")

client.run(db.get("config", "bot_token"))

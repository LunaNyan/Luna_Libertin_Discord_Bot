#!/usr/bin/python3
import re
import traceback
import discord
import asyncio
import logging
import os
import random
import configparser

import m_lifetime, m_food
from m_rps import rps_run
from m_seotda import *
from m_etc import *

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='log.txt', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot_ver = "1.7.3"

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
    if message.author == client.user:
        return
    if message.server.id == db.get("config", "server_id"):
        try:
            temp_point = int(db.get("user_point", str(message.author.id)))
            temp_point = temp_point + int(db.get("config", "point_increment"))
            db.set("user_point", str(message.author.id), str(temp_point))
        except:
            db.set("user_point", str(message.author.id), "0")
        hatespeech = re.compile('(메[0-9]*[갤갈]|[김씹]치[남녀]|한남충?|[남여]혐|워마드|빻[남녀]|피싸개|[빻애]니프사|피싸개|[트꼴]페미|재기|추하[네다죠]|[부통자]들[부통자]들|네덕|비틱|네다[찐씹]|[조좆]팔).*')
        hs_match = hatespeech.match(message.content)
        if hs_match:
            await client.send_message(discord.Object(id=db.get('config', 'alert_channel_id')), "possible hate speech found at " + message.channel.name + "\n" + message.author.display_name + " : " + message.content)
        if message.content.startswith(test_glyph + '루냥아 도와줘'):
            await client.send_message(message.channel, "#기계식루냥이_사용법 ㄱ")
        elif message.content.startswith(test_glyph + '루냥아 실행해줘 '):
            if message.author.id == str(db.get("config", "owner_id")):
                shl_str = message.content
                shl_str = shl_str.replace(test_glyph + '루냥아 실행해줘 ','')
                await client.send_message(message.channel, "```" + str(os.popen(shl_str).read()) + "```")
            else:
                await client.send_message(message.channel, ":thinking:")
        elif message.content.startswith(test_glyph + '루냥아 precense '):
            if message.author.id == str(db.get("config", "onwer_id")):
                precense_sanitize = message.content
                precense_sanitize = precense_sanitize.replace(test_glyph + '루냥아 precense ', '')
                precense = precense_sanitize
                await client.send_message(message.channel, ":ok_hand:")
            else:
                await client.send_message(message.channel, ":thinking:")
        elif message.content.startswith(test_glyph + '루냥아 presence --disable'):
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
        elif message.content.startswith(test_glyph + '루냥아 확성기 '):
            say_str = message.content
            say_str = say_str.replace(test_glyph + '루냥아 확성기 ','')
            say_mention = message.author.display_name
            say_channel = message.channel.name
            await client.delete_message(message)
            await client.send_message(message.channel, say_str)
            await client.send_message(discord.Object(id=db.get('config', 'log_channel_id')), "used sayd : " + say_mention + " : " + say_str + "\nat : " + say_channel)
        with open(db_path, 'w') as configfile:
            db.write(configfile)
    else:
        await client.send_message(message.channel, "**STOP!**\n\nRunning this bot out of owner's server is prohibited.\n**PLEASE KICK ME.**\n\nIf you can understand what are you doing, you can pork my source repository!\nhttps://github.com/LunaNyan/Luna_Libertin_Discord_Bot")

@client.event
async def on_message_delete(message):
    await client.send_message(discord.Object(id=db.get('config', 'log_channel_id')), "message removed from " + message.author.display_name + " at " + message.channel.name + "\n" + message.content)

@client.event
async def on_message_edit(before, after):
    await client.send_message(discord.Object(id=db.get('config', 'log_channel_id')), "message edited from " + before.author.display_name + " at " + before.channel.name + "\nbefore : " + before.content + "\nafter : " + after.content)

client.run(db.get("config", "bot_token"))

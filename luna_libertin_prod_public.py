#!/usr/bin/python3
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

bot_ver = "1.7.14m"

db_path = "luna_config.txt"

db = configparser.ConfigParser()
db.read(db_path)

test_glyph = ""
if db.get("config", "IsThisBotTesting") == "1":
    test_glyph = "_"

client = discord.Client()

@client.event
async def on_ready():
    print('name : ' + str(client.user.name))
    print('id   : ' + str(client.user.id))
    await client.change_presence(game=discord.Game(name='루냥아 도와줘 →  도움말 | v' + bot_ver))

@client.event
async def on_message(message):
    global test_glyph
    if message.author == client.user:
        return
    elif message.author.bot:
        return
    if message.content.startswith(test_glyph + '루냥아 도와줘'):
        await client.send_message(message.channel, ret_help())
    elif message.content.startswith(test_glyph + '루냥아 배고파'):
        await client.send_message(message.channel, m_food.return_food())
    elif message.content.startswith(test_glyph + '루냥이 귀여워') or message.content.startswith('루냥이 커여워') or message.content.startswith('귀냥이 루여워') or message.content.startswith('커냥이 루여워'):
        await client.send_message(message.channel, imcute())
    elif message.content.startswith(test_glyph + '와! 샌즈!'):
        await client.send_message(message.channel, sans())
    elif message.content.startswith(test_glyph + '루냥이 쓰담쓰담'):
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
            await client.send_message(message.channel, ret_player_selection() + " (" + ret_player_card() + ")을 골랐습니다")
            await client.send_message(message.channel, "상대방 패 : " + ret_cpu_selection() + " (" + ret_cpu_card() + ")")
            await client.send_message(message.channel, result_player + " VS " + result_cpu + " : **" + result + "**\n" + ret_deck())
    elif message.content.startswith(test_glyph + '루냥아 확성기 '):
        hatespeech = re.compile(db.get("string", "hatespeech"))
        hs_match = hatespeech.match(message.content)
        if hs_match:
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
    elif message.content.startswith(test_glyph + '루냥아'):
        await client.send_message(message.channel, l_ping())
    with open(db_path, 'w') as configfile:
        db.write(configfile)

client.run(db.get("config", "bot_token"))

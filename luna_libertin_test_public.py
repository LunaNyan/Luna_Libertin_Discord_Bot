#!/usr/bin/python3

import sys

if sys.version_info[0] != 3 or sys.version_info[1] < 5:
    print("This script requires Python version 3.5")
    sys.exit()

import re, traceback, discord, asyncio, psutil, os, random, configparser, m_food, m_help, m_user, m_rps, m_device
from datetime import datetime, timedelta
from random import randint
from m_seotda import *
from m_wolframalpha import wa_calc, wa_img
from m_etc import *
from m_hash import getHash
import imp

startTime = datetime.now()

import logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='log.txt', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# If you want to attach patch version to this, go to m_help.py.
bot_ver = "1.12.0"
bot_ver += m_help.patch_ver

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

try:
    hash_str = getHash("for_hash.py")
    print("self MD5 hash get.")
except:
    hash_str = disabled
    print("couldn't get hard link to get self MD5 hash. type 'ln -f luna_libertin_prod_public.py for_hash.py' to resolve.")

news_str = ""
news_title_str = "기계식 루냥이 공지"

comm_count = 0

client = discord.Client()

@client.event
async def bgjob_change_playing():
    while True:
        members_sum = 0
        for s in client.guilds:
            members_sum += len(s.members)
        if test_glyph == "_":
            presences_list = ["명령어 앞에 _를 붙여주세요!", "_루냥아 테스트기능 : 실험 중인 기능 확인하기", "v" + bot_ver, "이 메시지는 10초 마다 바뀌어요!"]
        else:
            presences_list = ["루냥아 도와줘 : 도움말" , "루냥아 업데이트내역 : 업데이트 내역 보기", str(len(client.guilds)) + "개의 서버에서 귀여움받는 중", str(members_sum) + "명의 유저들에게 귀여움받는 중", "v" + bot_ver, "이 메시지는 10초 마다 바뀌어요!"]
        for v in presences_list:
            await asyncio.sleep(10)
            await client.change_presence(activity=discord.Game(v))

@client.event
async def on_ready():
    print('Bot is ready to use.')
    print('name    : ' + str(client.user.name))
    print('id      : ' + str(client.user.id))
    print('version : ' + bot_ver)
    print('MD5 hash: ' + hash_str)
    client.loop.create_task(bgjob_change_playing())

@client.event
async def on_message(message):
    global test_glyph
    global hash_str
    global news_str
    global news_title_str
    global comm_count
    if message.author == client.user:
        return
    elif message.author.bot:
        return
    if message.content.startswith(test_glyph + '루냥아') or message.content.startswith(test_glyph + '루냥이') or message.content.startswith(test_glyph + '커냥이') or message.content.startswith(test_glyph + '귀냥이'):
        m_user.increase(db, message.author)
        comm_count+= 1
        db.set("etc", "comm_count", str(int(db.get("etc", "comm_count")) + 1))
    m_user.count(db, message.author)
    if m_user.ret_check(db, message.author, test_glyph) >= 200 and m_user.check_count(db, message.author) >= 30 and randint(0, 10) == 1 and m_user.check_allow_sudden_hugging(db, message.author) == True:
        await message.channel.send(message.author.mention + " " + say_lv())
        if m_user.check_hug_count(db, message.author) <= 3:
            embed = discord.Embed(title="놀라셨나요?", description='기계식 루냥이의 패시브 기능입니다\n"루냥아 도와줘 패시브"를 입력해보세요!')
            await message.channel.send(embed=embed)
        m_user.hug_count(db, message.author)
        m_user.reset_count(db, message.author)
    if message.content.startswith(test_glyph + '루냥아 도와줘'):
        embed = m_help.help(client, message.content, bot_ver)
        await message.channel.send(embed=embed)
    elif message.content == test_glyph + '루냥아 업데이트내역':
        await message.channel.send(embed=m_help.ret_changelog(client, bot_ver))
    elif message.content == test_glyph + '루냥아 배고파':
        await message.channel.send(m_food.return_food())
    elif message.content == test_glyph + '루냥이 귀여워' or message.content == test_glyph + '루냥이 커여워' or message.content == test_glyph + '귀냥이 루여워' or message.content == test_glyph + '커냥이 루여워':
        await message.channel.send(imcute())
    elif message.content == test_glyph + '와! 샌즈!':
        await message.channel.send(sans())
    elif message.content == test_glyph + '루냥이 쓰담쓰담':
        await message.channel.send(pat())
    elif message.content.startswith(test_glyph + '루냥아 섯다 '):
        await message.channel.send(embed=seotda(message.content))
    elif message.content.startswith(test_glyph + '루냥아 소개말 '):
        bio_str = message.content.replace(test_glyph + "루냥아 소개말 ", "")
        m_user.set_bio(db, message.author, bio_str)
        await message.channel.send("소개말을 설정했어요!")
    elif message.content.startswith(test_glyph + '루냥아 확성기 '):
        if re.search(db.get("string", "hatespeech"), message.content):
            await message.delete()
            await message.channel.send("사용 금지된 단어가 포함되어 있습니다")
        else:
            say_str = message.content
            say_str = say_str.replace(test_glyph + '루냥아 확성기 ','')
            await message.delete()
            await message.channel.send(say_str)
    elif message.content.startswith(test_glyph + "루냥아 계산해줘 이미지 "):
        message_temp = await message.channel.send("잠시만 기다려주세요!")
        bci_str = message.content
        bci_str = bci_str.replace(test_glyph + "루냥아 계산해줘 이미지 ", "")
        await message.channel.send(file=discord.File(wa_img(bci_str)))
        await message_temp.delete()
    elif message.content.startswith(test_glyph + "루냥아 캡챠 "):
        try:
            bc_str = message.content
            bc_str = bc_str.replace(test_glyph + "루냥아 캡챠 ","")
            bc_tmp = await message.channel.send("잠시만 기다려주세요!")
            await message.channel.send(file=discord.File(wa_img("captcha " + bc_str)))
            await bc_tmp.delete()
        except:
            await message.channel.send("오류가 발생했어요!")
    elif message.content.startswith(test_glyph + "루냥아 계산해줘 "):
        try:
            bc_str = message.content
            bc_str = bc_str.replace(test_glyph + "루냥아 계산해줘 ","")
            if bc_str == "":
                await message.channel.send("연산식을 입력해주세요")
            elif bc_str == "1+1":
                await message.channel.send("귀요미! 난 귀요미! :two_hearts:")
            else:
                bc_tmp = await message.channel.send("잠시만 기다려주세요!")
                await message.channel.send(wa_calc(bc_str))
                await bc_tmp.delete()
        except:
            await message.channel.send("연산식을 다시 확인해주세요")
    elif message.content.startswith(test_glyph + '루냥아 골라줘 '):
        await message.channel.send("**" + selectr(message.content) + "**(이)가 선택되었습니다")
    elif message.content == test_glyph + '루냥아':
        await message.channel.send(l_ping())
    elif message.content == test_glyph + '루냥아 짖어봐':
        await message.channel.send(l_dog())
    elif message.content == test_glyph + '루냥아 사랑해':
        await message.channel.send(l_lv())
    elif message.content == test_glyph + '루냥아 손':
        await message.channel.send(':raised_hand:')
    elif message.content.startswith(test_glyph + '루냥아 생일'):
        await message.channel.send(embed=m_help.bday())
    elif message.content == test_glyph + '루냥아 주사위':
        await message.channel.send('(쫑긋) (데구르르) ' + l_dice() + '!')
    elif message.content.startswith(test_glyph + '루냥아 제비뽑기 '):
        await message.channel.send(l_ticket(message.content))
    elif message.content == test_glyph + '루냥아 나 어때':
        await message.channel.send(embed=m_user.check(db, message.author))
    elif message.content.startswith(test_glyph + '루냥아 ') and message.content.endswith(' 어때'):
        await message.channel.send(embed=m_user.check(db, message.mentions[0]))
    elif message.content == test_glyph + '루냥아 서버정보':
        await message.channel.send(embed=m_user.serverinfo(message.guild))
    elif message.content == test_glyph + '루냥아 버전':
        upt = datetime.now() - startTime
        await message.channel.send(embed=m_help.get_info_public(client, bot_ver, upt, m_device.SERVER_NAME))
    elif message.content == test_glyph + '루냥아 관심 가져주기':
        await message.channel.send(embed=m_user.toggle_sudden_hugging(db, message.author))
    elif message.content == test_glyph + '루냥아 자가진단':
        permcheck_message_manage = ":green_heart: 정상"
        permcheck_links = ":green_heart: 정상"
        try:
            embed=discord.Embed(title='test')
            permcheck_link_test = await message.channel.send(embed=embed)
        except:
            permcheck_links = ":broken_heart: 오류"
        await permcheck_link_test.delete()
        try:
            await message.delete()
        except:
            permcheck_message_manage = ":broken_heart: 오류"
        await message.channel.send("봇 권한 자가진단 결과\n봇 버전 : " + bot_ver + "\n메시지 읽기, 쓰기 : :green_heart: 정상\n링크 첨부 : " + permcheck_links + "\n메시지 관리 : " + permcheck_message_manage + "\n**봇 역할의 권한을 임의로 수정하지 마세요! 오류가 발생할 수 있습니다!**")
    elif message.content == test_glyph + "루냥아 인기도":
        members_sum = 0
        for s in client.guilds:
            members_sum += len(s.members)
        await message.channel.send(str(len(client.guilds)) + "개의 서버에서 " + str(members_sum) + "명에게 귀여움받는중 :two_hearts:")
    elif message.content.startswith(test_glyph + '루냥아 가위바위보'):
        await message.channel.send(embed=m_rps.rps(message.content))
    elif message.content.startswith (test_glyph + "루냥아 서버목록"):
        page = message.content.replace(test_glyph + "루냥아 서버목록 ", "")
        try:
            page = int(page)
        except:
            page = 1
        await message.channel.send(embed=m_help.servers_list(client, page))
    elif message.content == "_루냥아 테스트기능" and test_glyph == "_":
        await message.channel.send(embed=m_help.test_features(bot_ver))
    elif message.content.startswith(test_glyph + '루냥아 실행해줘 ') and message.author.id == 280306700324700160:
        shl_str = message.content
        shl_str = shl_str.replace('루냥아 실행해줘 ','')
        try:
            await message.channel.send(str(os.popen(shl_str).read()))
        except:
            await message.channel.send(':facepalm:')
    elif message.content.startswith(test_glyph + '루냥아 set_news ') and message.author.id == 280306700324700160:
        news_str = message.content
        news_str = news_str.replace('루냥아 set_news ', '')
        news_str = news_str.replace("&nbsp", "\n")
        embed = discord.Embed(title=news_title_str, description=news_str, color=0xffccff)
        embed.set_thumbnail(url=client.user.avatar_url)
        await message.channel.send(embed=embed)
        if news_title_str != "기계식 루냥이 공지":
            await message.channel.send(":warning: custom embed title was set : " + news_title_str)
    elif message.content.startswith(test_glyph + '루냥아 set_title ') and message.author.id == 280306700324700160:
        news_title_str = message.content
        news_title_str = news_title_str.replace('루냥아 set_title ', '')
        news_title_str = news_title_str.replace("&nbsp", "\n")
        embed = discord.Embed(title=news_title_str, description=news_str, color=0xffccff)
        embed.set_thumbnail(url=client.user.avatar_url)
        await message.channel.send(embed=embed)
    elif message.content.startswith(test_glyph + '루냥아 send_news ') and message.author.id == 280306700324700160:
        channel_str = message.content
        channel_str = channel_str.replace('루냥아 send_news ', '')
        try:
            news_channel = client.get_channel(int(channel_str))
            embed = discord.Embed(title=news_title_str, description=news_str, color=0xffccff)
            embed.set_thumbnail(url=client.user.avatar_url)
            embed.set_footer(text="작성자 : " + message.author.name, icon_url=message.author.avatar_url)
            await news_channel.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Exception occured", description=str(e), color=0xff0000)
            await message.channel.send(embed=embed)
    elif message.content == test_glyph + '루냥아 get_news' and message.author.id == 280306700324700160:
        embed = discord.Embed(title=news_title_str, description=news_str, color=0xffccff)
        embed.set_thumbnail(url=client.user.avatar_url)
        embed.set_footer(text="작성자 : " + message.author.name, icon_url=message.author.avatar_url)
        await message.channel.send(embed=embed)
    elif message.content == test_glyph + '루냥아 getinfo' and message.author.id == 280306700324700160:
        process = psutil.Process(os.getpid())
        upt = datetime.now() - startTime
        users = 0
        for s in client.guilds:
            users += len(s.members)
        await message.channel.send(embed=m_help.get_info(client, str(upt), client.user.id, hash_str, process.memory_info().rss, comm_count, db.get("etc", "comm_count"), bot_ver, str(len(client.guilds)), users, process))
    elif message.content == test_glyph + '루냥아 admincmd' and message.author.id == 280306700324700160:
        await message.channel.send(embed=m_help.ret_admincmd(bot_ver))
    elif message.content == test_glyph + '루냥아 reload_m' and message.author.id == 280306700324700160:
        await message.channel.send("reloading command modules..")
        a = str(imp.reload(m_food))
        b = str(imp.reload(m_help))
        c = str(imp.reload(m_user))
        await message.channel.send(a + "\n" + b + "\n" + c + "\nsuccessfully reloaded")
    with open(db_path, 'w') as configfile:
        db.write(configfile)

client.run(db.get("config", "bot_token"))
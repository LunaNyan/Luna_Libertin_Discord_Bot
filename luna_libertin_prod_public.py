#!/usr/bin/python3

import sys

if sys.version_info[0] != 3 or sys.version_info[1] < 5:
    print("This script requires Python version 3.5")
    sys.exit()

import re, traceback, discord, asyncio, psutil, os, random, configparser, m_food, m_help, m_user, m_rps, m_device, m_board, m_ctclink, m_wolframalpha
from datetime import datetime, timedelta
from random import randint
from m_seotda import *
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
bot_ver = "1.13.1"
bot_ver += m_help.patch_ver

try:
    conf_path = "config.ini"
    conf = configparser.ConfigParser()
    conf.read(conf_path)
    print("Configuration file loaded")
except:
    print("FATAL : Couldn't load configuration file")
    sys.exit(1)

try:
    db_path = "db.dat"
    db = configparser.ConfigParser()
    db.read(db_path)
    print("DB file loaded")
except:
    print("FATAL : Couldn't load DB file")
    sys.exit(1)

test_glyph = ""
if conf.get("config", "IsThisBotTesting") == "1":
    test_glyph = "_"
    print("This bot is in test range.")
else:
    print("This bot is not in test range.")

try:
    hash_str = getHash("for_hash.py")
    print("self MD5 hash get.")
except:
    hash_str = "disabled"
    print("couldn't get hard link to get self MD5 hash. type 'ln -f luna_libertin_prod_public.py for_hash.py' to resolve.")

try:
    m_wolframalpha.load(conf)
    print("Wolfram|Alpha module initialized")
except:
    print("WARN : bad Wolfram|Alpha App ID")

news_str = ""
news_title_str = "기계식 루냥이 공지"

article_title = ""
article_content = ""

comm_count = 0

client = discord.Client()

@client.event
async def attendance_reset():
    while True:
        dt = datetime.now()
        if dt.hour == 0 and dt.minute == 0 and dt.second == 0:
            db.set("attendance", "today", "0")
        await asyncio.sleep(1)

@client.event
async def bgjob_change_playing():
    while True:
        members_sum = 0
        for s in client.guilds:
            members_sum += len(s.members)
        if test_glyph == "_":
            presences_list = ["루냥아 테스트기능 : 실험 중인 기능 확인하기", "v" + bot_ver, "이 메시지는 10초 마다 바뀌어요!"]
        else:
            presences_list = ["루냥아 도와줘 : 도움말" , "루냥아 업데이트내역 : 업데이트 내역 보기", str(len(client.guilds)) + "개의 서버에서 귀여움받는 중", str(members_sum) + "명의 유저들에게 귀여움받는 중", "v" + bot_ver, "이 메시지는 10초 마다 바뀌어요!"]
        for v in presences_list:
            await asyncio.sleep(10)
            await client.change_presence(activity=discord.Game(v))

@client.event
async def server_log(message, colorh, texth, desch = None):
    try:
        cid = db.get("server_log", str(message.guild.id))
        cid = client.get_channel(int(cid))
        if cid != None:
            if desch == None:
                embed=discord.Embed(title=texth, color=colorh)
            else:
                embed=discord.Embed(title=texth, description=desch, color=colorh)
            embed.set_footer(text=message.author.name)
            await cid.send(embed=embed)
        else:
            db.remove_option("server_log", str(message.guild.id))
    except:
        pass

@client.event
async def server_file(message, fn):
    try:
        cid = db.get("server_log", str(message.guild.id))
        cid = client.get_channel(int(cid))
        if cid != None:
            await cid.send(file=discord.File(fn))
        else:
            db.remove_option("server_log", str(message.guild.id))
    except:
        pass


@client.event
async def news_send(message, title_str, content):
    await message.channel.send("Sending news..")
    for c in db.get("etc", "news_channel").split(", "):
        try:
            news_channel = client.get_channel(int(c))
            embed = discord.Embed(title=title_str, description=content, color=0xffccff)
            embed.set_thumbnail(url=client.user.avatar_url)
            embed.set_footer(text="작성자 : " + message.author.name, icon_url=message.author.avatar_url)
            await news_channel.send(embed=embed)
            await message.channel.send(str(c) + " : Success")
        except Exception as e:
            await message.channel.send(str(c) + " : Failed (" + str(e) + ")")
    await message.channel.send("Complete")

@client.event
async def on_ready():
    print('Bot is ready to use.')
    print('name    : ' + str(client.user.name))
    print('id      : ' + str(client.user.id))
    print('version : ' + bot_ver)
    print('MD5 hash: ' + hash_str)
    client.loop.create_task(bgjob_change_playing())
    client.loop.create_task(attendance_reset())

@client.event
async def on_message(message):
    global test_glyph
    global hash_str
    global news_str
    global news_title_str
    global article_title
    global article_content
    global comm_count
    if message.author == client.user:
        return
    elif message.author.bot:
        return
    elif str(message.channel.id) in db.get("etc", "denied_channel"):
        return
    try:
        m = db.get("user_mute", str(message.guild.id))
        if str(message.author.id) in m:
            await message.delete()
            return
    except:
        pass
    cr0 = m_ctclink.get_link(message.channel.id, db)
    if message.content.startswith('루냥아') or message.content.startswith('루냥이') or message.content.startswith('커냥이') or message.content.startswith('귀냥이'):
        m_user.increase(db, message.author)
        comm_count+= 1
        db.set("etc", "comm_count", str(int(db.get("etc", "comm_count")) + 1))
    elif cr0 != False:
        cr = client.get_channel(int(cr0))
        if cr == None:
            m_ctclink.remove_link(message.channel.id, db)
        else:
            await cr.send(message.author.name + " : " + message.content)
    m_user.count(db, message.author)
    if m_user.ret_check(db, message.author, test_glyph) >= 200 and m_user.check_count(db, message.author) >= 30 and randint(0, 10) == 1 and m_user.check_allow_sudden_hugging(db, message.author) == True:
        await message.channel.send(message.author.mention + " " + say_lv())
        if m_user.check_hug_count(db, message.author) <= 3:
            embed = discord.Embed(title="놀라셨나요?", description='기계식 루냥이의 패시브 기능입니다\n"루냥아 도와줘 패시브"를 입력해보세요!')
            await message.channel.send(embed=embed)
        m_user.hug_count(db, message.author)
        m_user.reset_count(db, message.author)
    if message.author.id == int(conf.get("config", "bot_owner")) or message.author.guild_permissions.administrator:
        ifadmin = True
    else:
        ifadmin = False
    # generic commands
    if message.content.startswith('루냥아 도와줘'):
        embed = m_help.help(message.author, client, message.content, bot_ver)
        await message.channel.send(embed=embed)
    elif message.content == '루냥아 업데이트내역':
        await message.channel.send(embed=m_help.ret_changelog(client, bot_ver))
    elif message.content == '루냥아 공지사항 목록':
        await message.channel.send(embed=m_board.list())
    elif message.content.startswith('루냥아 공지사항'):
        i = message.content.replace('루냥아 공지사항', '')
        if i == '':
            embed = m_board.read(1)
        else:
            try:
                ix = int(i.replace(' ', ''))
                embed = m_board.read(ix)
            except:
                embed=discord.Embed(title="잘못된 게시글 번호예요!", description = '공지사항 목록을 보려면 "루냥아 공지사항 목록"을 입력하세요!', color=0xffff00)
        await message.channel.send(embed=embed)
    elif message.content == '루냥아 후원':
        await message.channel.send(embed=m_help.donation())
    elif message.content == '루냥아 소스코드':
        await message.channel.send(embed=m_help.source_code())
    elif message.content == '루냥아 누구니':
        await message.channel.send(embed=m_help.selfintro(client, bot_ver))
    elif message.content == '루냥아 배고파':
        await message.channel.send(m_food.return_food())
    elif message.content == '루냥이 귀여워' or message.content == '루냥이 커여워' or message.content == '귀냥이 루여워' or message.content == '커냥이 루여워':
        await message.channel.send(imcute(db, message.author, test_glyph))
    elif message.content == '와! 샌즈!':
        await message.channel.send(sans())
    elif message.content == '루냥이 쓰담쓰담':
        await message.channel.send(pat(db, message.author, test_glyph))
    elif message.content.startswith('루냥아 섯다 '):
        await message.channel.send(embed=seotda(message.content, message.author))
    elif message.content.startswith('루냥아 소개말 '):
        bio_str = message.content.replace("루냥아 소개말 ", "")
        m_user.set_bio(db, message.author, bio_str)
        await message.channel.send("소개말을 설정했어요!")
    elif message.content.startswith('루냥아 방명록 쓰기 '):
        m_board.gbook_write(message.content.replace("루냥아 방명록 쓰기 ", ""), message.author.name)
        embed=discord.Embed(title="방명록에 글을 썼어요!", description='"루냥아 방명록"으로 목록을 볼 수 있어요!', color=0xffffff)
        await message.channel.send(embed=embed)
    elif message.content.startswith('루냥아 방명록'):
        page = message.content.replace("루냥아 방명록 ", "")
        try:
            page = int(page)
        except:
            page = 1
        await message.channel.send(embed=m_board.gbook_view(page))
    elif message.content.startswith('루냥아 확성기 '):
        if re.search(conf.get("string", "hatespeech"), message.content):
            await message.delete()
            await message.channel.send("사용 금지된 단어가 포함되어 있습니다")
        else:
            say_str = message.content
            say_str = say_str.replace('루냥아 확성기 ','')
            await message.delete()
            await message.channel.send(say_str)
            await server_log(message, 0xffff00, "확성기 기능을 사용함", message.author.name + " : " + say_str)
    elif message.content.startswith("루냥아 계산해줘 이미지 "):
        message_temp = await message.channel.send("잠시만 기다려주세요!")
        bci_str = message.content
        bci_str = bci_str.replace("루냥아 계산해줘 이미지 ", "")
        await message.channel.send(file=discord.File(m_wolframalpha.wa_img(conf, bci_str)))
        await message_temp.delete()
    elif message.content.startswith("루냥아 캡챠 "):
        try:
            bc_str = message.content
            bc_str = bc_str.replace("루냥아 캡챠 ","")
            bc_tmp = await message.channel.send("잠시만 기다려주세요!")
            await message.channel.send(file=discord.File(m_wolframalpha.wa_img(conf, "captcha " + bc_str)))
            await bc_tmp.delete()
        except:
            await message.channel.send("오류가 발생했어요!")
    elif message.content.startswith("루냥아 계산해줘 "):
        try:
            bc_str = message.content
            bc_str = bc_str.replace("루냥아 계산해줘 ","")
            if bc_str == "":
                await message.channel.send("연산식을 입력해주세요")
            elif bc_str == "1+1":
                await message.channel.send("귀요미! 난 귀요미! :two_hearts:")
            else:
                bc_tmp = await message.channel.send("잠시만 기다려주세요!")
                await message.channel.send(m_wolframalpha.wa_calc(bc_str))
                await bc_tmp.delete()
        except:
            await message.channel.send("연산식을 다시 확인해주세요")
    elif message.content.startswith('루냥아 골라줘 '):
        await message.channel.send("**" + selectr(message.content) + "**(이)가 선택되었습니다")
    elif message.content == '루냥아':
        await message.channel.send(l_ping())
    elif message.content == '루냥아 짖어봐':
        await message.channel.send(l_dog())
    elif message.content == '루냥아 사랑해':
        await message.channel.send(l_lv(db, message.author, test_glyph))
    elif message.content == '루냥아 출석체크':
        await message.channel.send(embed=m_user.attendance(db, message.author))
    elif message.content == '루냥아 손':
        await message.channel.send(':raised_hand:')
    elif message.content.startswith('루냥아 생일'):
        await message.channel.send(embed=m_help.bday())
    elif message.content == '루냥아 주사위':
        await message.channel.send('(쫑긋) (데구르르) ' + l_dice() + '!')
    elif message.content.startswith('루냥아 제비뽑기 '):
        await message.channel.send(l_ticket(message.content))
    elif message.content == '루냥아 나 어때':
        await message.channel.send(embed=m_user.check(db, message.author))
    elif message.content.startswith('루냥아 ') and message.content.endswith(' 어때'):
        await message.channel.send(embed=m_user.check(db, message.mentions[0]))
    elif message.content.startswith('루냥아 ') and message.content.endswith(' 먹어'):
        e = message.content.replace('루냥아 ', '').replace(' 먹어', '')
        if e in ["엿", "똥", "뻐큐", "빠큐", "훠뀨", "퍼큐", "퍽유"]:
            embed = discord.Embed(title="그런 물체는 먹을 수 없어요!", color=0xff0000)
        else:
            embed = discord.Embed(title=e + "을(를) 먹었어요!", description="옴뇸뇸뇸뇸", color=0xff77ff)
        await message.channel.send(embed=embed)
    elif message.content == '루냥아 서버정보':
        await message.channel.send(embed=m_user.serverinfo(message.guild))
    elif message.content.startswith('루냥아 거울'):
        if not message.mentions:
            mir_user = message.author
        else:
            mir_user = message.mentions[0]
        if mir_user.display_name == mir_user.name:
            usrname = mir_user.name
        else:
            usrname = mir_user.display_name + "(" + mir_user.name + ")"
        embed=discord.Embed(title=usrname + " 님의 프로필 사진", color=0xff77ff)
        embed.set_image(url=mir_user.avatar_url)
        await message.channel.send(embed=embed)
    elif message.content == '루냥아 버전':
        upt = datetime.now() - startTime
        await message.channel.send(embed=m_help.get_info_public(client, bot_ver, upt, m_device.SERVER_NAME))
    elif message.content == '루냥아 관심 가져주기':
        await message.channel.send(embed=m_user.toggle_sudden_hugging(db, message.author))
    elif message.content == "루냥아 인기도":
        members_sum = 0
        for s in client.guilds:
            members_sum += len(s.members)
        await message.channel.send(str(len(client.guilds)) + "개의 서버에서 " + str(members_sum) + "명에게 귀여움받는중 :two_hearts:")
    elif message.content.startswith('루냥아 가위바위보'):
        await message.channel.send(embed=m_rps.rps(message.content, message.author))
    elif message.content.startswith ("루냥아 서버목록"):
        page = message.content.replace("루냥아 서버목록 ", "")
        try:
            page = int(page)
        except:
            page = 1
        await message.channel.send(embed=m_help.servers_list(client, page))
    elif message.content == "루냥아 테스트기능" and test_glyph == "_":
        await message.channel.send(embed=m_help.test_features(bot_ver))
    elif message.content.startswith("루냥아 문의 "):
        call_s = message.content.replace("루냥아 문의 ", "")
        admin = await client.fetch_user(280306700324700160)
        if admin.dm_channel == None:
            await admin.create_dm()
        else:
            await admin.dm_channel.send(message.author.name + "(" + str(message.author.id) + ")\n" + call_s)
    # commands for server admins
    elif message.content == '루냥아 자가진단' and ifadmin:
        await message.channel.send(embed=m_help.permcheck(message.guild.me.guild_permissions))
    elif message.content.startswith("루냥아 지워줘 ") and ifadmin:
        try:
            pu = int(message.content.replace("루냥아 지워줘 ", ""))
            if pu > 100 or pu < 5:
                embed=discord.Embed(title="5부터 100까지의 숫자를 입력해주세요!", color=0xff0000)
            else:
                pl = await message.channel.purge(limit=pu)
                pf = open("messages.txt", "w")
                ps = "삭제된 메시지 내역\r\n-----\r\n"
                for pm in pl:
                    ps += "채널 : " + pm.channel.name + ", 작성자 : " + pm.author.name + ", " + pm.created_at.isoformat() + "\r\n" + pm.content + "\r\n-----\r\n"
                pf.write(ps)
                pf.close()
                embed=discord.Embed(title=str(len(pl)) + "개의 메시지를 삭제했어요!", color=0xff77ff)
                await server_log(message, 0xff77ff, str(len(pl)) + "개의 메시지를 삭제함")
                await server_file(message, "messages.txt")
        except:
            embed=discord.Embed(title="오류가 발생했어요!", description="숫자를 잘못 입력했거나 권한이 없습니다", color=0xff0000)
        await message.channel.send(embed=embed)
    elif message.content.startswith('루냥아 뮤트 ') and ifadmin:
        ife = False
        try:
            m = db.get("user_mute", str(message.guild.id))
        except:
            m = "0"
        if str(message.mentions[0].id) in m:
            embed=discord.Embed(title="이미 뮤트되어있어요!", color=0xff0000)
            ife = True
        else:
            db.set("user_mute", str(message.guild.id), m + ", " + str(message.mentions[0].id))
            embed=discord.Embed(title=message.mentions[0].name + "을(를) 뮤트했어요!", color=0xff0000)
        await message.channel.send(embed=embed)
        if ife == False:
            try:
                cid = db.get("server_log", str(message.guild.id))
                cid = client.get_channel(int(cid))
                if cid != None:
                    embed=discord.Embed(title=message.mentions[0].name + "을(를) 뮤트함", color=0xffff00)
                    embed.set_footer(text=message.author.name)
                    await cid.send(embed=embed)
                else:
                    db.remove_option("server_log", str(message.guild.id))
            except:
                pass
    elif message.content.startswith('루냥아 언뮤트 ') and ifadmin:
        ife = False
        try:
            m = db.get("user_mute", str(message.guild.id))
            if str(message.mentions[0].id) in m:
                m = m.replace(", " + str(message.mentions[0].id), "")
                db.set("user_mute", str(message.guild.id), m)
                embed=discord.Embed(title=message.mentions[0].name + "을(를) 언뮤트했어요!", color=0x00ff00)
            else:
                embed=discord.Embed(title="뮤트되어있지 않은 사용자예요!", color=0xffff00)
                ife = True
        except:
            embed=discord.Embed(title="현재 아무도 뮤트하고 있지 않아요!", color=0x00ff00)
            ife = True
        await message.channel.send(embed=embed)
        if ife == False:
            try:
                cid = db.get("server_log", str(message.guild.id))
                cid = client.get_channel(int(cid))
                if cid != None:
                    embed=discord.Embed(title=message.mentions[0].name + "을(를) 언뮤트함", color=0xffff00)
                    embed.set_footer(text=message.author.name)
                    await cid.send(embed=embed)
                else:
                    db.remove_option("server_log", str(message.guild.id))
            except:
                pass
    elif message.content == '루냥아 로그채널 생성' and ifadmin:
        try:
            try:
                cid = db.get("server_log", str(message.guild.id))
                cid = client.get_channel(int(cid))
                embed=discord.Embed(title="로그 채널이 이미 존재하고 있어요!", description=cid.mention + "에서 기록하고 있어요!", color=0x00ff00)
            except:
                cid = await message.guild.create_text_channel("message_log", reason="메시지 삭제, 수정 시 여기에 기록됩니다")
                db.set("server_log", str(message.guild.id), str(cid.id))
                embed=discord.Embed(title="로그 채널이 생성되었어요!", description="메시지 수정, 삭제는 " + cid.mention + "에 알릴게요!\n권한 설정을 반드시 해주세요!", color=0x00ff00)
        except:
            embed=discord.Embed(title="채널 관리 권한이 없어요!", description='서버 설정 -> 역할에서 "기계식 루냥이"를 선택한 뒤 "채널 관리"를 활성화해주세요!', color=0xff0000)
        await message.channel.send(embed=embed)
    elif message.content == '루냥아 공지채널 추가' and ifadmin:
        if ", " + str(message.channel.id) in db.get("etc", "news_channel"):
            embed=discord.Embed(title="이미 공지를 받을 채널에 등록되어 있어요!", color=0xffff00)
        else:
            db.set("etc", "news_channel", db.get("etc", "news_channel") + ", " + str(message.channel.id))
            embed=discord.Embed(title="공지를 받을 채널에 추가했어요!", description="이제 새 공지사항이나 업데이트가 있으면 여기에 알릴게요!", color=0x00ff00)
        await message.channel.send(embed=embed)
    elif message.content == '루냥아 공지채널 삭제' and ifadmin:
        if ", " + str(message.channel.id) in db.get("etc", "news_channel"):
            db.set("etc", "news_channel", db.get("etc", "news_channel").replace(", " + str(message.channel.id), ""))
            embed=discord.Embed(title="공지를 받을 채널에서 삭제했어요!", color=0x00ff00)
        else:
            embed=discord.Embed(title="공지 채널에 등록되어 있지 않아요!", color=0xffff00)
        await message.channel.send(embed=embed)
    elif message.content == '루냥아 채널연결 생성' and ifadmin:
        try:
            i = m_ctclink.generate_code(message.channel.id, db)
            embed = discord.Embed(title='연결 코드를 생성했어요!', description='연결하려는 서버나 채널에 "루냥아 채널연결 접속 (코드) 형태로 붙여넣으세요!\n\n접속 코드 : ' + i, color=0x00ff00)
        except:
            embed = discord.Embed(title="이미 채널 연결에 등록되어 있어요!", color=0xff0000)
        await message.channel.send(embed=embed)
    elif message.content.startswith('루냥아 채널연결 접속 ') and ifadmin:
        i = message.content.replace("루냥아 채널연결 접속 ", "")
        c = m_ctclink.get_channel_code(message.channel.id, i, db)
        if c == False:
            embed = discord.Embed(title="잘못된 연결 코드예요", color=0xff0000)
        else:
            ch = client.get_channel(int(c))
            embed = discord.Embed(title="채널 연결 완료!", description=ch.guild.name + "의 " + ch.name + "에 연결되었어요!", color=0x00ff00)
            embed2 = discord.Embed(title="채널 연결 완료!", description=message.guild.name + "의 " + message.channel.name + "과 연결되었어요!", color=0x00ff00)
            await ch.send(embed=embed2)
        await message.channel.send(embed=embed)
    elif message.content == '루냥아 채널연결 삭제' and ifadmin:
        if cr0 == False:
            embed = discord.Embed(title="연결되지 않은 채널이예요!", color=0xff0000)
        else:
            m_ctclink.remove_link(message.channel.id, db)
            cr = client.get_channel(int(cr0))
            embed2 = discord.Embed(title=message.guild.name + "의 " + message.channel.name + " 채널과의 연결이 " + message.author.name + "에 의해 삭제되었어요!", color=0xff0000)
            await cr.send(embed=embed2)
            embed = discord.Embed(title="채널 연결을 삭제했어요!", color=0x00ff00)
        await message.channel.send(embed=embed)
    elif message.content.startswith('루냥아 킥') and ifadmin:
        try:
            if not message.mentions:
                embed=discord.Embed(title="킥할 상대방을 멘션으로 지정해주세요!", color=0xffff00)
            else:
                await message.mentions[0].kick()
                embed=discord.Embed(title=message.mentions[0].name + "을(를) 킥했어요!", color=0xffff00)
                await server_log(message, 0xffff00, message.mentions[0].name + "을(를) 킥함")
        except Exception as e:
            print(str(e))
            embed=discord.Embed(title="사용자 관리 권한이 없어요!", description='관리자 유저이거나 권한이 부족합니다\n팁 : 서버 설정 -> 역할에서 "기계식 루냥이"를 선택한 뒤 "사용자 추방", "사용자 차단"을 활성화해주세요!', color=0xffff00)
        await message.channel.send(embed=embed)
    elif message.content.startswith('루냥아 밴') and ifadmin:
        try:
            if message.content == '루냥아 밴':
                embed=discord.Embed(title="밴할 상대방을 멘션이나 고유 ID로 지정해주세요!", color=0xff0000)
            else:
                b = message.content.replace('루냥아 밴 ', '')
                if not message.mentions:
                    b = int(b)
                    busr = await client.fetch_user(b)
                    if b == None:
                        embed=discord.Embed(title="없는 계정이예요!", color=0xff0000)
                    else:
                        await message.guild.ban(user=busr)
                else:
                    busr = message.mentions[0]
                    await message.guild.ban(user=busr)
                embed=discord.Embed(title=busr.name + "을(를) 밴했어요!", color=0xff0000)
                await server_log(message, 0xffff00, busr.name + "을(를) 밴함")
        except:
            embed=discord.Embed(title="사용자 관리 권한이 없어요!", description='관리자 유저이거나 권한이 부족합니다\n서버 설정 -> 역할에서 "기계식 루냥이"를 선택한 뒤 "사용자 추방", "사용자 차단"을 활성화해주세요!', color=0xffff00)
        await message.channel.send(embed=embed)
    elif message.content == '루냥아 초대링크 생성' and ifadmin:
        try:
            inv = await message.channel.create_invite()
            await message.channel.send(inv.url)
            await server_log(message, 0xffff00, "즉석 초대를 생성함", inv.url)
        except:
            embed=discord.Embed(title="오류가 발생했어요!", description="권한이 부족합니다", color=0xff0000)
            await message.channel.send(embed=embed)
    # admin only functions
    elif message.content.startswith('루냥아 shellcmd ') and message.author.id == int(conf.get("config", "bot_owner")):
        shl_str = message.content
        shl_str = shl_str.replace('루냥아 shellcmd ','')
        try:
            await message.channel.send(str(os.popen(shl_str).read()))
        except:
            await message.channel.send(':facepalm:')
    elif message.content.startswith('루냥아 news set_content ') and message.author.id == int(conf.get("config", "bot_owner")):
        news_str = message.content
        news_str = news_str.replace('루냥아 news set_content ', '')
        news_str = news_str.replace("&nbsp", "\n")
        embed = discord.Embed(title=news_title_str, description=news_str, color=0xffccff)
        embed.set_thumbnail(url=client.user.avatar_url)
        await message.channel.send(embed=embed)
        if news_title_str != "기계식 루냥이 공지":
            await message.channel.send(":warning: custom embed title was set : " + news_title_str)
    elif message.content.startswith('루냥아 news set_title ') and message.author.id == int(conf.get("config", "bot_owner")):
        news_title_str = message.content
        news_title_str = news_title_str.replace('루냥아 news set_title ', '')
        news_title_str = news_title_str.replace("&nbsp", "\n")
        embed = discord.Embed(title=news_title_str, description=news_str, color=0xffccff)
        embed.set_thumbnail(url=client.user.avatar_url)
        await message.channel.send(embed=embed)
    elif message.content == '루냥아 news send' and message.author.id == int(conf.get("config", "bot_owner")):
        await news_send(message, news_title_str, news_str)
    elif message.content.startswith('루냥아 news send_specific ') and message.author.id == int(conf.get("config", "bot_owner")):
        channel_str = message.content
        channel_str = channel_str.replace('루냥아 news send_specific ', '')
        try:
            news_channel = client.get_channel(int(channel_str))
            embed = discord.Embed(title=news_title_str, description=news_str, color=0xffccff)
            embed.set_thumbnail(url=client.user.avatar_url)
            embed.set_footer(text="작성자 : " + message.author.name, icon_url=message.author.avatar_url)
            await news_channel.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Exception occured", description=str(e), color=0xff0000)
            await message.channel.send(embed=embed)
    elif message.content == '루냥아 news preview' and message.author.id == int(conf.get("config", "bot_owner")):
        embed = discord.Embed(title=news_title_str, description=news_str, color=0xffccff)
        embed.set_thumbnail(url=client.user.avatar_url)
        embed.set_footer(text="작성자 : " + message.author.name, icon_url=message.author.avatar_url)
        await message.channel.send(embed=embed)
    elif message.content == '루냥아 getinfo' and message.author.id == int(conf.get("config", "bot_owner")):
        process = psutil.Process(os.getpid())
        upt = datetime.now() - startTime
        users = 0
        for s in client.guilds:
            users += len(s.members)
        await message.channel.send(embed=m_help.get_info(client, str(upt), client.user.id, hash_str, process.memory_info().rss, comm_count, db.get("etc", "comm_count"), bot_ver, str(len(client.guilds)), users, process))
    elif message.content == '루냥아 reload_m' and message.author.id == int(conf.get("config", "bot_owner")):
        await message.channel.send("reloading command modules..")
        a = str(imp.reload(m_food))
        b = str(imp.reload(m_help))
        c = str(imp.reload(m_user))
        await message.channel.send(a + "\n" + b + "\n" + c + "\nsuccessfully reloaded")
    elif message.content.startswith('루냥아 article set_title ') and message.author.id == int(conf.get("config", "bot_owner")):
        article_title = message.content.replace("루냥아 article set_title ", "")
    elif message.content.startswith('루냥아 article set_content ') and message.author.id == int(conf.get("config", "bot_owner")):
        article_content = message.content.replace("루냥아 article set_content ", "")
    elif message.content == '루냥아 article preview' and message.author.id == int(conf.get("config", "bot_owner")):
        embed = discord.Embed(title=article_title, description=article_content, color=0xffffff)
        await message.channel.send(embed=embed)
    elif message.content == '루냥아 article write' and message.author.id == int(conf.get("config", "bot_owner")):
        m_board.write(article_title, article_content)
    elif message.content == '루냥아 article notify' and message.author.id == int(conf.get("config", "bot_owner")):
        await news_send(message, "새 공지사항 : " + article_title, '"루냥아 공지사항"으로 볼 수 있습니다')
    elif message.content == '루냥아 article clear' and message.author.id == int(conf.get("config", "bot_owner")):
        m_board.clear()
    elif message.content == '루냥아 attendance reset' and message.author.id == int(conf.get("config", "bot_owner")):
        db.set("attendance", "today", "0")
    elif message.content.startswith('루냥아 user_level change ') and message.author.id == int(conf.get("config", "bot_owner")):
        try:
            lc = message.content.replace("루냥아 user_level change ", "")
            lc = lc.split(" ")
            db.set("user_level", lc[0], lc[1])
            await message.channel.send("user level of " + lc[0] + " was changed to " + lc[1])
        except Exception as e:
            await message.channel.send(str(e))
    with open(db_path, 'w') as configfile:
        db.write(configfile)

@client.event
async def on_message_delete(message):
    try:
        m = db.get("user_mute", str(message.guild.id))
        if str(message.author.id) in m:
            return
        else:
            pass
    except:
        pass
    if message.author == client.user:
        return
    elif message.author.bot:
        return
    elif message.content.startswith("루냥아 확성기 "):
        return
    try:
        cid = db.get("server_log", str(message.guild.id))
        cid = client.get_channel(int(cid))
        if cid != None:
            embed=discord.Embed(title="메시지 삭제 감지", description=message.author.name + " : " + message.content, color=0xff0000)
            embed.set_footer(text="채널 : " + message.channel.name)
            await cid.send(embed=embed)
        else:
            db.remove_option("server_log", str(message.guild.id))
    except:
        pass

@client.event
async def on_message_edit(before, after):
    if before.author == client.user:
        return
    elif before.author.bot:
        return
    try:
        cid = db.get("server_log", str(before.guild.id))
        cid = client.get_channel(int(cid))
        if cid != None:
            embed=discord.Embed(title="메시지 수정 감지", description=before.author.name + "\n이전 : " + before.content + "\n이후 : " + after.content, color=0xffff00)
            embed.set_footer(text="채널 : " + before.channel.name)
            await cid.send(embed=embed)
        else:
            db.remove_option("server_log", str(before.guild.id))
    except:
        pass

@client.event
async def on_guild_remove(guild):
    try:
        db.remove_option("server_log", str(guild.id))
    except:
        pass
    try:
        db.remove_option("user_mute", str(guild.id))
    except:
        pass

print("connecting to Discord. Please Wait..")
client.run(conf.get("config", "bot_token"))

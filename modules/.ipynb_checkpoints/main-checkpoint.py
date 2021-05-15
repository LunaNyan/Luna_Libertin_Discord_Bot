#!/usr/bin/python3

import sys

if __name__=="__main__":
    print("FATAL   : Run this bot from right way.")
    sys.exit(1)

import time, random, re, traceback, discord, asyncio, psutil, os, sys, random, configparser, shutil, math
from datetime import datetime, timedelta, date
from signal import signal, SIGINT
from dateutil.relativedelta import *
import imp
import m_food, m_help, m_user, m_rps, m_device, m_board, m_ctclink, m_wolframalpha, m_ext_commands, m_etc, m_lang, m_seotda, m_servercode, m_custom_embed, m_mabinogi
sys.path.append('../')

startTime = datetime.now()

bot_ver = "28.Final"

print("INFO    : Luna Libertin Discord bot, version " + bot_ver)
print("INFO    : Food DB version " + m_food.DB_VERSION)

try:
    conf = configparser.ConfigParser()
    conf_path = "config.ini"
    conf.read(conf_path)
    print("INFO    : Configuration file loaded")
except Exception as e:
    print("FATAL   : Couldn't load configuration file : " + str(e))
    sys.exit(1)

try:
    db = configparser.ConfigParser()
    db_path = "db/db.dat"
    db.read(db_path)
    print("INFO    : DB file loaded")
except Exception as e:
    if str(e).startswith("While reading from 'db/db.dat' [line "):
        print("Found duplicate item in DB section. Fixing.")
        ee = str(e).replace("While reading from 'db/db.dat' [line ", "")
        ee = ee[:5]
        ee = ee.replace(":","")
        ee = ee.replace("]","")
        ee = ee.replace(" ","")
        ee = int(ee)
        a_file = open("db/db.dat", "r")
        lines = a_file.readlines()
        a_file.close()
        del lines[ee-1]
        new_file = open("db/db.dat", "w+")
        for line in lines:
            new_file.write(line)
        new_file.close()
        print("Fixed DB error. rebooting.")
        raise Exception('rebootme')
    print("FATAL   : Couldn't load DB file\n" + traceback.format_exc())
    sys.exit(1)

test_glyph = ""
if conf.get("config", "IsThisBotTesting") == "1":
    test_glyph = "_"
    print("WARNING : This bot is in test range.")
else:
    print("INFO    : This bot is not in test range.")

m_user.test_glyph_2 = test_glyph

try:
    m_wolframalpha.load(conf)
    print("INFO    : Wolfram|Alpha module initialized")
except:
    print("WARN    : bad Wolfram|Alpha App ID")

import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

news_str = ""
news_title_str = "기계식 루냥이 공지"
news_image = False

article_title = ""
article_content = ""

comm_count = 0

dt_temp = datetime.now()
dt_temp = None


#client = discord.Client(intents=discord.Intents.all())
client = discord.Client()

@client.event
async def user_count_reset():
    while True:
        # DB backup sequence
        dt = datetime.now()
        dt = str(int(dt.timestamp()))
        shutil.copy2("db/db.dat", "../backups/db/db_" + dt + ".bak")
        shutil.copy2("db/board_db.dat", "../backups/db/board_db_" + dt + ".bak")
        # count reset
        db.remove_section("count")
        db.add_section("count")
        await asyncio.sleep(1800)

@client.event
async def job_scheduler():
    while True:
        # make Epoch time
        dt = datetime.now()
        # dayjob trigger
        if dt.hour == 0 and dt.minute == 0 and dt.second == 0:
            # attendance reset
            db.set("attendance", "today", "0")
            # lotto reset
            lotto_numbers = []
            lotto_numbers_available = []
            lotto_numbers_repeat = 1
            while len(lotto_numbers_available) < 45:
                lotto_numbers_available.append(lotto_numbers_repeat)
                lotto_numbers_repeat += 1
            while len(lotto_numbers) < 6:
                il = random.randint(0, len(lotto_numbers_available)-1)
                lotto_numbers.append(lotto_numbers_available[il])
                del lotto_numbers_available[il]
            lotto_numbers_str = ""
            for l in lotto_numbers:
                lotto_numbers_str += str(l) + ","
            db.set("lotto_meta", "number", lotto_numbers_str[:-1])
            db.set("lotto_meta", "dt", str(dt.year) + "," + str(dt.month) + "," + str(dt.day-1))
            # gamemoney reset
            db.remove_section("gamemoney")
            db.add_section("gamemoney")
            db.remove_section("birthday_notification")
            db.add_section("birthday_notification")
            with open(db_path, 'w') as configfile:
                db.write(configfile)
            logger.info('dayjob sequence launched')
        # sleep cooldown
        dt = int(dt.timestamp())
        cd = db.items('j_sleep_cooldown')
        cd2 = db.items('guild_unlock')
        for i in cd:
            if int(i[1]) <= dt:
                db.remove_option('j_sleep_cooldown', i[0])
                with open(db_path, 'w') as configfile:
                    db.write(configfile)
        for i in cd2:
            if int(i[1]) <= dt:
                db.remove_option('guild_unlock', i[0])
                try:
                    db.remove_option('move_guild_pending', i[0])
                except:
                    pass
                if i[0] in db.get("etc", "reset_guild_pending"):
                    db.set("etc", "reset_guild_pending", db.get("etc", "reset_guild_pending").replace(", " + i[0], ""))
                with open(db_path, 'w') as configfile:
                    db.write(configfile)
        await asyncio.sleep(1)

@client.event
async def bgjob_change_playing():
    while True:
        members_sum = 0
        for s in client.guilds:
            members_sum += len(s.members)
        if test_glyph == "_":
            presences_list = ["루냥아 대신 루우냥아를 써주세요!", "v" + bot_ver, "이 메시지는 10초 마다 바뀌어요!"]
        else:
            presences_list = ["루냥아 도와줘 : 도움말", str(len(client.guilds)) + "개의 서버에서 귀여움받는 중", str(members_sum) + "명의 유저들에게 귀여움받는 중", "v" + bot_ver, "이 메시지는 10초 마다 바뀌어요!"]
        for v in presences_list:
            await asyncio.sleep(10)
            await client.change_presence(activity=discord.Game(v))
    client.loop.create_task(bgjob_change_playing())

@client.event
async def server_log(message, colorh, texth, desch = None, footh = None):
    try:
        cid = db.get("server_log", str(message.guild.id))
        cid = client.get_channel(int(cid))
        if cid != None:
            if desch == None:
                embed=discord.Embed(title=texth, color=colorh)
            else:
                embed=discord.Embed(title=texth, description=desch, color=colorh)
            if footh == None:
                embed.set_footer(text=message.author.name)
            else:
                embed.set_footer(text=footh)
            await cid.send(embed=embed)
        else:
            db.remove_option("server_log", str(message.guild.id))
        return True
    except:
        return False

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
    embed = discord.Embed(title=title_str, description=content, color=0xffccff)
    embed.set_thumbnail(url=client.user.avatar_url)
    if news_image != False:
        embed.set_image(url=news_image)
    embed.set_footer(text="작성자 : " + message.author.name, icon_url=message.author.avatar_url)
    cs = db.get("etc", "news_channel")
    for c in db.get("etc", "news_channel").split(", "):
        try:
            news_channel = client.get_channel(int(c))
            await news_channel.send(embed=embed)
            await message.channel.send(":green_square:" + news_channel.name + " at " + news_channel.guild.name + " (" + str(c) + ") : Success")
        except Exception as e:
            cs = cs.replace(c + ", ", "")
            await message.channel.send(str(c) + ":red_square: : Failed (" + str(e) + ")")
    db.set("etc", "news_channel", cs)
    await message.channel.send("Complete")

@client.event
async def on_ready():
    print('INFO    : Bot is ready to use.')
    print("INFO    : Account : " + str(client.user.name) + "(" + str(client.user.id) + ")")
#    client.loop.create_task(bgjob_change_playing())
    await client.change_presence(activity=discord.Game("루냥아 도와줘 → 도움말 | ver " + bot_ver))
    client.loop.create_task(user_count_reset())
    client.loop.create_task(job_scheduler())

@client.event
async def on_connect():
    print('INFO    : Connected to Discord.')

@client.event
async def on_message(message):
    try:
        global test_glyph, hash_str, news_str, news_title_str, article_title, article_content, comm_count, news_image
        # DM channel indicator
        try:
            if str(message.channel).startswith("Direct Message with "):
                dmchannel = True
            else:
                dmchannel = False
        except Exception as e:
            dmchannel = False
        # head pointer
        head_s = m_user.head(db, message)
        # admin indicator
        try:
            if str(message.author.id) in conf.get("config", "bot_owner") or message.author.guild_permissions.administrator:
                ifadmin = True
            else:
                ifadmin = False
        except:
            ifadmin = False
        # delete messages for volatile channel
        if not dmchannel:
            try:
                cnn = int(db.get("volatile_channel", str(message.channel.id)))
                cnt = 0
                async for mes in message.channel.history(limit=100):
                    cnt += 1
                if cnt > cnn:
                   await message.channel.purge(limit=cnt-cnn, oldest_first=True)
            except:
                pass
        # skip for herself, bots, command-denied channel
        if message.author == client.user:
            return
        elif message.author.bot:
            return
        elif message.content == head_s + "금지채널 삭제" and dmchannel == False and ifadmin:
            dst = db.get("etc", "denied_channel")
            if str(message.channel.id) in dst:
                dst = dst.replace(", " + str(message.channel.id), "")
                db.set("etc", "denied_channel", dst)
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "muted_channel_deleted"), color=0xffffff)
            else:
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "not_muted_channel"), color=0xff0000)
            await message.channel.send(embed=embed)
        elif str(message.channel.id) in db.get("etc", "denied_channel") and dmchannel == False and ifadmin == False:
            return
        # delete muted user's message, discord link in adblock channel
        if not dmchannel:
            try:
                m = db.get("user_mute", str(message.guild.id))
                if str(message.author.id) in m:
                    await message.delete()
                    return
            except:
                pass
            if str(message.channel.id) in db.get("etc", "adblock_channel") and ifadmin == False:
                if "discordapp.com/invite" in message.content or "discord.gg" in message.content:
                    await message.delete()
                    await message.channel.send(message.author.mention + m_lang.string(db, message.author.id, "ad_blocked"))
                    return
        # server count, server level passive
        if not dmchannel:
            try:
                scnt = int(db.get("server_count", str(message.guild.id)))
                if scnt != -1:
                    scnt += 1
                    db.set("server_count", str(message.guild.id), str(scnt))
            except:
                db.set("server_count", str(message.guild.id), "-1")
                scnt = -1
        # command count and passive
        if not dmchannel:
            if message.content.startswith('루냥아') or message.content.startswith('루냥이') or message.content.startswith('커냥이') or message.content.startswith('귀냥이') or message.content.startswith(head_s):
                m_user.increase(db, message.author)
                comm_count+= 1
                db.set("etc", "comm_count", str(int(db.get("etc", "comm_count")) + 1))
            elif scnt >= 70 and random.randint(1, 100) == 1 and test_glyph != "_":
                db.set("server_count", str(message.guild.id), "0")
                await message.channel.send(m_ext_commands.server_burning(db, message.guild.id))
            # ctclink routine
            cr0 = m_ctclink.get_link(message.channel.id, db)
            if cr0 != False and message.content.startswith(head_s) == False:
                cr = client.get_channel(int(cr0))
                if cr == None:
                    m_ctclink.remove_link(message.channel.id, db)
                else:
                    await cr.send(message.author.name + " : " + message.content)
            m_user.count(db, message.author)
            pst = db.get("etc", "passive_denied")
            if m_user.ret_check(db, message.author, test_glyph) >= 200 and m_user.check_count(db, message.author) >= 30 and random.randint(0, 10) == 1 and m_user.check_allow_sudden_hugging(db, message.author) == True and str(message.guild.id) in pst == False and test_glyph != "_":
                await message.channel.send(message.author.mention + " " + m_ext_commands.say_lv(message, db))
                if m_user.check_hug_count(db, message.author) <= 3:
                    embed = discord.Embed(title=m_lang.string(db, message.author.id, "user_passive_title"), description=m_lang.string(db, message.author.id, "user_passive_desc"))
                    await message.channel.send(embed=embed)
                m_user.hug_count(db, message.author)
                m_user.reset_count(db, message.author)
        # unsleep routine
        if m_user.check_sleep(db, message.author, message.guild) != None and dmchannel == False:
            embed=m_user.unsleep(db, message, datetime.now())
            try:
                sc = db.get("sleep_channel", str(message.guild.id))
                c = client.get_channel(int(sc))
            except:
                c = message.channel
            await c.send(message.author.mention, embed=embed)
        # notify mentioning user that sleeping
        if len(message.mentions) >= 1 and dmchannel == False:
            for mn in message.mentions:
                mb = m_user.check_sleep(db, mn, message.guild)
                if mb != None:
                    embed=discord.Embed(title=mn.name + m_lang.string(db, message.author.id, "is_sleeping"))
                    embed.add_field(name="잠수 시간", value=mb[1])
                    embed.add_field(name="사유", value=mb[0])
                    try:
                        sc = db.get("sleep_channel", str(message.guild.id))
                        c = client.get_channel(int(sc))
                    except:
                        c = message.channel
                    await c.send(message.author.mention, embed=embed)
        # birthday notification from dday
        try:
            bday = db.get("dday", str(message.author.id) + "_생일")
            do = datetime.strptime(bday, '%Y-%m-%d').date()
            dt = datetime.now().date()
            if do.day == dt.day and do.month == dt.month:
                ds = relativedelta(dt, do)
                try:
                    dbay_c = db.get("birthday_notification", str(message.author.id))
                except Exception as e:
                    st = m_lang.string(db, message.author.id, "happy_birthday").replace("{1}", message.author.name)
                    st = st.replace("{2}", str(ds.years + 1))
                    embed=discord.Embed(title=st)
                    try:
                        await message.channel.send(message.author.mention, embed=embed)
                        db.set("birthday_notification", str(message.author.id), "1")
                    except:
                        pass
            else:
                pass
        except:
            pass
        # namebase writting routine
        try:
            m_etc.set_name(message)
        except:
            pass
        # generic commands starts with head string
        if message.content.startswith(head_s) and message.content.endswith(' 도와줘'):
            embed = m_help.help(message.author, client, message.content, bot_ver, head_s, 0)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + '도와줘 '):
            embed = m_help.help(message.author, client, message.content, bot_ver, head_s, 1)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + '도움말 '):
            embed = m_help.help(message.author, client, message.content, bot_ver, head_s, 2)
            await message.channel.send(embed=embed)
        elif message.content == head_s + '도움말':
            embed = m_help.help(message.author, client, message.content, bot_ver, head_s, 2, True)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "공지사항 목록":
            await message.channel.send(embed=m_board.list())
        elif message.content.startswith(head_s + '공지사항'):
            i = message.content.replace(head_s + '공지사항', '')
            if i == "":
                embed = m_board.read(1, db, message.author.id)
            else:
                try:
                    ix = int(i.replace(' ', ''))
                    embed = m_board.read(ix, db, message.author.id)
                except:
                    embed=discord.Embed(title=m_lang.string(db, message.author.id, "undefined_article_num_title"), description = m_lang.string(db, message.author.id, "undefined_article_num_desc"), color=0xffff00)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "소스코드":
            await message.channel.send(embed=m_help.source_code())
        elif message.content == head_s + "누구니":
            await message.channel.send(embed=m_help.selfintro(client, bot_ver, message))
        elif message.content == head_s + "배고파":
            s = m_food.return_food()
            embed=discord.Embed(title=s, color=0xff7fff)
            embed.set_footer(text=m_lang.string(db, message.author.id, "food_footer"))
            await message.channel.send(embed=embed)
        elif message.content == '루냥이 귀여워' or message.content == '루냥이 커여워' or message.content == '귀냥이 루여워' or message.content == '커냥이 루여워':
            await message.channel.send(m_ext_commands.imcute(db, message.author, test_glyph))
        elif message.content == head_s + "놀아줘" or message.content == head_s + "심심해":
            await message.channel.send(embed=m_help.suggest_game(db, message.author.id))
        elif message.content == "와! 샌즈!":
            await message.channel.send(m_ext_commands.sans())
        elif message.content == head_s + "쓰담쓰담":
            await message.channel.send(embed=m_ext_commands.pat(db, message.author, test_glyph))
        elif message.content == head_s + "꼬옥":
            await message.channel.send(embed=m_ext_commands.hug())
        elif message.content == head_s + "부비부비":
            await message.channel.send(embed=m_ext_commands.cuddle())
        elif message.content == head_s + "쪽":
            await message.channel.send(embed=m_ext_commands.kiss())
        elif message.content.startswith(head_s + '섞어줘'):
            await message.channel.send(m_ext_commands.say_shuffle(message, head_s))
        elif message.content.startswith(head_s + '행운의숫자'):
            await message.channel.send(m_ext_commands.say_rint(message))
        elif message.content.startswith(head_s + '섯다'):
            if message.content == head_s + '섯다':
                embed=discord.Embed(title="사용 방법 : 루냥아 섯다 (0부터 9까지의 숫자) (0부터 9까지의 숫자)", color=0xff77ff)
            else:
                if m_user.gamemoney(db, message) < 10:
                    embed=discord.Embed(title=m_lang.string(db, message.author.id, "not_enough_gamemoney"), desctiption=m_lang.string(db, message.author.id, "not_enough_gamemoney_desc"))
                else:
                    m_user.gamemoney(db, message, -10)
                    embed=m_seotda.seotda(db, message, head_s)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + "로하이"):
            embed=m_seotda.lowhigh(db, message, head_s)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + '소개말'):
            if message.content == head_s + "소개말":
                embed=discord.Embed(title="사용 방법 : 루냥아 소개말 (소개문장)", color=0xffffff)
            else:
                bio_str = message.content.replace(head_s + "소개말 ", "")
                if len(bio_str) > 300:
                    await message.channel.send(m_lang.string(db, message.author.id, "bio_too_long"))
                else:
                    m_user.set_bio(db, message.author, bio_str)
                    await message.channel.send(m_lang.string(db, message.author.id, "bio_set"))
        elif message.content.startswith(head_s + '방명록 쓰기 '):
            if len(message.content.replace(head_s + "방명록 쓰기 ", "")) > 150:
                await message.channel.send(m_lang.string(db, message.author.id, "board_too_long"))
            else:
                m_board.gbook_write(message.content.replace(head_s + "방명록 쓰기 ", ""), message.author.id)
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "board_writed_title"), description=m_lang.string(db, message.author.id, "board_writed_desc"), color=0xffffff)
                await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + '방명록'):
            page = message.content.replace(head_s + "방명록 ", "")
            try:
                page = int(page)
            except:
                page = 1
            await message.channel.send(embed=m_board.gbook_view(page, db, message.author.id))
        elif message.content.startswith(head_s + "색상"):
            if message.content == head_s + "색상":
                embed=discord.Embed(title="사용 방법 : 루냥아 색상 (헥사코드)", description="예시 : 루냥아 색상 FFFFFF", color=0xffffff)
                await message.channel.send(embed=embed)
            else:
                try:
                    fn = m_etc.make_color(message.content, head_s, True)
                    await message.channel.send(file=discord.File(fn))
                    os.remove(fn)
                except ValueError:
                    embed=discord.Embed(title="사용 방법 : 루냥아 색상 (헥사코드)", description="예시 : 루냥아 색상 FFFFFF", color=0xffffff)
                    await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + "색상코드"):
            if message.content == head_s + "색상코드":
                embed=discord.Embed(title="사용 방법 : 루냥아 색상코드 (헥사코드)", description="예시 : 루냥아 색상코드 FFFFFF", color=0xffffff)
                await message.channel.send(embed=embed)
            else:
                try:
                    fn = m_etc.make_color(message.content, head_s, False)
                    await message.channel.send(file=discord.File(fn))
                    os.remove(fn)
                except ValueError:
                    embed=discord.Embed(title="사용 방법 : 루냥아 색상 (헥사코드)", description="예시 : 루냥아 색상 FFFFFF", color=0xffffff)
                    await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + '받아쓰기'):
            if message.content == head_s + '받아쓰기':
                embed=discord.Embed(title='사용 방법 : 루냥아 받아쓰기 (텍스트)', color=0xffffff)
                await message.channel.send(embed=embed)
            else:
                fn = m_etc.make_pil(message.content, head_s)
                await message.channel.send(file=discord.File(fn))
        elif message.content.startswith(head_s + '확성기 '):
            if str(message.guild.id) in db.get("permissions", "deny_megaphone"):
                await message.channel.send(m_lang.string(db, message.author.id, "sayd_denied"))
            else:
                mentioned_too_much = message.mentions
                if len(mentioned_too_much) > 3:
                    mentioned_too_much = True
                else:
                    mentioned_too_much = False
                if re.search(conf.get("string", "hatespeech"), message.content) or message.mention_everyone or "@here" in message.content or "<@&" in message.content or mentioned_too_much:
                    try:
                        await message.delete()
                    except:
                        pass
                    await message.channel.send(m_lang.string(db, message.author.id, "sayd_blocked"))
                else:
                    say_str = message.content
                    say_str = say_str.replace(head_s + '확성기 ','')
                    try:
                        await message.delete()
                    except:
                        pass
                    await message.channel.send(say_str)
                    log_available = await server_log(message, 0x00ffff, "확성기 기능을 사용함", message.author.name + " : " + say_str, "채널 : " + message.channel.name)
                    if str(message.guild.id) in db.get("etc", "mplog"):
                        mplog = True
                    else:
                        mplog = False
                    if log_available == False or mplog == True:
                        await message.channel.send("||작성자 : " + message.author.name + "||")
        elif message.content.startswith(head_s + "계산해줘 이미지 "):
            await message.channel.trigger_typing()
            bci_str = message.content
            bci_str = bci_str.replace(head_s + "계산해줘 이미지 ", "")
            await message.channel.send(message.author.mention, file=discord.File(m_wolframalpha.wa_img(conf, bci_str)))
            os.remove("wa_temp_img.gif")
        elif message.content.startswith(head_s + "캡챠 "):
            try:
                bc_str = message.content
                bc_str = bc_str.replace(head_s + "캡챠 ","")
                await message.channel.trigger_typing()
                await message.channel.send(file=discord.File(m_wolframalpha.captcha(conf, "captcha " + bc_str)))
                os.remove("wa_temp_img.gif")
            except:
                await message.channel.send(m_lang.string(db, message.author.id, "generic_error"))
        elif message.content.startswith(head_s + "계산해줘 "):
            try:
                bc_str = message.content
                bc_str = bc_str.replace(head_s + "계산해줘 ","")
                if bc_str == "":
                    await message.channel.send(m_lang.string(db, message.author.id, "insert_algebra"))
                elif bc_str == "1+1":
                    await message.channel.send("귀요미! 난 귀요미! :two_hearts:")
                else:
                    await message.channel.trigger_typing()
                    await message.channel.send(message.author.mention + "\n" + m_wolframalpha.wa_calc(bc_str))
            except:
                await message.channel.send(m_lang.string(db, message.author.id, "recheck_algebra"))
        elif message.content.startswith(head_s + "계산 "):
            try:
                bc_str = message.content
                bc_str = bc_str.replace(head_s + "계산 ","")
                if bc_str == "":
                    await message.channel.send(m_lang.string(db, message.author.id, "insert_algebra"))
                elif bc_str == "1+1":
                    await message.channel.send("귀요미! 난 귀요미! :two_hearts:")
                else:
                    await message.channel.trigger_typing()
                    await message.channel.send(message.author.mention + "\n" + m_wolframalpha.wa_calc(bc_str))
            except:
                await message.channel.send(m_lang.string(db, message.author.id, "recheck_algebra"))
        elif message.content.startswith(head_s + '골라줘 '):
            await message.channel.send(message.author.mention + ", **" + m_ext_commands.selectr(message.content, head_s) + m_lang.string(db, message.author.id, "selectr_tail"))
        elif message.content == head_s + "이용약관":
            await message.channel.send(embed=m_help.tos())
        elif message.content == head_s + "이용수칙":
            await message.channel.send(embed=m_help.rules())
        elif message.content == "루냥아":
            await message.channel.send(m_ext_commands.l_ping())
        elif message.content == head_s + "짖어":
            await message.channel.send(m_ext_commands.l_dog())
        elif message.content == head_s + "사랑해":
            await message.channel.send(m_ext_commands.l_lv(db, message.author, test_glyph))
        elif message.content == head_s + "출석체크" or message.content == head_s + "출첵":
            await message.channel.send(embed=m_user.attendance(db, message.author))
        elif message.content == head_s + "출석체크 초기화":
            db.set("attendance", str(message.author.id), "0")
            tod = db.get("attendance", "today")
            db.set("attendance", "today", tod.replace(", " + str(message.author.id), ""))
            await message.channel.send(m_lang.string(db, message.author.id, "attendance_count_reset"))
        elif message.content.startswith(head_s + '생일'):
            await message.channel.send(embed=m_help.bday())
        elif message.content == head_s + "주사위":
            await message.channel.send('(쫑긋) (데구르르) ' + m_ext_commands.l_dice() + '!')
        elif message.content.startswith(head_s + '제비뽑기 '):
            await message.channel.send(m_ext_commands.l_ticket(message, head_s, db))
        elif message.content == head_s + "나 어때":
            await message.channel.send(embed=m_user.check(db, message))
        elif message.content.startswith(head_s) and message.content.endswith(' 어때'):
            if message.content == head_s + "어때":
                await message.channel.send(m_lang.string(db, message.author.id, "plz_set_target"))
            else:
                res2 = m_user.guild_custom_commands(client, db, message, dmchannel)
                if res2 == None:
                    try:
                        await message.channel.send(embed=m_user.check_another(db, message.mentions[0], message))
                    except:
                        await message.channel.send(m_lang.string(db, message.author.id, "plz_set_target"))
                else:
                    await message.channel.send(res2)
        elif message.content.startswith(head_s + "계정정보"):
            if not message.mentions:
                await message.channel.send(embed=m_user.accountinfo(db, message.author, message, dmchannel))
            else:
                await message.channel.send(embed=m_user.accountinfo(db, message.mentions[0], message, dmchannel))
        elif message.content.startswith(head_s) and message.content.endswith(' 먹어'):
            await message.channel.send(embed=m_ext_commands.eat(message, head_s, db))
        elif message.content.startswith(head_s) and message.content.endswith(' 물어'):
            await message.channel.send(embed=m_ext_commands.bite(message, head_s, db))
        elif message.content == head_s + '배워':
            embed=discord.Embed(title="사용 방법", description="루냥아 배워 (명령어) | (반응)", color=0xffffff)
            embed.add_field(name="응용", value="(반응) && (반응2) & (반응3) .. : 다수 반응 중 랜덤 출현", inline=False)
            embed.add_field(name="이름 삽입", value="[멘션] : 명령어 사용자를 멘션\n[이름] : 명령어 사용자의 이름을 표시", inline=False)
            embed.add_field(name="커스텀 임베드 사용", value="임베드 [임베드 코드] : 명령어를 커스텀 임베드에 연결", inline=False)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + '배워 '):
            try:
                embed=m_user.make_custom_commands(db, message, dmchannel)
            except NameError:
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "no_such_custom_embed_title"), description=m_lang.string(db, message.author.id, "no_such_custom_embed_desc"))
            await message.channel.send(embed=embed)
        elif message.content == head_s + '제안':
            embed=discord.Embed(title="사용 방법", description="루냥아 제안 (제안할 기능)", color=0xffffff)
            embed.add_field(name="주의사항", value="제안 후 선정된 명령어는 모든 서버에서 사용됩니다\n부적절한 명령어를 제안하는 경우 이용 제재가 따를 수 있습니다", inline=False)
            await message.channel.send(embed=embed)
        elif message.content == head_s + '제안 목록':
            await message.channel.send(embed=m_user.list_suggests(db, message))
        elif message.content == head_s + '제안 삭제':
            await message.channel.send(embed=m_user.purge_suggests(db, message))
        elif message.content.startswith(head_s + '제안 '):
            await message.channel.send(embed=m_user.suggest_commands(db, message, datetime.now()))
        elif message.content == head_s + '음식제안':
            embed=discord.Embed(title="사용 방법", description="루냥아 음식제안 (간단한 설명)", color=0xffffff)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + '음식제안 '):
            await message.channel.send(embed=m_user.suggest_food(db, message, datetime.now()))
        elif message.content.startswith(head_s + '잊어 '):
            await message.channel.send(embed=m_user.remove_custom_commands(db, message, dmchannel))
        elif message.content.startswith(head_s + "배운거"):
            try:
                if message.content != head_s + "배운거":
                    m = message.content.replace(head_s + "배운거", "")
                    mn = int(m)
                await message.channel.send(embed=m_user.list_custom_commands(db, message, head_s, dmchannel))
            except:
                await message.channel.send(embed=m_user.info_custom_commands(db, message, dmchannel))
        elif message.content == head_s + "서버정보":
            await message.channel.send(embed=m_user.serverinfo(db, message))
        elif message.content == head_s + "서버설정":
            await message.channel.send(embed=m_user.serversettings(db, message, ifadmin))
        elif message.content.startswith(head_s + '거울'):
            if not message.mentions:
                mir_user = message.author
            else:
                mir_user = message.mentions[0]
            if mir_user.display_name == mir_user.name:
                usrname = mir_user.name + "#" + mir_user.discriminator
            else:
                usrname = mir_user.display_name + "(" + mir_user.name + "#" + mir_user.discriminator + ")"
            embed=discord.Embed(title=usrname + " 님의 프로필 사진", color=0xff77ff)
            embed.set_image(url=mir_user.avatar_url)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "성능":
            await message.channel.send(embed=m_help.get_info_public(str(datetime.now() - startTime), m_device.SERVER_NAME, bot_ver))
        elif message.content.startswith(head_s + '잠수') and message.content != head_s + "잠수 쿨타임" and message.content != head_s + "잠수금지" and message.content != head_s + "잠수채널" and not dmchannel:
            if str(message.guild.id) in db.get("permissions", "deny_sleep"):
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "sleep_denied"))
            if len(message.content.replace(head_s + "잠수 ", "")) >= 200:
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "sleep_too_long"))
            else:
                if "discord.gg" in message.content or "discord.com" in message.content or "discordapp.com" in message.content:
                    embed=discord.Embed(title="초대 코드를 사유로 잠수할 수 없습니다")
                else:
                    embed = m_user.sleep(db, message, datetime.now())
            try:
                sc = db.get("sleep_channel", str(message.guild.id))
                c = client.get_channel(int(sc))
            except:
                c = message.channel
            await c.send(message.author.mention, embed=embed)
        elif message.content == head_s + "관심 가져주기":
            res = m_user.toggle_sudden_hugging(db, message.author)
            if res == True:
                await message.channel.send(embed=discord.Embed(title=m_lang.string(db, message.author.id, "user_passive_on")))
            else:
                await message.channel.send(embed=discord.Embed(title=m_lang.string(db, message.author.id, "user_passive_off")))
        elif message.content.startswith(head_s + "관심 가져주기 커스텀"):
            if message.content == head_s + "관심 가져주기 커스텀":
                text = "루냥아 관심 가져주기 커스텀 (텍스트)\n\n' && '으로 구분해 랜덤 출현 목록을 만듭니다"
                embed=discord.Embed(title="사용 방법", description=text)
                await message.channel.send(embed=embed)
            else:
                m = message.content.replace(head_s + "관심 가져주기 커스텀 ", "")
                db.set("user_passive_custom", str(message.author.id), m)
                await message.channel.send(m_lang.string(db, message.author.id, "user_passive_customized"))
        elif message.content == head_s + "인기도":
            members_sum = 0
            for s in client.guilds:
                members_sum += len(s.members)
            #await message.channel.send(str(len(client.guilds)) + "개의 서버에서 " + str(members_sum) + "명에게 귀여움받는중 :two_hearts:")
            await message.channel.send(str(len(client.guilds)) + "개의 서버에서 귀여움받는중 :two_hearts:")
        elif message.content.startswith(head_s + '가위바위보'):
            if m_user.gamemoney(db, message) < 10:
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "not_enough_gamemoney"), desctiption=m_lang.string(db, message.author.id, "not_enough_gamemoney_desc"))
                await message.channel.send(embed=embed)
            else:
                m_user.gamemoney(db, message, -10)
                await message.channel.send(embed=m_rps.rps(message, head_s, message.author, db))
        elif message.content.startswith(head_s + "서버목록"):
            page = message.content.replace(head_s + "서버목록 ", "")
            try:
                page = int(page)
            except:
                page = 1
            await message.channel.send(embed=m_user.servers_list(client, page, db, message.author.id))
#        elif message.content.startswith(head_s + "서버랭킹"):
#            try:
#                page = int(message.content.replace(head_s + "서버랭킹 ", ""))
#            except:
#                page = 1
#            await message.channel.send(embed=m_user.servers_rank_users(client, db, page))
        elif message.content == head_s + "호감도랭킹":
            await message.channel.send(embed=m_user.level_rank(client, db))
        elif message.content.startswith(head_s + "닉변 "):
            nc = message.content.replace(head_s + "닉변 ", "")
            try:
                np = message.author.display_name
                await message.author.edit(nick=nc)
                embed=discord.Embed(title="닉네임 변경!", description=np + " >> " + nc, color=0xff77ff)
                await server_log(message, 0xff77ff, message.author.name + "이(가) 닉네임을 변경함", np + " >> " + nc)
            except Exception as e:
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "generic_error"), description=m_lang.string(db, message.author.id, "changenick_error"), color=0xff0000)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "핑":
            pb = time.monotonic()
            await message.channel.send(":ping_pong: 퐁!")
            ping = (time.monotonic() - pb) * 1000
            await message.channel.send("응답 시간 : " + str(int(ping)) + "ms")
        elif message.content == head_s + "가입일시공개":
            jnd = db.get("etc", "joinedat_nduser")
            if str(message.author.id) in jnd:
                jnd = jnd.replace(", " + str(message.author.id), "")
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "ndjoined_user_activated"), color=0xffffff)
            else:
                jnd = jnd + ", " + str(message.author.id)
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "ndjoined_user_deactivated"), color=0xffffff)
            db.set("etc", "joinedat_nduser", jnd)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "생성일시공개":
            cnd = db.get("etc", "createdat_nd")
            if str(message.author.id) in cnd:
                cnd = cnd.replace(", " + str(message.author.id), "")
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "ndcreated_activated"), color=0xffffff)
            else:
                cnd = cnd + ", " + str(message.author.id)
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "ndcreated_deactivated"), color=0xffffff)
            db.set("etc", "createdat_nd", cnd)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "테스트기능" and test_glyph == "_":
            await message.channel.send(embed=m_help.test_features(db, bot_ver))
        elif message.content.startswith(head_s + "문의 "):
            call_s = message.content.replace(head_s + "문의 ", "")
            s = message.author.name + "(" + str(message.author.id) + ")\n" + call_s
            u = await client.fetch_user(int(conf.get("config", "bot_owner")))
            await u.send(s)
        elif message.content == head_s + "서버아이콘":
            await message.channel.send(message.guild.icon_url)
        elif message.content.startswith(head_s + "메모 목록"):
            await message.channel.send(embed=m_board.memo_view(message, head_s, db))
        elif message.content.startswith(head_s + "메모 삭제 "):
            await message.channel.send(embed=m_board.memo_remove(message, head_s, db))
        elif message.content.startswith(head_s + "메모 "):
            await message.channel.send(embed=m_board.memo_write(message, head_s, db))
        elif message.content.startswith(head_s + "짤"):
            await message.channel.trigger_typing()
            await message.channel.send(embed=m_ext_commands.neko(message, head_s))
        elif message.content.startswith(head_s + "야짤") and message.content != head_s + "야짤채널":
            if str(message.channel.id) in db.get("etc", "nsfw_channel"):
                if str(message.guild.id) in db.get("moderation", "ban_nsfw"):
                    embed=discord.Embed(title="사용할 수 없는 기능입니다")
                    await message.channel.send(embed=embed)
                elif message.channel.is_nsfw():
                    await message.channel.trigger_typing()
                    await message.channel.send(embed=m_ext_commands.nsfw_neko(message, head_s))
                else:
                    embed=discord.Embed(title="채널을 후방 주의로 설정해주십시오.")
                    await message.channel.send(embed=embed)
#            ! 一部のギルドでの要請による措置 !
#            ! 보안 상 비활성화됨 !
#            else:
#                embed=discord.Embed(title=m_lang.string(db, message.author.id, "nsfw_neko_blocked_title"), description=m_lang.string(db, message.author.id, "contact_to_server_admin"), color=0xff0000)
#                await message.channel.send(embed=embed)
        elif message.content == head_s + "반모":
            if m_lang.check_lang(db, message.author.id) == "한국어(기본)":
                db.set("lang", str(message.author.id), "ban")
                await message.channel.send("이제 반말로 대화할게!\n일부 명령어는 반말을 사용하지 않아!")
            elif m_lang.check_lang(db, message.author.id) == "한국어(반말모드)":
                db.set("lang", str(message.author.id), "default")
                await message.channel.send("이제 존댓말로 대화할게요!")
        elif message.content == head_s + "로또":
            embed=discord.Embed(title="로또 이용 방법")
            embed.add_field(name="명령어", value="루냥아 로또 (1~45 사이의 숫자 6개)", inline=False)
            embed.add_field(name="규칙", value="매일 0시에 갱신되는 로또 번호와 응모한 로또 번호가 몇 개나 동일한 지에 따라 등수가 정해집니다\n1등 : 4개 이상\n2등 : 3개\n3등 : 2개", inline=False)
            embed.add_field(name="결과 확인", value='루냥아 로또 결과', inline=False)
            embed.add_field(name="주의사항", value="같은 번호를 반복 응모할 수 없습니다")
            await message.channel.send(embed=embed)
        elif message.content == head_s + "로또 결과":
            await message.channel.send(embed=m_user.get_lotto(db, message, datetime.now(), db.get("lotto_meta", "number"), db.get("lotto_meta", "dt")))
        elif message.content == head_s + "로또 자동":
            await message.channel.send(embed=m_user.autolotto(db, message, datetime.now()))
        elif message.content.startswith(head_s + "로또"):
            await message.channel.send(embed=m_user.set_lotto_number(db, message, datetime.now()))
        elif message.content == head_s + "무트코인":
            await message.channel.send(embed=m_ext_commands.turnipcalc())
        elif message.content == head_s + "원신가챠":
            await message.channel.send(embed=m_ext_commands.genshingacha())
        elif message.content.startswith(head_s + "검색"):
            await message.channel.send(embed=m_ext_commands.search_url(message, head_s))
        elif message.content.startswith(head_s + "유저 접두어"):
            if message.content == head_s + "유저 접두어":
                embed=discord.Embed(title="사용 방법 : 루냥아 유저 접두어 (접두어)")
            else:
                hst = message.content.replace(head_s + "유저 접두어 ", "")
                db.set("user_custom_head", str(message.author.id), hst)
                embed=discord.Embed(title='유저 지정 접두어가 "' + hst + m_lang.string(db, message.author.id, "custom_head_set_title"), description=m_lang.string(db, message.author.id, "custom_head_set_desc"), color=0xffffff)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "임베드":
            embed=discord.Embed(title="커스텀 임베드 사용 방법")
            embed.add_field(name="루냥아 임베드 제목 (제목)", value="임베디의 제목을 설정합니다", inline=False)
            embed.add_field(name="루냥아 임베드 개요 (개요)", value="임베드의 개요를 설정합니다", inline=False)
            embed.add_field(name="루냥아 임베드 내용추가 (이름) | (설명)", value="임베드에 내용을 추가합니다", inline=False)
            embed.add_field(name="루냥아 임베드 초기화", value="임시저장된 임베드를 삭제합니다", inline=False)
            embed.add_field(name="루냥아 임베드 미리보기 (코드)", value="저장된 임베드를 확인할 수 있습니다\n코드를 지정하지 않은 경우 임시보관된 임베드를 미리 볼 수 있습니다", inline=False)
            embed.add_field(name="루냥아 임베드 저장", value="임시 보관된 임베드를 저장소에 저장하고 코드를 생성합니다", inline=False)
            embed.add_field(name="루냥아 임베드 목록", value="저장된 커스텀 임베드를 확인할 수 있습니다", inline=False)
            embed.add_field(name="루냥아 임베드 예제", value="커스텀 임베드의 예제를 보여줍니다", inline=False)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + "임베드 제목"):
            if message.content == head_s + "임베드 제목":
                embed=discord.Embed(title="사용 방법 : 루냥아 임베드 제목 (제목)")
            else:
                m_custom_embed.set_title(message, head_s, db)
                em = m_custom_embed.get_embed_raw(message, db, None)
                embed = m_custom_embed.convert_to_embed(message, em)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + "임베드 개요"):
            if message.content == head_s + "임베드 개요":
                embed=discord.Embed(title="사용 방법 : 루냥아 임베드 개요 (개요)")
            else:
                m_custom_embed.set_desc(message, head_s, db)
                em = m_custom_embed.get_embed_raw(message, db, None)
                embed = m_custom_embed.convert_to_embed(message, em)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + "임베드 내용추가"):
            if message.content == head_s + "임베드 내용추가":
                embed=discord.Embed(title="사용 방법 : 루냥아 임베드 내용추가 (이름) (설명)")
            else:
                m_custom_embed.add_content(message, head_s, db)
                em = m_custom_embed.get_embed_raw(message, db, None)
                embed = m_custom_embed.convert_to_embed(message, em)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + "임베드 미리보기"):
            try:
                if message.content == head_s + "임베드 미리보기":
                    em = m_custom_embed.get_embed_raw(message, db, None)
                else:
                    m = str(message.author.id) + "_" + message.content.replace(head_s + "임베드 미리보기 ", "")
                    em = m_custom_embed.get_embed_raw(message, db, m)
                embed = m_custom_embed.convert_to_embed(message, em)
            except:
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "no_such_custom_embed_title"), description=m_lang.string(db, message.author.id, "no_such_custom_embed_desc"))
            await message.channel.send(embed=embed)
        elif message.content == head_s + "임베드 초기화":
            m_custom_embed.purge_nvram(message, db)
            await message.channel.send(m_lang.string(db, message.author.id, "custom_embed_reset"))
        elif message.content == head_s + "임베드 저장":
            container = m_custom_embed.get_embed_raw(message, db, None)
            code = m_custom_embed.commit_embed(message, db, container, False)
            m_custom_embed.purge_nvram(message, db)
            embed=discord.Embed(title=m_lang.string(db, message.author.id, "custom_embed_saved"), description="임베드 코드 : " + code)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + "임베드 목록"):
            await message.channel.send(embed=m_custom_embed.list_embeds(message, head_s, db))
        elif message.content == head_s + "임베드 예제":
            embed=discord.Embed(title="루냥아 임베드 제목 (제목)", description="루냥아 임베드 개요 (텍스트)")
            embed.add_field(name="루냥아 임베드 내용추가 (A) (B) 중 A에 해당", value="루냥아 임베드 내용추가 (A) (B) 중 B에 해당", inline=False)
            embed.add_field(name="여러 내용을 추가할 수 있습니다", value="내용은 한 줄에 하나씩 표시됩니다", inline=False)
            embed.add_field(name="응용", value="' && '을 붙여 랜덤 출현 목록을 만들 수 있습니다", inline=False)
            embed.set_footer(text="이 구역은 임베드 작성자명으로 고정됩니다")
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + "포스트 작성"):
            await message.channel.send(embed=m_user.write_posts(db, message, head_s))
        elif message.content.startswith(head_s + "포스트 목록"):
            await message.channel.send(embed=m_user.list_posts(db, message, head_s))
        elif message.content.startswith(head_s + "포스트 검색"):
            await message.channel.send(embed=m_user.search_posts(db, message, head_s))
        elif message.content.startswith(head_s + "포스트 "):
            await message.channel.send(embed=m_user.view_posts(db, message, head_s))
        elif message.content.startswith(head_s + "수정노기 설정"):
            await message.channel.send(embed=m_mabinogi.settings(db, message, head_s))
        elif message.content.startswith(head_s + "수정노기"):
            await message.channel.trigger_typing()
            res=m_mabinogi.do_sujeong(db, message, head_s)
            await message.channel.send(embed=res[0])
            if res[1]:
                await message.channel.send(file=discord.File("sujeong.txt"))
            try:
                os.remove("sujeong.txt")
            except:
                pass
        elif message.content == head_s + "수능":
            date_format = "%Y-%m-%d"
            d = db.get("etc", "ksat_date")
            a = datetime.strptime(d, date_format)
            b = datetime.now()
            delta = b - a
            m = m_lang.string(db, message.author.id, "ksat_left").replace("{1}", str(delta.days)[1:])
            await message.channel.send(m)
        elif message.content.startswith(head_s + "디데이 추가"):
            await message.channel.send(embed=m_user.dday_add(db, message, head_s))
        elif message.content.startswith(head_s + "디데이 삭제"):
            await message.channel.send(embed=m_user.dday_del(db, message, head_s))
        elif message.content.startswith(head_s + "디데이"):
            await message.channel.send(embed=m_user.dday_list(db, message, head_s))
        elif message.content.startswith(head_s + "소유권이전"):
            try:
                await message.guild.edit(owner=message.author)
                await message.channel.send(m_lang.string(db, message.author.id, "successfully_set"))
            except:
                pass
        # admin only functions
        elif message.content == head_s + 'raise_test' and str(message.author.id) in conf.get("config", "bot_owner"):
            raise
        elif message.content.startswith(head_s + 'shellcmd ') and str(message.author.id) in conf.get("config", "bot_owner"):
            shl_str = message.content
            shl_str = shl_str.replace(head_s + 'shellcmd ','')
            try:
                shl_res = str(os.popen(shl_str).read())
                if len(shl_res) >= 1000:
                    pf = open("command_result.txt", "w")
                    ps = "bash command : " + shl_str + "\r\n-----\r\n" + shl_res
                    pf.write(ps)
                    pf.close()
                    await message.channel.send("length of result is over 1000. here is text file of result", file=discord.File("command_result.txt"))
                else:
                    if shl_res == "":
                        shl_res = "no stdout or stderr."
                    await message.channel.send("```" + shl_res + "```")
            except Exception as e:
                await message.channel.send(":facepalm:" + str(e))
        elif message.content == head_s + "list_servers" and str(message.author.id) in conf.get("config", "bot_owner"):
            ps = "--servers list--"
            pf = open("servers_list.txt", "w")
            for s in client.guilds:
                ps += "\n" + s.name + " | " + str(s.id)
            pf.write(ps)
            pf.close()
            await message.channel.send(file=discord.File("servers_list.txt"))
        elif message.content.startswith(head_s + 'leave_server ') and str(message.author.id) in conf.get("config", "bot_owner"):
            lv_str = message.content
            lv_str = lv_str.replace(head_s + 'leave_server ','')
            g = await client.fetch_guild(int(lv_str))
            await g.leave()
            await message.channel.send("leaved from " + g.name)
        elif message.content.startswith(head_s + 'ban_nsfw ') and str(message.author.id) in conf.get("config", "bot_owner"):
            nb_str = message.content
            nb_str = nb_str.replace(head_s + 'ban_nsfw ','')
            db.set("moderation", "ban_nsfw", db.get("moderation", "ban_nsfw") + ", " + nb_str)
            await message.channel.send(":ok_hand:")
        elif message.content == head_s + "stringtest" and str(message.author.id) in conf.get("config", "bot_owner"):
            await message.channel.send(m_lang.string(db, message.author.id, "foo"))
        elif message.content == head_s + "exceptiontest" and str(message.author.id) in conf.get("config", "bot_owner"):
            fuck = fuck
        elif message.content.startswith(head_s + "debug message ") and str(message.author.id) in conf.get("config", "bot_owner"):
            mid = message.content.replace(head_s + "debug message ", "")
            mid = mid.split(" ")
            if len(mid) == 1:
                l = await message.channel.fetch_message(int(mid[0]))
            if len(mid) == 2:
                c = client.get_channel(int(mid[0]))
                l = await c.fetch_message(int(mid[1]))
            embed=discord.Embed(title="debug info of past message", description="message id : " + str(l.id), color=0xffffff)
            embed.add_field(name="guild", value="```" + l.guild.name + " (" + str(l.guild.id) + ")" + "```", inline=False)
            embed.add_field(name="channel", value="```" + l.channel.name + " (" + str(l.channel.id) + ")" + "```", inline=False)
            embed.add_field(name="author", value="```" + l.author.name + "(" + str(l.id) + ")" + "```", inline=False)
            if l.content == "" or l.content == None:
                lc = "None"
            else:
                lc = l.content
            embed.add_field(name="content", value=lc, inline=False)
            embed.add_field(name="content in raw value", value="```" + lc + "```", inline=False)
            embed.add_field(name="message channel", value="```" + l.channel.name + "(" + str(l.channel.id) + ")" + "```", inline=False)
            embed.add_field(name="mentions everyone", value="```" + str(l.mention_everyone) + "```", inline=False)
            embed.add_field(name="created at", value="```" + str(l.created_at) + "```", inline=False)
            embed.add_field(name="edited at", value="```" + str(l.edited_at) + "```", inline=False)
            embed.add_field(name="jump url", value="[" + l.jump_url + "](" + l.jump_url + ")", inline=False)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + "debug channel text ") and str(message.author.id) in conf.get("config", "bot_owner"):
            mid = message.content.replace(head_s + "debug channel text ", "")
            l = client.get_channel(int(mid))
            embed=discord.Embed(title="debug info of text channel", description="channel id : " + str(l.id), color=0xffffff)
            embed.add_field(name="name", value="```" + l.name + "```", inline=False)
            embed.add_field(name="guild", value="```" + l.guild.name + " (" + str(l.guild.id) + ")" + "```", inline=False)
            try:
                embed.add_field(name="category", value="```" + l.category.name + " (" + str(l.category.id) + ")" + "```", inline=False)
            except:
                embed.add_field(name="category", value="```None```", inline=False)
            embed.add_field(name="created at", value="```" + str(l.created_at) + "```", inline=False)
            embed.add_field(name="slowmode delay", value="```" + str(l.slowmode_delay) + "```", inline=False)
            embed.add_field(name="is NSFW", value="```" + str(l.is_nsfw()) + "```", inline=False)
            embed.add_field(name="is News", value="```" + str(l.is_news()) + "```", inline=False)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + "debug channel voice ") and str(message.author.id) in conf.get("config", "bot_owner"):
            mid = message.content.replace(head_s + "debug channel voice ", "")
            l = client.get_channel(int(mid))
            embed=discord.Embed(title="debug info of voice channel", description="channel id : " + str(l.id), color=0xffffff)
            embed.add_field(name="name", value="```" + l.name + "```", inline=False)
            embed.add_field(name="guild", value="```" + l.guild.name + " (" + str(l.guild.id) + ")" + "```", inline=False)
            try:
                embed.add_field(name="category", value="```" + l.category.name + " (" + str(l.category.id) + ")" + "```", inline=False)
            except:
                embed.add_field(name="category", value="```None```", inline=False)
            embed.add_field(name="created at", value="```" + str(l.created_at) + "```", inline=False)
            embed.add_field(name="user limit", value="```" + str(l.user_limit) + "```", inline=False)
            embed.add_field(name="bitrate", value="```" + str(l.bitrate) + "```", inline=False)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + 'db pick item ') and str(message.author.id) in conf.get("config", "bot_owner"):
            m = message.content.replace(head_s + 'db pick item ', '')
            m = m.split(' ')
            embed=discord.Embed(title="Key " + m[1] + " in section " + m[0], color=0xffffff)
            try:
                i = db.get(m[0], m[1])
                if m[1] == "" or m[1] == None:
                    embed=discord.Embed(title="Value of Key " + m[1] + " in section is empty." + m[0], color=0xffffff)
                else:
                    embed.add_field(name="value", value=i, inline=False)
            except Exception as e:
                embed.add_field(name="error string", value=str(e), inline=False)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + 'db poke item ') and str(message.author.id) in conf.get("config", "bot_owner"):
            m = message.content.replace(head_s + 'db poke item ', '')
            m = m.split(' ')
            embed=discord.Embed(title="Key " + m[1] + " in section " + m[0], color=0xffffff)
            v = message.content.replace(head_s + 'db poke item ' + m[0] + ' ' + m[1] + ' ', '')
            db.set(m[0], m[1], v)
            embed.add_field(name="value", value=v, inline=False)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + 'db pick section ') and str(message.author.id) in conf.get("config", "bot_owner"):
            m = message.content.replace(head_s + 'db pick section ', '')
            v = db.items(m)
            embed=discord.Embed(title="Section " + m, description=str(v), color=0xffffff)
            await message.channel.send(embed=embed)
        elif message.content == head_s + 'db pick sections' and str(message.author.id) in conf.get("config", "bot_owner"):
            v = db.sections()
            embed=discord.Embed(title="DB sections list ", description=str(v), color=0xffffff)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + 'news set_content ') and str(message.author.id) in conf.get("config", "bot_owner"):
            news_str = message.content
            news_str = news_str.replace(head_s + 'news set_content ', '')
            news_str = news_str.replace("&nbsp", "\n")
            embed = discord.Embed(title=news_title_str, description=news_str, color=0xffccff)
            embed.set_thumbnail(url=client.user.avatar_url)
            if news_image != False:
                embed.set_image(url=news_image)
            await message.channel.send(embed=embed)
            if news_title_str != "기계식 루냥이 공지":
                await message.channel.send(":warning: custom embed title was set : " + news_title_str)
        elif message.content.startswith(head_s + 'news set_title ') and str(message.author.id) in conf.get("config", "bot_owner"):
            news_title_str = message.content
            news_title_str = news_title_str.replace(head_s + 'news set_title ', '')
            news_title_str = news_title_str.replace("&nbsp", "\n")
            embed = discord.Embed(title=news_title_str, description=news_str, color=0xffccff)
            if news_image != False:
                embed.set_image(url=news_image)
            embed.set_thumbnail(url=client.user.avatar_url)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + 'news set_image ') and str(message.author.id) in conf.get("config", "bot_owner"):
            news_image = message.content.replace(head_s + "news set_image ", "")
            embed = discord.Embed(title=news_title_str, description=news_str, color=0xffccff)
            embed.set_image(url=news_image)
            embed.set_thumbnail(url=client.user.avatar_url)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "news clear_image" and str(message.author.id) in conf.get("config", "bot_owner"):
            news_image = False
        elif message.content == head_s + "news send" and str(message.author.id) in conf.get("config", "bot_owner"):
            await news_send(message, news_title_str, news_str)
        elif message.content.startswith(head_s + 'news send_specific ') and str(message.author.id) in conf.get("config", "bot_owner"):
            channel_str = message.content
            channel_str = channel_str.replace(head_s + 'news send_specific ', '')
            try:
                news_channel = client.get_channel(int(channel_str))
                embed = discord.Embed(title=news_title_str, description=news_str, color=0xffccff)
                embed.set_thumbnail(url=client.user.avatar_url)
                if news_image != False:
                    embed.set_image(url=news_image)
                embed.set_footer(text="작성자 : " + message.author.name, icon_url=message.author.avatar_url)
                await news_channel.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(title="Exception occured", description=str(e), color=0xff0000)
                await message.channel.send(embed=embed)
        elif message.content == head_s + "news preview" and str(message.author.id) in conf.get("config", "bot_owner"):
            embed = discord.Embed(title=news_title_str, description=news_str, color=0xffccff)
            embed.set_thumbnail(url=client.user.avatar_url)
            if news_image != False:
                embed.set_image(url=news_image)
            embed.set_footer(text="작성자 : " + message.author.name, icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "getinfo" and str(message.author.id) in conf.get("config", "bot_owner"):
            process = psutil.Process(os.getpid())
            upt = datetime.now() - startTime
            users = 0
            for s in client.guilds:
                users += len(s.members)
            await message.channel.send(embed=m_help.get_info(client, str(upt), client.user.id, hash_str, process.memory_info().rss, comm_count, db.get("etc", "comm_count"), bot_ver, str(len(client.guilds)), users, process))
        elif message.content == head_s + "suicide" and str(message.author.id) in conf.get("config", "bot_owner"):
            await message.channel.send("suiciding..")
            raise SystemExit
        elif message.content == head_s + "reboot" and str(message.author.id) in conf.get("config", "bot_owner"):
            await message.channel.send("rebooting..")
            raise Exception("rebootme")
        elif message.content.startswith(head_s + 'article set_title ') and str(message.author.id) in conf.get("config", "bot_owner"):
            article_title = message.content.replace(head_s + "article set_title ", "")
        elif message.content.startswith(head_s + 'article set_content ') and str(message.author.id) in conf.get("config", "bot_owner"):
            article_content = message.content.replace(head_s + "article set_content ", "")
        elif message.content == head_s + "article preview" and str(message.author.id) in conf.get("config", "bot_owner"):
            embed = discord.Embed(title=article_title, description=article_content, color=0xffffff)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "article write" and str(message.author.id) in conf.get("config", "bot_owner"):
            m_board.write(article_title, article_content)
            await message.channel.send(":ok_hand:")
        elif message.content.startswith(head_s + "article amend") and str(message.author.id) in conf.get("config", "bot_owner"):
            no = message.content.replace(head_s + "article amend ", "")
            m_board.amend(no, article_title, article_content)
            await message.channel.send(":ok_hand:")
        elif message.content == head_s + "article notify" and str(message.author.id) in conf.get("config", "bot_owner"):
            await news_send(message, "새 공지사항 : " + article_title, '"루냥아 공지사항"으로 볼 수 있습니다')
        elif message.content == head_s + "article clear" and str(message.author.id) in conf.get("config", "bot_owner"):
            m_board.clear()
        elif message.content == head_s + "attendance reset" and str(message.author.id) in conf.get("config", "bot_owner"):
            db.set("attendance", "today", "0")
        elif message.content.startswith(head_s + 'attendance set') and str(message.author.id) in conf.get("config", "bot_owner"):
            ats = message.content.replace(head_s + "attendance set ", "")
            ats = ats.split(" ")
            db.set("attendance", ats[0], ats[1])
        elif message.content.startswith(head_s + 'user level change ') and str(message.author.id) in conf.get("config", "bot_owner"):
            try:
                lc = message.content.replace(head_s + "user level change ", "")
                lc = lc.split(" ")
                db.set("user_level", lc[0], lc[1])
                await message.channel.send("user level of " + lc[0] + " was changed to " + lc[1])
                us = await client.fetch_user(int(lc[0]))
                await message.channel.send(embed=m_user.check_another(db, us, message))
            except Exception as e:
                await message.channel.send(str(e))
        elif message.content.startswith(head_s + 'user tropy set ') and str(message.author.id) in conf.get("config", "bot_owner"):
            try:
                lc = message.content.replace(head_s + "user tropy set ", "")
                lc = lc.split(" ")
                lc2 = lc[1:]
                lc3 = ""
                for i in lc2:
                    lc3 += i + " "
                db.set("user_tropy", lc[0], lc3)
                await message.channel.send("user level of " + lc[0] + " was changed to " + lc3)
                us = await client.fetch_user(int(lc[0]))
                await message.channel.send(embed=m_user.check_another(db, us, message))
            except Exception as e:
                await message.channel.send(str(e))
        elif message.content.startswith(head_s + 'user inspect '): # 편의상 일반 유저들에게도 사용 가능하도록 설정
            lc = message.content.replace(head_s + "user inspect ", "")
            u = await client.fetch_user(int(lc))
            embed=discord.Embed(title="user inspection of " + lc)
            embed.set_thumbnail(url=u.avatar_url)
            embed.add_field(name="Name", value=u.name)
            embed.add_field(name="UID", value=str(u.id))
            embed.add_field(name="Account created at", value=u.created_at.isoformat())
            embed.add_field(name="is Bot", value=str(u.bot))
            embed.add_field(name="is system", value=str(u.system))
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + 'exec ') and str(message.author.id) in conf.get("config", "bot_owner"):
            exec(message.content.replace(head_s + "exec ", ""))
        elif message.content.startswith(head_s + 'awaitexec ') and str(message.author.id) in conf.get("config", "bot_owner"):
            await exec(message.content.replace(head_s + "awaitexec ", ""))
        elif message.content.startswith(head_s + 'say ') and str(message.author.id) in conf.get("config", "bot_owner"):
            m = message.content.replace(head_s + 'say ', '')
            mc = m.split(" ")[0]
            mx = m.split(" ")[1:]
            mm = ""
            for mxi in mx:
                mm = mm + mxi + " "
            c = client.get_channel(int(mc))
            await c.send(mm)
            await message.channel.send(c.name + "(" + str(c.id) + ") in " + c.guild.name + "(" + str(c.guild.id) + ")\n" + mm)
        elif message.content == head_s + 'generate_guildcode' and str(message.author.id) in conf.get("config", "bot_owner"):
            try:
                for s in client.guilds:
                    m_servercode.generate_code(s, db, False)
                await message.channel.send(":ok_hand:")
            except Exception as e:
                await message.channel.send(str(e))
        elif message.content.startswith(head_s + 'get_guildcode ') and str(message.author.id) in conf.get("config", "bot_owner"):
            lc = message.content.replace(head_s + "get_guildcode ", "")
            gid = m_servercode.get_guild(lc, db)
            await message.channel.send(gid)
        elif message.content == "db_cleanup" and str(message.author.id) in conf.get("config", "bot_owner"):
            await message.channel.send("see the progress in terminal.")
            # Progress will seen in Terminal
            # DO NOT ERASE THESE PRINTS
            print("DB Cleanup Sequence\n-----")
            dt = datetime.now()
            dt = str(int(dt.timestamp()))
            shutil.copy2("db/db.dat", "db_backups/db_before_cleanup_" + dt + ".bak")
            print("db backed up")
            print("cleaning up user level")
            ul = db.items("user_level")
            n = 1
            f = 0
            for i in ul:
                try:
                    client.get_user(int(i[0]))
                    print(str(n) + "/" + str(len(ul)) + " : user '" + i[0] + "'. looks good.")
                except:
                    db.remove_option("user_level", i[0])
                    print(str(n) + "/" + str(len(ul)) + " : Failed to get user '" + i[0] + "'. removing.")
                    f += 1
                n += 1
            print("cleaning up hug count")
            ul = db.items("hug_count")
            n = 1
            for i in ul:
                try:
                    client.get_user(int(i[0]))
                    print(str(n) + "/" + str(len(ul)) + " : user '" + i[0] + "'. looks good.")
                except:
                    db.remove_option("hug_count", i[0])
                    print(str(n) + "/" + str(len(ul)) + " : Failed to get user '" + i[0] + "'. removing.")
                    f += 1
                n += 1
            print("cleaning up bio")
            ul = db.items("bio")
            n = 1
            for i in ul:
                try:
                    client.get_user(int(i[0]))
                    print(str(n) + "/" + str(len(ul)) + " : user '" + i[0] + "'. looks good.")
                except:
                    db.remove_option("bio", i[0])
                    print(str(n) + "/" + str(len(ul)) + " : Failed to get user '" + i[0] + "'. removing.")
                    f += 1
                n += 1
            print("cleaning up lang")
            ul = db.items("lang")
            n = 1
            for i in ul:
                try:
                    client.get_user(int(i[0]))
                    print(str(n) + "/" + str(len(ul)) + " : user '" + i[0] + "'. looks good.")
                except:
                    db.remove_option("lang", i[0])
                    print(str(n) + "/" + str(len(ul)) + " : Failed to get user '" + i[0] + "'. removing.")
                    f += 1
                n += 1
            print("cleaning up guild_intro")
            ul = db.items("guild_intro")
            n = 1
            for i in ul:
                try:
                    client.get_guild(int(i[0]))
                    print(str(n) + "/" + str(len(ul)) + " : guild '" + i[0] + "'. looks good.")
                except:
                    db.remove_option("guild_intro", i[0])
                    print(str(n) + "/" + str(len(ul)) + " : Failed to get guild '" + i[0] + "'. removing.")
                    f += 1
                n += 1
            print("cleaning up tropy")
            ul = db.items("user_tropy")
            n = 1
            for i in ul:
                try:
                    client.get_user(int(i[0]))
                    print(str(n) + "/" + str(len(ul)) + " : user '" + i[0] + "'. looks good.")
                except:
                    db.remove_option("user_tropy", i[0])
                    print(str(n) + "/" + str(len(ul)) + " : Failed to get user '" + i[0] + "'. removing.")
                    f += 1
                n += 1
            print("cleaning up attendance")
            ul = db.items("attendance")
            n = 1
            for i in ul:
                if i[0] == "today":
                    pass
                else:
                    try:
                        client.get_user(int(i[0]))
                        print(str(n) + "/" + str(len(ul)) + " : user '" + i[0] + "'. looks good.")
                    except:
                        db.remove_option("attendance", i[0])
                        print(str(n) + "/" + str(len(ul)) + " : Failed to get user '" + i[0] + "'. removing.")
                        f += 1
                    n += 1
            print("cleaning up user_mute")
            ul = db.items("user_mute")
            n = 1
            for i in ul:
                try:
                    client.get_guild(int(i[0]))
                    print(str(n) + "/" + str(len(ul)) + " : guild '" + i[0] + "'. looks good.")
                except:
                    db.remove_option("user_mute", i[0])
                    print(str(n) + "/" + str(len(ul)) + " : Failed to get guild '" + i[0] + "'. removing.")
                    f += 1
                n += 1
            print("cleaning up custom commands")
            ul = db.items("custom_commands")
            n = 1
            for i in ul:
                ix = i[0].split("_")[0]
                try:
                    client.get_guild(int(ix))
                    print(str(n) + "/" + str(len(ul)) + " : guild '" + ix + "'. looks good.")
                except:
                    db.remove_option("custom_commands", i[0])
                    print(str(n) + "/" + str(len(ul)) + " : Failed to get guild '" + ix + "'. removing.")
                    f += 1
                n += 1
            print("cleaning up user_custom_head")
            ul = db.items("user_custom_head")
            n = 1
            for i in ul:
                try:
                    client.get_user(int(i[0]))
                    print(str(n) + "/" + str(len(ul)) + " : user '" + i[0] + "'. looks good.")
                except:
                    db.remove_option("user_custom_head", i[0])
                    print(str(n) + "/" + str(len(ul)) + " : Failed to get user '" + i[0] + "'. removing.")
                    f += 1
                n += 1
            print("cleaning up custom_head")
            ul = db.items("custom_head")
            n = 1
            for i in ul:
                try:
                    client.get_guild(int(i[0]))
                    print(str(n) + "/" + str(len(ul)) + " : guild '" + i[0] + "'. looks good.")
                except:
                    db.remove_option("custom_head", i[0])
                    print(str(n) + "/" + str(len(ul)) + " : Failed to get guild '" + i[0] + "'. removing.")
                    f += 1
                n += 1
            print("cleaning up server_count")
            ul = db.items("server_count")
            n = 1
            for i in ul:
                try:
                    client.get_guild(int(i[0]))
                    print(str(n) + "/" + str(len(ul)) + " : guild '" + i[0] + "'. looks good.")
                except:
                    db.remove_option("server_count", i[0])
                    print(str(n) + "/" + str(len(ul)) + " : Failed to get guild '" + i[0] + "'. removing.")
                    f += 1
                n += 1
            print("cleaning up server_code")
            ul = db.items("server_code")
            n = 1
            for i in ul:
                try:
                    client.get_guild(int(i[0]))
                    print(str(n) + "/" + str(len(ul)) + " : guild '" + i[0] + "'. looks good.")
                except:
                    db.remove_option("server_code", i[0])
                    print(str(n) + "/" + str(len(ul)) + " : Failed to get guild '" + i[0] + "'. removing.")
                    f += 1
                n += 1
            ul = None
            print(str(f) + " errored items removed.")
        # commands for guild admins
        # these commands will be disabled when bot is in test mode
        elif message.content.startswith(head_s + "서버소개") and ifadmin:
            if message.content == head_s + "서버소개":
                embed=discord.Embed(title="사용 방법", description="루냥아 서버소개 (소개말)\n\n서버 목록에 표시됩니다\n100자까지 등록할 수 있으며, 초대 코드는 첨부할 수 없습니다")
            else:
                if "discord.gg" in message.content or "discord.com" in message.content or "discordapp.com" in message.content:
                    embed=discord.Embed(title="초대 코드를 소개말에 첨부할 수 없습니다")
                else:
                    m = message.content.replace(head_s + "서버소개 ", "")
                    if len(m) > 100:
                        m = m[:99]
                    db.set("guild_intro", str(message.guild.id), m)
                    embed=discord.Embed(title=m_lang.string(db, message.author.id, "guild_intro_set"))
                await message.channel.send(embed=embed)
        elif message.content == head_s + "서버공개" and ifadmin:
            snd = db.get("etc", "ndserver")
            if str(message.guild.id) in snd:
                snd = snd.replace(", " + str(message.guild.id), "")
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "ndserver_activated"), color=0xffffff)
            else:
                snd = snd + ", " + str(message.guild.id)
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "ndserver_deactivated"), color=0xffffff)
            db.set("etc", "ndserver", snd)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "확성기로그" and ifadmin:
            snd = db.get("etc", "mplog")
            if str(message.guild.id) in snd:
                snd = snd.replace(", " + str(message.guild.id), "")
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "mplog_deactivated"), color=0xffffff)
            else:
                snd = snd + ", " + str(message.guild.id)
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "mplog_activated"), color=0xffffff)
            db.set("etc", "mplog", snd)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "가입일시 전체공개" and ifadmin:
            jnd = db.get("etc", "joinedat_ndserver")
            if str(message.guild.id) in jnd:
                jnd = jnd.replace(", " + str(message.guild.id), "")
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "ndjoined_server_deactivated"), color=0xffffff)
            else:
                jnd = jnd + ", " + str(message.guild.id)
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "ndjoined_server_activated"), color=0xffffff)
            db.set("etc", "joinedat_ndserver", jnd)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + "불타는 서버 문구 ") and ifadmin:
            m = message.content.replace(head_s + "불타는 서버 문구 ", "")
            db.set("server_burning", str(message.guild.id), m)
            await message.channel.send(m_lang.string(db, message.author.id, "successfully_set"))
        elif message.content == head_s + "불타는 서버 토글" and ifadmin:
            if scnt != -1:
                db.set("server_count", str(message.guild.id), "-1")
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "server_burning_deactivated"), color=0xffffff)
            else:
                db.set("server_count", str(message.guild.id), "0")
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "server_burning_activated"), color=0xffffff)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "자가진단" and ifadmin:
            await message.channel.trigger_typing()
            await message.channel.send(embed=m_help.permcheck(message.guild.me.guild_permissions))
        elif message.content.startswith(head_s + "지워줘 ") and ifadmin:
            try:
                pu = int(message.content.replace(head_s + "지워줘 ", ""))
                if pu > 100 or pu < 5:
                    embed=discord.Embed(title=m_lang.string(db, message.author.id, "purge_int_error"), color=0xff0000)
                else:
                    pl = await message.channel.purge(limit=pu)
                    pf = open("messages.txt", "w")
                    ps = "삭제된 메시지 내역\r\n-----\r\n"
                    for pm in pl:
                        ps += "채널 : " + pm.channel.name + ", 작성자 : " + pm.author.name + ", " + pm.created_at.isoformat() + "\r\n" + pm.content + "\r\n-----\r\n"
                    pf.write(ps)
                    pf.close()
                    embed=discord.Embed(title=str(len(pl)) + m_lang.string(db, message.author.id, "purged_n"), color=0xff77ff)
                    await server_log(message, 0xff77ff, str(len(pl)) + "개의 메시지를 삭제함")
                    await server_file(message, "messages.txt")
                    os.remove("messages.txt")
            except:
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "generic_error"), description=m_lang.string(db, message.author.id, "purge_error_desc"), color=0xff0000)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "잠수금지" and ifadmin:
            snd = db.get("permissions", "deny_sleep")
            if str(message.guild.id) in snd:
                snd = snd.replace(", " + str(message.guild.id), "")
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "deny_sleep_deactivated"), color=0xffffff)
            else:
                snd = snd + ", " + str(message.guild.id)
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "deny_sleep_activated"), color=0xffffff)
            db.set("permissions", "deny_sleep", snd)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "확성기금지" and ifadmin:
            snd = db.get("permissions", "deny_megaphone")
            if str(message.guild.id) in snd:
                snd = snd.replace(", " + str(message.guild.id), "")
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "deny_megaphone_deactivated"), color=0xffffff)
            else:
                snd = snd + ", " + str(message.guild.id)
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "deny_megaphone_activated"), color=0xffffff)
            db.set("permissions", "deny_megaphone", snd)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + '뮤트 ') and message.content != head_s + '뮤트 목록' and ifadmin:
            ife = False
            try:
                m = db.get("user_mute", str(message.guild.id))
            except:
                m = "0"
            if str(message.mentions[0].id) in m:
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "already_muted"), color=0xff0000)
                ife = True
            else:
                db.set("user_mute", str(message.guild.id), m + ", " + str(message.mentions[0].id))
                embed=discord.Embed(title=message.mentions[0].name + m_lang.string(db, message.author.id, "muted_desc"), color=0xff0000)
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
        elif message.content.startswith(head_s + '언뮤트 ') and ifadmin:
            ife = False
            try:
                m = db.get("user_mute", str(message.guild.id))
                if str(message.mentions[0].id) in m:
                    m = m.replace(", " + str(message.mentions[0].id), "")
                    db.set("user_mute", str(message.guild.id), m)
                    embed=discord.Embed(title=message.mentions[0].name + m_lang.string(db, message.author.id, "unmuted_desc"), color=0x00ff00)
                else:
                    embed=discord.Embed(title=m_lang.string(db, message.author.id, "not_muted"), color=0xffff00)
                    ife = True
            except:
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "not_muting_anyone"), color=0x00ff00)
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
        elif message.content == head_s + '뮤트 목록' and ifadmin:
            try:
                m = db.get("user_mute", str(message.guild.id))
                if m == "0":
                    raise
                else:
                    m = m.split(",")
                    del m[0]
                n = ""
                for i in m:
                    n += m_etc.get_name(i)
                embed = discord.Embed(title="뮤트된 유저 목록", description="```" + n + "```")
            except:
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "not_muting_anyone"), color=0x00ff00)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "로그채널 생성" and ifadmin:
            try:
                try:
                    cid = db.get("server_log", str(message.guild.id))
                    cid = client.get_channel(int(cid))
                    embed=discord.Embed(title=m_lang.string(db, message.author.id, "log_channel_already_exists_title"), description=cid.mention + m_lang.string(db, message.author.id, "log_channel_already_exists_desc"), color=0x00ff00)
                except:
                    cid = await message.guild.create_text_channel("message_log")
                    try:
                        overwrite = discord.PermissionOverwrite()
                        overwrite.read_messages = False
                        await cid.set_permissions(message.guild.default_role, overwrite=overwrite)
                        overwrite.read_messages = True
                        overwrite.send_messages = True
                        overwrite.manage_messages = True
                        overwrite.embed_links = True
                        overwrite.attach_files = True
                        overwrite.read_message_history = True
                        await cid.set_permissions(client.user, overwrite=overwrite)
                    except Exception as e:
                        await message.channel.send(m_lang.string(db, message.author.id, "log_channel_permission_failed"))
                    db.set("server_log", str(message.guild.id), str(cid.id))
                    embed=discord.Embed(title=m_lang.string(db, message.author.id, "log_channel_created_title"), description="메시지 수정, 삭제는 " + cid.mention + m_lang.string(db, message.author.id, "log_channel_created_desc"), color=0x00ff00)
            except:
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "no_channel_management_title"), description=m_lang.string(db, message.author.id, "no_channel_management_desc"), color=0xff0000)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "공지채널 추가" and ifadmin:
            if str(message.channel.id) in db.get("etc", "news_channel"):
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "notice_channel_already"), color=0xffff00)
            else:
                db.set("etc", "news_channel", db.get("etc", "news_channel") + ", " + str(message.channel.id))
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "notice_channel_set_title"), description=m_lang.string(db, message.author.id, "notice_channel_set_desc"), color=0x00ff00)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "공지채널 삭제" and ifadmin:
            if ", " + str(message.channel.id) in db.get("etc", "news_channel"):
                db.set("etc", "news_channel", db.get("etc", "news_channel").replace(", " + str(message.channel.id), ""))
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "notice_channel_unset"), color=0x00ff00)
            else:
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "not_notice_channel"), color=0xffff00)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "채널연결 생성" and ifadmin:
            i = m_ctclink.generate_code(message.channel.id, db)
            if i != False:
                embed = discord.Embed(title=m_lang.string(db, message.author.id, "ctc_code_created"), description=m_lang.string(db, message.author.id, "ctc_code_desc") + i, color=0x00ff00)
            else:
                if m_ctclink.get_link(message.channel.id, db) != False:
                    embed = discord.Embed(title=m_lang.string(db, message.author.id, "already_ctc"), color=0xff0000)
                else:
                    i = m_ctclink.get_link(message.channel.id, db)
                    embed = discord.Embed(title=m_lang.string(db, message.author.id, "no_ctc_connected_title"), description=m_lang.string(db, message.author.id, "ctc_code_desc") + m_ctclink.prev_code)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + '채널연결 접속 ') and ifadmin:
            i = message.content.replace(head_s + "채널연결 접속 ", "")
            c = m_ctclink.get_channel_code(message.channel.id, i, db)
            if c == False:
                embed = discord.Embed(title=m_lang.string(db, message.author.id, "invalid_ctc_code"), color=0xff0000)
            else:
                ch = client.get_channel(int(c))
                embed = discord.Embed(title="채널 연결 완료!", description=ch.guild.name + "의 " + ch.name + m_lang.string(db, message.author.id, "ctc_created"), color=0x00ff00)
                embed2 = discord.Embed(title="채널 연결 완료!", description=message.guild.name + "의 " + message.channel.name + m_lang.string(db, message.author.id, "ctc_created"), color=0x00ff00)
                await ch.send(embed=embed2)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "채널연결 삭제" and ifadmin:
            if cr0 == False:
                if m_ctclink.remove_pending(message.channel.id, db) == True:
                    embed = discord.Embed(title=m_lang.string(db, message.author.id, "ctc_canceled"), color=0xffff00)
                else:
                    embed = discord.Embed(title=m_lang.string(db, message.author.id, "ctc_not_connected"), color=0xff0000)
            else:
                m_ctclink.remove_link(message.channel.id, db)
                cr = client.get_channel(int(cr0))
                embed2 = discord.Embed(title=message.guild.name + "의 " + message.channel.name + " 채널과의 연결이 " + message.author.name + m_lang.string(db, message.author.id, "ctc_deleted_another"), color=0xff0000)
                await cr.send(embed=embed2)
                embed = discord.Embed(title=m_lang.string(db, message.author.id, "ctc_deleted"), color=0x00ff00)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "채널연결 정보" and ifadmin:
            if cr0 != False:
                cr = client.get_channel(int(cr0))
                embed = discord.Embed(title="채널연결 정보", color=0xffffff)
                embed.add_field(name="연결된 서버 이름", value=cr.guild.name, inline=False)
                embed.add_field(name="연결된 채널 이름", value=cr.name, inline=False)
                embed.add_field(name="연결 코드", value=m_ctclink.get_code(message.channel.id, db))
            else:
                embed = discord.Embed(title=m_lang.string(db, message.author.id, "ctc_not_connected"), color=0xff0000)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + '채널연결 debug ') and ifadmin:
            m = message.content.replace(head_s + '채널연결 debug ', '')
            n = m_ctclink.get_link_by_code(m, db)
            await message.channel.send(n)
        elif message.content.startswith(head_s + '킥') and ifadmin:
            try:
                if not message.mentions:
                    embed=discord.Embed(title=m_lang.string(db, message.author.id, "define_user_to_kick"), color=0xffff00)
                else:
                    await message.mentions[0].kick()
                    embed=discord.Embed(title=message.mentions[0].name + m_lang.string(db, message.author.id, "kicked"), color=0xffff00)
                    await server_log(message, 0xffff00, message.mentions[0].name + "을(를) 킥함")
            except Exception as e:
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "no_user_management_title"), description=m_lang.string(db, message.author.id, "no_user_management_desc"), color=0xffff00)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + '밴') and ifadmin:
            try:
                if message.content == head_s + "밴":
                    embed=discord.Embed(title=m_lang.string(db, message.author.id, "define_user_to_ban"), color=0xff0000)
                else:
                    b = message.content.replace(head_s + '밴 ', '')
                    if not message.mentions:
                        b = int(b)
                        busr = await client.fetch_user(b)
                        if b == None:
                            embed=discord.Embed(title=m_lang.string(db, message.author.id, "user_not_found"), color=0xff0000)
                        else:
                            await message.guild.ban(user=busr)
                    else:
                        busr = message.mentions[0]
                        await message.guild.ban(user=busr)
                    embed=discord.Embed(title=busr.name + m_lang.string(db, message.author.id, "banned"), color=0xff0000)
                    await server_log(message, 0xffff00, busr.name + "을(를) 밴함")
            except:
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "no_user_management_title"), description=m_lang.string(db, message.author.id, "no_user_management_desc"), color=0xffff00)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "초대링크 생성" and ifadmin:
            try:
                inv = await message.channel.create_invite()
                await message.channel.send(inv.url)
                await server_log(message, 0xffff00, "즉석 초대를 생성함", inv.url)
            except:
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "generic_error"), description=m_lang.string(db, message.author.id, "lack_permissions"), color=0xff0000)
                await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + "환영인사 ") and ifadmin:
            if message.content == head_s + "환영인사 삭제":
                try:
                    db.remove_option("welcome_message", str(message.guild.id))
                    embed=discord.Embed(title=m_lang.string(db, message.author.id, "welcome_message_deleted"), color=0x00ff00)
                except:
                    embed=discord.Embed(title=m_lang.string(db, message.author.id, "welcome_message_not_set"), color=0xff0000)
            else:
                if not " | " in message.content:
                    db.set("welcome_message", str(message.guild.id), str(message.channel.id) + " | " + message.content.replace(head_s + "환영인사 ", ""))
                    embed = discord.Embed(title=m_lang.string(db, message.author.id, "welcome_message_set_title"), description=m_lang.string(db, message.author.id, "welcome_message_set_desc"), color=0x00ff00)
                else:
                    embed = discord.Embed(title=m_lang.string(db, message.author.id, "unallowed_glyph"), description=m_lang.string(db, message.author.id, "unallowed_glyph_desc_1"), color=0xff0000)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + "작별인사 ") and ifadmin:
            if message.content == head_s + "작별인사 삭제":
                try:
                    db.remove_option("farewell_message", str(message.guild.id))
                    embed=discord.Embed(title=m_lang.string(db, message.author.id, "farewell_message_deleted"), color=0x00ff00)
                except:
                    embed=discord.Embed(title=m_lang.string(db, message.author.id, "farewell_message_not_set"), color=0xff0000)
            else:
                if not " | " in message.content:
                    db.set("farewell_message", str(message.guild.id), str(message.channel.id) + " | " + message.content.replace(head_s + "작별인사 ", ""))
                    embed = discord.Embed(title=m_lang.string(db, message.author.id, "farewell_message_set_title"), description=m_lang.string(db, message.author.id, "farewell_message_set_desc"), color=0x00ff00)
                else:
                    embed = discord.Embed(title=m_lang.string(db, message.author.id, "unallowed_glyph"), description=m_lang.string(db, message.author.id, "unallowed_glyph_desc_1"), color=0xff0000)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + "서버 접두어") and ifadmin:
            if message.content == head_s + "서버 접두어":
                embed=discord.Embed(title='사용 방법 : 루냥아 서버 접두어 (접두어)')
            else:
                hst = message.content.replace(head_s + "서버 접두어 ", "")
                db.set("custom_head", str(message.guild.id), hst)
                embed=discord.Embed(title='서버의 지정 접두어가 "' + hst + m_lang.string(db, message.author.id, "custom_head_set_title"), description=m_lang.string(db, message.author.id, "custom_head_set_desc"), color=0xffffff)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "금지채널 추가" and ifadmin:
            dst = db.get("etc", "denied_channel")
            if str(message.channel.id) in dst:
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "already_muted_channel"), color=0xff0000)
            else:
                dst = dst + ", " + str(message.channel.id)
                db.set("etc", "denied_channel", dst)
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "muted_channel_title"), description=m_lang.string(db, message.author.id, "muted_channel_desc"), color=0xffffff)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "잠수채널" and ifadmin:
            try:
                _ = db.get("sleep_channel", str(message.guild.id))
                db.remove_option("sleep_channel", str(message.guild.id))
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "deleted_from_sleep_channel"), color=0xff0000)
            except:
                db.set("sleep_channel", str(message.guild.id), str(message.channel.id))
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "added_to_sleep_channel"), description=m_lang.string(db, message.author.id, "added_to_sleep_channel_desc"), color=0xffffff)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "애드블락 추가" and ifadmin:
            ast = db.get("etc", "adblock_channel")
            if str(message.channel.id) in ast:
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "already_adblock"), color=0xff0000)
            else:
                ast = ast + ", " + str(message.channel.id)
                db.set("etc", "adblock_channel", ast)
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "adblock_added_title"), description=m_lang.string(db, message.author.id, "adblock_added_desc"), color=0xffff00)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "애드블락 삭제" and ifadmin:
            ast = db.get("etc", "adblock_channel")
            if str(message.channel.id) in ast:
                ast = ast.replace(", " + str(message.channel.id), "")
                db.set("etc", "adblock_channel", ast)
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "adblock_deleted"), color=0xffff00)
            else:
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "no_adblock"), color=0xff0000)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "유저패시브" and ifadmin:
            pst = db.get("etc", "passive_denied")
            if str(message.guild.id) in pst:
                pst = pst.replace(", " + str(message.guild.id), "")
                db.set("etc", "passive_denied", pst)
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "user_passive_allowed"), color=0xffff00)
            else:
                pst = pst + ", " + str(message.guild.id)
                db.set("etc", "passive_denied", pst)
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "user_passive_denied"), color=0xffff00)
            await message.channel.send(embed=embed)
        elif message.content == head_s + "야짤채널" and ifadmin:
            if str(message.guild.id) in db.get("moderation", "ban_nsfw"):
                embed=discord.Embed(title="오류 발생 : 사용할 수 없는 기능입니다", description="[민원창구](https://discordapp.com/invite/6pgYMbC)에 해당 에러 내용을 접수해 주시기 바랍니다")
                await message.channel.send(embed=embed)
            else:
                if message.channel.is_nsfw():
                    if str(message.channel.id) in db.get("etc", "nsfw_channel"):
                        db.set("etc", "nsfw_channel", db.get("etc", "nsfw_channel").replace(", " + str(message.channel.id), ""))
                        embed=discord.Embed(title=m_lang.string(db, message.author.id, "nsfw_neko_denied"), color=0xffff00)
                        await message.channel.send(embed=embed)
                    else:
                        db.set("etc", "nsfw_channel", db.get("etc", "nsfw_channel") + ", " + str(message.channel.id))
                        embed=discord.Embed(title=m_lang.string(db, message.author.id, "nsfw_neko_allowed"), color=0xffff00)
                        await message.channel.send(embed=embed)
                else:
                    embed=discord.Embed(title=m_lang.string(db, message.author.id, "not_a_nsfw_channel"), color=0xffff00)
                    await message.channel.send(embed=embed)
        elif message.content == head_s + "잠수 쿨타임" and ifadmin:
            if str(message.guild.id) in db.get("etc", "no_sleep_cooldown"):
                db.set("etc", "no_sleep_cooldown", db.get("etc", "no_sleep_cooldown").replace(", " + str(message.guild.id), ""))
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "sleep_cooldown_enabled"), color=0xffff00)
                await message.channel.send(embed=embed)
            else:
                cd = db.items('j_sleep_cooldown')
                for i in cd:
                    if i[0].startswith(str(message.guild.id)):
                        db.remove_option('j_sleep_cooldown', i[0])
                db.set("etc", "no_sleep_cooldown", db.get("etc", "no_sleep_cooldown") + ", " + str(message.guild.id))
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "sleep_cooldown_disabled"), color=0xffff00)
                await message.channel.send(embed=embed)
        elif message.content == head_s + "일상대화 접두어" and ifadmin:
            if str(message.guild.id) in db.get("etc", "pingpong_headless"):
                db.set("etc", "pingpong_headless", db.get("etc", "pingpong_headless").replace(", " + str(message.guild.id), ""))
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "pingpong_headless_denied"), color=0xffff00)
                await message.channel.send(embed=embed)
            else:
                db.set("etc", "pingpong_headless", db.get("etc", "pingpong_headless") + ", " + str(message.guild.id))
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "pingpong_headless_allowed"), color=0xffff00)
                await message.channel.send(embed=embed)
        elif message.content == head_s + "서버 지정 명령어 접두어" and ifadmin:
            if str(message.guild.id) in db.get("etc", "guild_custom_headless"):
                db.set("etc", "guild_custom_headless", db.get("etc", "guild_custom_headless").replace(", " + str(message.guild.id), ""))
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "guild_custom_headless_denied"), color=0xffff00)
                await message.channel.send(embed=embed)
            else:
                db.set("etc", "guild_custom_headless", db.get("etc", "guild_custom_headless") + ", " + str(message.guild.id))
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "guild_custom_headless_allowed"), color=0xffff00)
                await message.channel.send(embed=embed)
        elif message.content == head_s + "비밀채널" and ifadmin:
            embed=discord.Embed(title="사용 방법", description="루냥아 비밀채널 (5부터 75까지의 숫자)")
            embed.add_field(name="효과", value="채널 내 메시지 수가 지정된 수를 넘어서는 경우 제일 오래된 메시지부터 삭제", inline=False)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + "비밀채널 ") and message.content != head_s + "비밀채널 해제" and ifadmin:
            m = int(message.content.replace(head_s + "비밀채널 ", ""))
            cnt = 0
            if m > 75 or m < 5:
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "volatile_invalid_count"), color=0xff0000)
            else:
                async for cf in message.channel.history(limit=100):
                    cnt += 1
                if cnt > m:
                    embed=discord.Embed(title=m_lang.string(db, message.author.id, "volatile_counts_too_much"), color=0xff0000)
                else:
                    db.set("volatile_channel", str(message.channel.id), str(m))
                    embed=discord.Embed(title=m_lang.string(db, message.author.id, "volatile_channel_set"))
                    embed.set_footer(text='비밀채널 해제 : "루냥아 비밀채널 해제"')
            await message.channel.send(embed=embed)
        elif message.content == head_s + "비밀채널 해제" and ifadmin:
            try:
                db.remove_option("volatile_channel", str(message.channel.id))
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "volatile_channel_unset"))
                await message.channel.send(embed=embed)
            except:
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "volatile_channel_not_set"))
                await message.channel.send(embed=embed)
        elif message.content == head_s + "서버코드 초기화" and ifadmin:
            code = m_servercode.generate_code(message.guild, db, True)
            embed=discord.Embed(title=m_lang.string(db, message.author.id, "server_code_reset"), description="바뀐 서버 코드 : " + code)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + "커스텀 명령어 연결") and not message.content.startswith(head_s + "커스텀 명령어 연결해제") and not message.content.startswith(head_s + "커스텀 명령어 연결목록") and ifadmin:
            if message.content == head_s + "커스텀 명령어 연결":
                embed=discord.Embed(title="사용 방법 : 루냥아 커스텀 명령어 연결 (서버코드)", description="서버 코드는 '루냥아 서버설정'에서 확인할 수 있습니다")
                await message.channel.send(embed=embed)
            else:
                lc = message.content.replace(head_s + "커스텀 명령어 연결 ", "")
                try:
                    sid = m_servercode.get_guild(lc, db)
                    try:
                        db.set("link_custom_commands_pending", str(message.guild.id), sid)
                        cid = db.get("server_log", sid)
                        c = client.get_channel(int(cid))
                        text = c.guild.owner.mention + " " + message.guild.name + "에서 서버 지정 명령어 연결을 요청했어요!\n\n"
                        text+= "서버 지정 명령어를 연결하면 " + message.guild.name + "이 " + c.guild.name + "의 서버 지정 명령어를 사용할 수 있게 돼요!\n"
                        text+= message.guild.name + "에서 " + c.name + "의 서버 지정 명령어를 수정할 수는 없으니 안심하세요!\n\n"
                        text+= "요청을 승인하려면 'Y', 거절하려면 'N'을 입력해주세요!"
                        await c.send(text)
                        text = m_lang.string(db, message.author.id, "requested_link_custom_commands")
                        text = text.replace("{1}", c.name)
                        await message.channel.send(text)
                    except Exception as e:
                        await message.channel.send(m_lang.string(db, message.author.id, "no_log_channel_in_there"))
                except:
                    await message.channel.send(m_lang.string(db, message.author.id, "servercode_not_found"))
        elif message.content == head_s + "커스텀 명령어 연결목록" and ifadmin:
            try:
                g1id = db.get("link_custom_commands", str(message.guild.id))
                g1 = client.get_guild(int(g1id))
                g1t = g1.name
            except:
                g1t = "없음"
            g2l = db.items("link_custom_commands")
            g2num = 1
            g2t = ""
            nog = True
            for g2i in g2l:
                if message.guild.id == int(g2i[1]):
                    nog = False
                    g2 = client.get_guild(int(g2i[0]))
                    g2t += "#" + str(g2num) + " : " + g2.name + "\n"
                    g2num += 1
            if nog:
                g2t = "없음"
            embed=discord.Embed(title="연결된 커스텀 명령어 목록")
            embed.add_field(name="가져온 명령어 서버", value=g1t, inline=False)
            embed.add_field(name="현재 서버의 명령어를 가져감", value=g2t, inline=False)
            await message.channel.send(embed=embed)
        elif message.content.startswith(head_s + "커스텀 명령어 연결해제") and ifadmin:
            if message.content == head_s + "커스텀 명령어 연결해제":
                text = "루냥아 커스텀 명령어 연결해제 (번호)\n\n"
                text+= "번호는 '루냥아 커스텀 명령어 연결목록'에서 확인 가능합니다\n"
                text+= "0번을 입력하면 현재 서버에서 가져온 명령어 연결을 끊습니다"
                embed=discord.Embed(title="사용 방법", description=text)
            else:
                m = message.content.replace(head_s + "커스텀 명령어 연결해제 ", "")
                gl = []
                g2l = db.items("link_custom_commands")
                for g2i in g2l:
                    if g2i[1] == str(message.guild.id):
                        gl.append(g2i[0])
                else:
                    await message.channel.send(m_lang.string(db, message.author.id, "no_linked_custom_commands"))
                try:
                    if m == "0":
                        g1id = db.get("link_custom_commands", str(message.guild.id))
                        db.remove_option("link_custom_commands", str(message.guild.id))
                        g1ci = db.get("server_log", g1id)
                        g1c = client.get_channel(g1ci)
                        embed=discord.Embed("커스텀 명령어 연결을 끊음", description="서버명 : " + message.guild.name)
                        await g1c.send(embed=embed)
                        text = m_lang.string(db, message.author.id, "deleted_custom_command_link")
                        text = text.replace("{1}", g1c.guild.name)
                        await message.channel.send(text)
                    else:
                        g1id = db.get("link_custom_commands", gl[int(m) - 1])
                        db.remove_option("link_custom_commands", gl[int(m) - 1])
                        g1ci = db.get("server_log", g1id)
                        g1c = client.get_channel(g1ci)
                        embed=discord.Embed("커스텀 명령어 연결을 끊음", description="서버명 : " + message.guild.name)
                        await g1c.send(embed=embed)
                        text = m_lang.string(db, message.author.id, "deleted_custom_command_link")
                        text = text.replace("{1}", g1c.guild.name)
                        await message.channel.send(text)
                except:
                    await message.channel.send(m_lang.string(db, message.author.id, "wrong_idx"))
        elif message.content == head_s + "잠금해제" and ifadmin:
            te = datetime.now()
            te = int(te.timestamp())
            db.set('guild_unlock', str(message.guild.id), str(te + 60))
            await message.channel.send(m_lang.string(db, message.author.id, "server_unlocked"))
        elif message.content.startswith(head_s + "서버이동") and ifadmin:
            try:
                db.get('guild_unlock', str(message.guild.id))
                if message.content == head_s + "서버이동":
                    embed=discord.Embed(title="사용 방법 : 루냥아 서버이동 (서버코드)", description="서버 코드는 '루냥아 서버설정'에서 확인할 수 있습니다")
                    await message.channel.send(embed=embed)
                else:
                    lc = message.content.replace(head_s + "서버이동 ", "")
                    try:
                        sid = m_servercode.get_guild(lc, db)
                        try:
                            db.set("move_guild_pending", str(message.guild.id), sid)
                            cid = db.get("server_log", sid)
                            c = client.get_channel(int(cid))
                            text = c.guild.owner.mention + " " + message.guild.name + "에서 서버 이동을 요청했어요!\n\n"
                            text+= "서버를 이동하면 " + message.guild.name + "에서 " + c.guild.name + "으로 커스텀 명령어와 서버 설정이 이동돼요!\n"
                            text+= "요청을 승인하려면 'Y', 거절하려면 'N'을 입력해주세요!"
                            await c.send(text)
                            text = m_lang.string(db, message.author.id, "requested_guild_move")
                            text = text.replace("{1}", c.name)
                            await message.channel.send(text)
                        except Exception as e:
                            await message.channel.send(m_lang.string(db, message.author.id, "no_log_channel_in_there"))
                    except:
                        await message.channel.send(m_lang.string(db, message.author.id, "servercode_not_found"))
            except:
                await message.channel.send(m_lang.string(db, message.author.id, "plz_unlock_server"))
        elif message.content == head_s + "서버초기화" and ifadmin:
            try:
                db.get('guild_unlock', str(message.guild.id))
                db.set("etc", "reset_guild_pending", db.get("etc", "reset_guild_pending") + ", " + str(message.guild.id))
                embed = discord.Embed(title=m_lang.string(db, message.author.id, "confirm_guild_reset_title"), description=m_lang.string(db, message.author.id, "confirm_guild_reset_desc"))
                embed.add_field(name="하게 되는 것", value="```- 서버 설정이 초기화됩니다\n- 뮤트된 사용자 목록이 초기화됩니다\n- 서버 지정 명령어가 **모두 삭제**됩니다```")
                await message.channel.send(embed=embed)
            except:
                await message.channel.send(m_lang.string(db, message.author.id, "plz_unlock_server"))
        elif message.content == "Y" and ifadmin:
            cs = db.items("link_custom_commands_pending")
            cs2 = db.items("move_guild_pending")
            cs3 = db.get("etc", "reset_guild_pending")
            for cc in cs:
                if cc[1] == str(message.guild.id):
                    db.remove_option("link_custom_commands_pending", cc[0])
                    db.set("link_custom_commands", cc[0], cc[1])
                    try:
                        c = client.get_channel(int(db.get("server_log", cc[0])))
                        await c.send(m_lang.string(db, message.author.id, "link_custom_commands_accepted_orig"))
                    except:
                        pass
                    await message.channel.send(m_lang.string(db, message.author.id, "link_custom_commands_accepted_targ"))
            else:
                for cc in cs2:
                    if cc[1] == str(message.guild.id):
                        db.remove_option("move_guild_pending", cc[0])
                        cc = db.items("custom_commands")
                        for ci in cc:
                            if str(message.guild.id) in ci[0]:
                                cix = ci[0].replace(cc[0], cc[1])
                                db.set("custom_commands", cix, ci[1])
                                db.remove_option("custom_commands", ci[0])
                        for mv in ["joinedat_nduser", "joinedat_ndserver", "createdat_nd", "ndserver", "passive_denied", "pingpong_headless", "guild_custom_headless"]:
                            if cc[0] in db.get("etc", mv):
                                db.set("etc", mv, db.get("etc", mv).replace(cc[0], cc[1]))
                        try:
                            db.set("custom_head", cc[1], db.get("custom_head", cc[0]))
                            db.remove_option("custom_head", cc[0])
                        except:
                            pass
                        try:
                            db.set("guild_intro", cc[1], db.get("guild_intro", cc[0]))
                            db.remove_option("guild_intro", cc[0])
                        except:
                            pass
                        try:
                            c = client.get_channel(int(db.get("server_log", cc[0])))
                            await c.send(m_lang.string(db, message.author.id, "guild_moved_orig"))
                        except:
                            pass
                        await message.channel.send(m_lang.string(db, message.author.id, "guild_moved_targ"))
                else:
                    if str(message.guild.id) in cs3:
                        dt = datetime.now()
                        dt = str(int(dt.timestamp()))
                        cc = db.items("custom_commands")
                        pf = open("logs/guild_reset_" + str(message.guild.id) + dt + ".txt", "w")
                        ps = "[custom commands]\n"
                        for ci in cc:
                            if str(message.guild.id) in ci[0]:
                                ps += ci[0] + " = " + ci[1] + "\n"
                                db.remove_option("custom_commands", ci[0])
                        ps += "\n[etc]"
                        for mv in ["joinedat_nduser", "joinedat_ndserver", "createdat_nd", "ndserver", "passive_denied", "pingpong_headless", "guild_custom_headless"]:
                            if str(message.guild.id) in db.get("etc", mv):
                                ps += mv + "\n"
                                db.set("etc", mv, db.get("etc", mv).replace(", " + str(message.guild.id), ""))
                        try:
                            ps += "\n[custom_head]\n" + str(message.guild.id) + " = " + db.get("custom_head", str(message.guild.id))
                            db.remove_option("custom_head", str(message.guild.id))
                        except:
                            pass
                        try:
                            ps += "\n[guild_intro]\n" + str(message.guild.id) + " = " + db.get("guild_intro", str(message.guild.id))
                            db.remove_option("guild_intro", str(message.guild.id))
                        except:
                            pass
                        db.set("etc", "reset_guild_pending", db.get("etc", "reset_guild_pending").replace(", " + str(message.guild.id), ""))
                        pf.write(ps)
                        pf.close()
                        await message.channel.send(m_lang.string(db, message.author.id, "guild_reset"))
                    else:
                        pass
        elif message.content == "N" and ifadmin:
            cs = db.items("link_custom_commands_pending")
            cs2 = db.items("move_guild_pending")
            cs3 = db.get("etc", "reset_guild_pending")
            for cc in cs:
                if cc[1] == str(message.guild.id):
                    db.remove_option("link_custom_commands_pending", cc[0])
                    try:
                        c = client.get_channel(int(db.get("server_log", cc[0])))
                        await c.send(m_lang.string(db, message.author.id, "link_custom_commands_canceled_orig"))
                    except:
                        pass
                    await message.channel.send(m_lang.string(db, message.author.id, "link_custom_commands_canceled_targ"))
            else:
                for cc in cs2:
                    if cc[1] == str(message.guild.id):
                        db.remove_option("move_guild_pending", cc[0])
                    try:
                        c = client.get_channel(int(db.get("server_log", cc[0])))
                        await c.send(m_lang.string(db, message.author.id, "guild_move_canceled_orig"))
                    except:
                        pass
                    await message.channel.send(m_lang.string(db, message.author.id, "guild_move_canceled_targ"))
                else:
                    if str(message.guild.id) in cs3:
                        db.set("etc", "reset_guild_pending", db.get("etc", "reset_guild_pending").replace(", " + str(message.guild.id), ""))
                        await message.channel.send(m_lang.string(db, message.author.id, "reset_guild_cancelled"))
                    else:
                        pass
        # external commands
        else:
            res = m_ext_commands.ext_talk(client, message, head_s)
            res2 = m_user.guild_custom_commands(client, db, message, dmchannel)
            if res != None:
                try:
                    if str(message.guild.id) in db.get("etc", "pingpong_headless"):
                        await message.channel.send(embed=res)
                    elif message.content.startswith(head_s):
                        await message.channel.send(embed=res)
                    else:
                        pass
                except:
                    await message.channel.send(embed=res)
            elif res2 != None:
                try:
                    if dmchannel:
                        if str(type(res2)) == "<class 'discord.embeds.Embed'>":
                            await message.channel.send(embed=res2)
                        else:
                            await message.channel.send(res2)
                    elif str(message.guild.id) in db.get("etc", "guild_custom_headless"):
                        if str(type(res2)) == "<class 'discord.embeds.Embed'>":
                            await message.channel.send(embed=res2)
                        else:
                            await message.channel.send(res2)
                    elif message.content.startswith(head_s):
                        if str(type(res2)) == "<class 'discord.embeds.Embed'>":
                            await message.channel.send(embed=res2)
                        else:
                            await message.channel.send(res2)
                    else:
                        pass
                except Exception as e:
                    print(traceback.format_exc())
                    pass
            else:
                pass
        with open(db_path, 'w') as configfile:
            db.write(configfile)
    except Exception as e:
        if str(e) == "rebootme":
            sys.exit("rebootme")
        else:
            if "Missing Permissions" in str(e):
                embed=discord.Embed(title=m_etc.err_txt(), description="봇이 해당 명령을 수행하기 위한 권한이 충족되지 않았습니다. '루냥아 자가진단'으로 권한을 확인할수 있습니다.")
            else:
                embed=discord.Embed(title=m_etc.err_txt(), description="오류 보고서가 자동 전송되었습니다.")
                await message.channel.send(embed=embed)
                cid = conf.get("config", "traceback_channel")
                cid = client.get_channel(int(cid))
                embed = discord.Embed(title="Traceback occured at " + str(datetime.now()))
                embed.add_field(name="Traceback", value="```" + traceback.format_exc() + "```")
                try:
                    embed.add_field(name="user", value="```" + message.author.name + " (" + str(message.author.id) + ")```", inline=False)
                    embed.add_field(name="guild", value="```" + message.guild.name + " (" + str(message.guild.id) + ")```", inline=False)
                    embed.add_field(name="channel", value="```" + message.channel.name + " (" + str(message.channel.id) + ")```", inline=False)
                except:
                    pass
                embed.add_field(name="message content", value="```" + message.content + "```", inline=False)
                await cid.send(embed=embed)

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
    elif message.content.startswith(m_user.head(db, message, test_glyph) + "확성기 "):
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
    elif before.content == after.content:
        return
    try:
        cid = db.get("server_log", str(before.guild.id))
        cid = client.get_channel(int(cid))
        if cid != None:
            embed=discord.Embed(title="메시지 수정 감지", description=before.author.name, color=0xff0000)
            embed.add_field(name="이전", value=before.content, inline=False)
            embed.add_field(name="이후", value=after.content, inline=False)
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

@client.event
async def on_member_join(member):
    s = str(member.guild.id)
    l = dict(db.items("welcome_message"))
    if s in l:
        a = db.get("welcome_message", s)
        a = a.split("|")
        c = client.get_channel(int(a[0]))
        m = a[1]
        m = m.replace("[멘션]", member.mention)
        m = m.replace("[이름]", member.name)
        try:
            await c.send(m)
        except:
            db.remove_option("welcome_message", s)
    try:
        cid = db.get("server_log", str(member.guild.id))
        cid = client.get_channel(int(cid))
        if cid != None:
            embed=discord.Embed(title="사용자가 서버를 입장함", color=0x00ff00)
            embed.add_field(name="이름", value=member.name, inline=False)
            embed.add_field(name="사용자 ID", value=str(member.id), inline=False)
            await cid.send(embed=embed)
        else:
            db.remove_option("server_log", str(member.guild.id))
    except:
        pass

@client.event
async def on_member_remove(member):
    s = str(member.guild.id)
    l = dict(db.items("farewell_message"))
    if s in l:
        a = db.get("farewell_message", s)
        a = a.split("|")
        c = client.get_channel(int(a[0]))
        m = a[1]
        m = m.replace("[이름]", member.name)
        try:
            await c.send(m)
        except:
            db.remove_option("farewell_message", s)
    try:
        cid = db.get("server_log", str(member.guild.id))
        cid = client.get_channel(int(cid))
        if cid != None:
            embed=discord.Embed(title="사용자가 서버를 퇴장함", color=0x00ff00)
            embed.add_field(name="이름", value=member.name, inline=False)
            embed.add_field(name="사용자 ID", value=str(member.id), inline=False)
            await cid.send(embed=embed)
        else:
            db.remove_option("server_log", str(member.guild.id))
    except:
        pass

@client.event
async def on_member_update(before, after):
    s = before.guild
    nb = before.nick
    na = after.nick
    nn = after.name
    if nb != na and nb != None and na != None:
        try:
            cid = db.get("server_log", str(before.guild.id))
            cid = client.get_channel(int(cid))
            if cid != None:
                embed=discord.Embed(title=nn + " 님이 서버 닉네임을 변경함", color=0x00ff00)
                embed.add_field(name="이전", value=nb, inline=False)
                embed.add_field(name="이후", value=na, inline=False)
                await cid.send(embed=embed)
            else:
                db.remove_option("server_log", str(before.guild.id))
        except:
            pass
    else:
        pass

@client.event
async def on_guild_join(guild):
    m_servercode.generate_code(guild, db, False)
    if guild.system_channel != None:
        await guild.system_channel.send(embed=m_help.bot_welcome_message(client, bot_ver))

def handler(signal_received, frame):
    print('Saving DB...')
    with open(db_path, 'w') as configfile:
        db.write(configfile)
    print('Terminating...')
    sys.exit(0)

signal(SIGINT, handler)
print("INFO    : connecting to Discord. Please Wait..")
client.run(conf.get("config", "bot_token"))

#!/usr/bin/python3
import re, traceback, discord, datetime, asyncio, logging, os, random, configparser, m_lifetime, m_food, m_ez2ac, m_muteuser
from m_rps import rps_run
from m_seotda import *
from m_wolframalpha import wa_calc
from m_etc import *

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='log.txt', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot_ver = "1.7.8"

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
    print('name : ' + str(client.user.name))
    print('id   : ' + str(client.user.id))
    await client.change_presence(game=discord.Game(name='#기계식루냥이_사용법 ㄱ | ' + bot_ver))

@client.event
async def on_message(message):
    global precense_enabled
    global precense
    global test_glyph
    if message.author == client.user:
        return
    elif message.author.bot:
        return
    if message.server.id == db.get("config", "server_id"):
        if m_muteuser.check_muted(str(message.author.id)):
            await client.delete_message(message)
            return
        try:
            temp_point = int(db.get("user_point", str(message.author.id)))
            temp_point = temp_point + int(db.get("config", "point_increment"))
            db.set("user_point", str(message.author.id), str(temp_point))
        except:
            db.set("user_point", str(message.author.id), "0")
        hatespeech = re.compile(db.get("string", "hatespeech"))
        hs_match = hatespeech.match(message.content)
        if hs_match:
            await client.send_message(discord.Object(id=db.get('config', 'alert_channel_id')), "possible hate speech found at " + message.channel.name + "\n" + message.author.display_name + " : " + message.content + "\nat : " + str(datetime.datetime.now()))
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
        elif message.content.startswith(test_glyph + '루냥아 gprecense '):
            if message.author.id == str(db.get("config", "owner_id")):
                gprec_sanitize = message.content
                gprec_sanitize = gprec_sanitize.replace('루냥아 gprecense ', '')
                await client.change_presence(game=discord.Game(name=gprec_sanitize))
                await client.send_message(message.channel, ":ok_hand:")
            else:
                await client.send_message(message.channel, ":thinking:")
        elif message.content.startswith(test_glyph + '루냥아 gpresence --disable'):
            if message.author.id == str(db.get("config", "owner_id")):
                await client.change_presence(game=discord.Game(name='#기계식루냥이_사용법 ㄱ | ' + bot_ver))
                await client.send_message(message.channel, ":ok_hand:")
            else:
                await client.send_message(message.channel, ":thinking:")
        elif message.content.startswith(test_glyph + '루냥아 뭐하니'):
            await client.send_message(message.channel, m_lifetime.return_lifetime(precense))
        elif message.content.startswith(test_glyph + '루냥이 실력 어느정도니'):
            await client.send_message(message.channel, lg_ret())
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
        elif message.content.startswith(test_glyph + "루냥아 계산해줘 "):
            try:
                bc_str = message.content
                bc_str = bc_str.replace("루냥아 계산해줘 ","")
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
        elif message.content.startswith(test_glyph + '루냥아 초대코드'):
            await client.send_message(message.channel, str(db.get("string", "invite_code")))
        elif message.content.startswith(test_glyph + '루냥아 갓곡알려줘'):
            await client.send_message(message.channel, m_ez2ac.ez2ac_song_select())
        elif message.content.startswith(test_glyph + '루냥아 채금해줘 '):
            if message.author.server_permissions.administrator:
                await client.send_message(message.channel, m_muteuser.mute_user(str(message.mentions[0].id)))
                await client.send_message(discord.Object(id=db.get('config', 'alert_channel_id')), str(message.mentions[0].name) + " muted by " + message.author.display_name + " at " + str(datetime.datetime.now()))
            else:
                await client.send_message(message.channel, ":thinking:")
        elif message.content.startswith(test_glyph + '루냥아 채금 풀어줘 '):
            if message.author.server_permissions.administrator:
                await client.send_message(message.channel, m_muteuser.unmute_user(str(message.mentions[0].id)))
                await client.send_message(discord.Object(id=db.get('config', 'alert_channel_id')), str(message.mentions[0].name) + " unmuted by " + message.author.display_name + " at " + str(datetime.datetime.now()))
            else:
                await client.send_message(message.channel, ":thinking:")
        with open(db_path, 'w') as configfile:
            db.write(configfile)
    else:
        await client.send_message(message.channel, "**STOP!**\n\nRunning this bot out of owner's server is prohibited.\n**PLEASE KICK ME.**\n\nIf you can understand what are you doing, you can pork my source repository!\nhttps://github.com/LunaNyan/Luna_Libertin_Discord_Bot")

@client.event
async def on_message_delete(message):
    if message.author == client.user:
        return
    elif message.author.bot:
        return
    await client.send_message(discord.Object(id=db.get('config', 'log_channel_id')), "message removed from " + message.author.display_name + " at " + message.channel.name + "\n" + message.content + "\nat : " + str(datetime.datetime.now()))

@client.event
async def on_message_edit(before, after):
    if before.author == client.user:
        return
    elif before.author.bot:
        return
    await client.send_message(discord.Object(id=db.get('config', 'log_channel_id')), "message edited from " + before.author.display_name + " at " + before.channel.name + "\nbefore : " + before.content + "\nafter : " + after.content + "\nat : " + str(datetime.datetime.now()))

client.run(db.get("config", "bot_token"))

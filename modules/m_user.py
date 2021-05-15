import sys, math, discord, random, datetime, m_etc, m_lang, configparser, m_custom_embed
from dateutil.relativedelta import *

if __name__=="__main__":
    print("FATAL   : Run this bot from right way.")
    sys.exit(1)

test_glyph_2 = ""

sdb_path = "db/command_suggests.dat"

sdb = configparser.ConfigParser()
sdb.read(sdb_path)

def set_bio(conf, user, text):
    conf.set("bio", str(user.id), text)

def get_bio(conf, user):
    try:
        s = conf.get("bio", str(user.id))
    except:
        s = m_lang.string(conf, user.id, "bio_not_set")
    return s

def increase(conf, user):
    try:
        if int(conf.get("user_level", str(user.id))) == -1:
            return True
        else:
            pt = int(conf.get("user_level", str(user.id))) + 1
            conf.set("user_level", str(user.id), str(pt))
            return True
    except:
        conf.set("user_level", str(user.id), "1")
        return False

def ret_check(conf, user, test_glyph):
    try:
        if test_glyph != "":
            return 99999
        else:
            return int(conf.get("user_level", str(user.id)))
    except:
        return 0

def check(conf, message):
    user = message.author
    try:
        pt = int(conf.get("user_level", str(message.author.id)))
    except:
        pt = 1
    if message.author.display_name == message.author.name:
        usrname = message.author.name + "#" + message.author.discriminator
    else:
        usrname = message.author.display_name + "(" + message.author.name + "#" + message.author.discriminator + ")"
    embed = discord.Embed(title=usrname + " 님의 프로필", color=0xff0080)
    embed.set_thumbnail(url=message.author.avatar_url)
    embed.add_field(name="자기소개", value=get_bio(conf, message.author), inline=False)
    # point text for current level
    if pt >= 5000:
        ptstr = "신의 경지"
    elif pt >= 3000:
        ptstr = "팬"
    elif pt >= 1000:
        ptstr = "파워유저"
    elif pt >= 500:
        ptstr = "애인"
    elif pt >= 300:
        ptstr = "친한 친구"
    elif pt >= 200:
        ptstr = "친구"
    elif pt >= 100:
        ptstr = "더 알아가고 싶은 사람"
    elif pt >= 60:
        ptstr = "저에게 관심이 많은 사람"
    elif pt >= 30:
        ptstr = "한번씩 놀아주는 사람"
    elif pt >= 0:
        ptstr = "안녕하세요!"
    else:
        ptstr = "개발자"
    # point text for next level
    if pt == -1:
        nxtstr = "호감도 최고 레벨이예요!"
    elif pt >= 5000:
        nxtstr = "호감도 최고 레벨이예요!"
    elif pt < 30:
        nxtstr = "한번씩 놀아주는 사람까지 " + str(30 - pt) + " 남음"
    elif pt < 60:
        nxtstr = "저에게 관심이 많은 사람까지 " + str(60 - pt) + " 남음"
    elif pt < 100:
        nxtstr = "더 알아가고 싶은 사람까지 " + str(100 - pt) + " 남음"
    elif pt < 200:
        nxtstr = "친구까지 " + str(200 - pt) + " 남음"
    elif pt < 300:
        nxtstr = "친한 친구까지 " + str(300 - pt) + " 남음"
    elif pt < 500:
        nxtstr = "애인까지 " + str(500 - pt) + " 남음"
    elif pt < 1000:
        nxtstr = "파워유저까지 " + str(1000 - pt) + " 남음"
    elif pt < 3000:
        nxtstr = "팬까지 " + str(3000 - pt) + " 남음"
    elif pt < 5000:
        nxtstr = "신의 경지까지 " + str(5000 - pt) + " 남음"
    embed.add_field(name="호감도", value=ptstr + "(" + str(pt) + ")", inline=True)
    try:
        embed.add_field(name="누적 출석 횟수", value=str(conf.get("attendance", str(user.id))), inline=True)
    except:
        pass
    embed.add_field(name="호감도 목표치", value=nxtstr, inline=True)
    try:
        tr = conf.get("user_tropy", str(message.author.id))
        embed.add_field(name="칭호", value=tr, inline=True)
    except:
        tr = ""
    try:
        hd = conf.get("user_custom_head", str(message.author.id))
        embed.add_field(name="사용자 지정 접두어", value=hd, inline=True)
    except:
        hd = ""
    if pt >= 200:
        try:
            pst = conf.get("etc", "passive_denied")
            if str(message.guild.id) in pst:
                embed.add_field(name="관심 가져주기 패시브", value="현재 서버 설정에 의해 비허용됨", inline=False)
            elif int(conf.get("sudden_hugging", str(message.author.id))) == 1:
                embed.add_field(name="관심 가져주기 패시브", value="켜짐", inline=False)
            else:
                embed.add_field(name="관심 가져주기 패시브", value="꺼짐", inline=False)
        except:
            embed.add_field(name="관심 가져주기 패시브", value="켜짐", inline=False)
    else:
        embed.add_field(name="관심 가져주기 패시브", value=m_lang.string(conf, message.author.id, "insufficient_level"), inline=False)
    embed.add_field(name="언어", value=m_lang.check_lang(conf, message.author.id))
    embed.add_field(name="소지 중인 게임머니", value=gamemoney(conf, message))
    embed.set_footer(text='계정 생성일시 등의 정보 확인 : "루냥아 계정정보"')
    return embed

def check_another(conf, user, message):
    try:
        pt = int(conf.get("user_level", str(user.id)))
    except:
        pt = 1
    if user.display_name == user.name:
        usrname = user.name + "#" + user.discriminator
    else:
        usrname = user.display_name + "(" + user.name + "#" + user.discriminator + ")"
    embed = discord.Embed(title=usrname + " 님의 프로필", color=0xff0080)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="자기소개", value=get_bio(conf, user), inline=False)
    # point text for current level
    if pt == -1:
        ptstr = "개발자"
    elif pt >= 5000:
        ptstr = "신의 경지"
    elif pt >= 3000:
        ptstr = "팬"
    elif pt >= 1000:
        ptstr = "파워유저"
    elif pt >= 500:
        ptstr = "애인"
    elif pt >= 300:
        ptstr = "친한 친구"
    elif pt >= 200:
        ptstr = "친구"
    elif pt >= 100:
        ptstr = "더 알아가고 싶은 사람"
    elif pt >= 60:
        ptstr = "저에게 관심이 많은 사람"
    elif pt >= 30:
        ptstr = "한번씩 놀아주는 사람"
    elif pt >= 0:
        ptstr = "안녕하세요!"
    else:
        ptstr = "개발자"
    embed.add_field(name="호감도", value=ptstr + "(" + str(pt) + ")", inline=True)
    try:
        embed.add_field(name="누적 출석 횟수", value=str(conf.get("attendance", str(user.id))), inline=True)
    except:
        pass
    try:
        tr = conf.get("user_tropy", str(user.id))
        embed.add_field(name="칭호", value=tr, inline=True)
    except:
        tr = ""
    return embed

def accountinfo(conf, user, message, dmchannel):
    if user.display_name == user.name:
        usrname = user.name + "#" + user.discriminator
    else:
        usrname = user.display_name + "(" + user.name + "#" + user.discriminator + ")"
    embed = discord.Embed(title=usrname + " 님의 계정 정보", color=0xff0080)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="유저 ID", value=str(user.id), inline=False)
# ! PRIVILEGED INTENT REQUIRED !
#    if not dmchannel:
#        st = str(user.status)
#        if st == "online":
#            sta = "온라인"
#        elif st == "offline":
#            sta = "오프라인"
#        elif st == "idle":
#            sta = "자리 비움"
#        elif st == "dnd" or st == "do_not_disturb":
#            sta = "방해 금지"
#        embed.add_field(name="현재 상태", value=sta, inline=True)
    if str(user.id) in conf.get("etc", "createdat_nd") and not dmchannel:
        crat = "비공개 설정됨"
    else:
        crat = user.created_at.isoformat()
    embed.add_field(name="Discord 가입 일시", value=crat, inline=True)
    try:
        if str(user.id) in conf.get("etc", "joinedat_nduser"):
            joat = "사용자에 의해 비공개 설정됨"
        elif str(message.guild.id) in conf.get("etc", "joinedat_ndserver"):
            joat = "서버 설정에 의해 비공개 설정됨"
        else:
            joat = user.joined_at.isoformat()
    except:
        pass
    if not dmchannel:
        embed.add_field(name="서버 가입 일시", value=joat, inline=True)
        if user.guild_permissions.administrator:
            usrperm = "서버 관리자"
        else:
            usrperm = "일반"
        embed.add_field(name="서버에서의 권한", value=usrperm, inline=True)
    return embed

def check_allow_sudden_hugging(conf, user):
    try:
        if int(conf.get("sudden_hugging", str(user.id))) == 1:
            return True
        elif int(conf.get("sudden_hugging", str(user.id))) == 0:
            return False
    except:
        conf.set("sudden_hugging", str(user.id), "1")
        return True

def toggle_sudden_hugging(conf, user):
    if user.display_name == user.name:
        usrname = user.name
    else:
        usrname = user.display_name + "(" + user.name + ")"
    try:
        if int(conf.get("sudden_hugging", str(user.id))) == 1:
            conf.set("sudden_hugging", str(user.id), "0")
            res = False
        elif int(conf.get("sudden_hugging", str(user.id))) == 0:
            conf.set("sudden_hugging", str(user.id), "1")
            res = True
    except:
        conf.set("sudden_hugging", str(user.id), "0")
        res = False
    return res

def hug_count(conf, user):
    try:
        pt = int(conf.get("hug_count", str(user.id))) + 1
        conf.set("hug_count", str(user.id), str(pt))
    except:
        conf.set("hug_count", str(user.id), "1")

def check_hug_count(conf, user):
    try:
        return int(conf.get("hug_count", str(user.id)))
    except:
        conf.set("hug_count", str(user.id), "0")
        return 0

def count(conf, user):
    try:
        pt = int(conf.get("count", str(user.id))) + 1
        conf.set("count", str(user.id), str(pt))
    except:
        conf.set("count", str(user.id), "1")

def check_count(conf, user):
    try:
        return int(conf.get("count", str(user.id)))
    except:
        conf.set("count", str(user.id), "1")
        return 1

def reset_count(conf, user):
    conf.set("count", str(user.id), "0")

def serverinfo(conf, message):
    embed=discord.Embed(title=message.guild.name, color=0xffff00)
    embed.set_thumbnail(url=message.guild.icon_url)
    embed.add_field(name="서버 생성 일시", value=message.guild.created_at.isoformat() + "\n지금으로부터 " + str(datetime.datetime.now() - message.guild.created_at) + " 전", inline=True)
    try:
        embed.add_field(name="주인", value=message.guild.owner.name, inline=True)
    except:
        pass
    try:
        #embed.add_field(name="상세 정보", value=str(len(message.guild.members)) + "명의 인원\n" + str(len(message.guild.roles)) + "개의 역할\n" + str(len(message.guild.emojis)) + "개의 서버 커스텀 이모지", inline=True)
        embed.add_field(name="상세 정보", value=str(len(message.guild.roles)) + "개의 역할\n" + str(len(message.guild.emojis)) + "개의 서버 커스텀 이모지", inline=True)
    except:
        pass
    if str(message.guild.id) in conf.get("etc", "ndserver"):
        embed=discord.Embed(title="서버 정보를 볼 수 없습니다", description="서버 설정에 의해 정보를 볼 수 있도록 허용되지 않았습니다", color=0xff0000)
    return embed

def serversettings(conf, message, ifadmin):
    embed=discord.Embed(title=message.guild.name, color=0xffff00)
    if ifadmin:
        embed.add_field(name="서버 코드", value=conf.get("server_code", str(message.guild.id)), inline=True)
    if str(message.guild.id) in conf.get("etc", "ndserver"):
        embed.add_field(name="서버 공개 여부", value="비공개", inline=True)
    else:
        embed.add_field(name="서버 공개 여부", value="공개", inline=True)
    try:
        if int(conf.get("server_count", str(message.guild.id))) >= 0:
            embed.add_field(name="불타는 서버 패시브", value="켜짐", inline=True)
        else:
            embed.add_field(name="불타는 서버 패시브", value="꺼짐", inline=True)
    except:
        embed.add_field(name="불타는 서버 패시브", value="켜짐", inline=True)
    if str(message.guild.id) in conf.get("etc", "passive_denied"):
        embed.add_field(name="유저 패시브", value="비허용", inline=True)
    else:
        embed.add_field(name="유저 패시브", value="허용", inline=True)
    if str(message.guild.id) in conf.get("etc", "joinedat_ndserver"):
        embed.add_field(name="서버 구성원의 가입 일자 공개", value="비허용", inline=True)
    else:
        embed.add_field(name="서버 구성원의 가입 일자 공개", value="허용", inline=True)
    try:
        hd = db.get("custom_head", str(message.guild.id))
        if hd != "루냥아":
            embed.add_field(name="서버 지정 접두사", value=hd, inline=True)
        else:
            embed.add_field(name="서버 지정 접두사", value="없음", inline=True)
    except:
        embed.add_field(name="서버 지정 접두사", value="없음", inline=True)
    try:
        bu = db.get("server_burning", str(message.guild.id))
        embed.add_field(name="불타는 서버 지정 문구", value=bu, inline=True)
    except:
        embed.add_field(name="불타는 서버 지정 문구", value="없음", inline=True)
    if str(message.guild.id) in conf.get("etc", "pingpong_headless"):
        embed.add_field(name="일상대화 접두어", value="불필요", inline=True)
    else:
        embed.add_field(name="일상대화 접두어", value="필수", inline=True)
    if str(message.guild.id) in conf.get("etc", "guild_custom_headless"):
        embed.add_field(name="서버 지정 명령어 접두어", value="불필요", inline=True)
    else:
        embed.add_field(name="서버 지정 명령어 접두어", value="필수", inline=True)
    if str(message.guild.id) in conf.get("permissions", "deny_sleep"):
        embed.add_field(name="잠수 허용", value="아니오", inline=True)
    else:
        embed.add_field(name="잠수 허용", value="예", inline=True)
    if str(message.guild.id) in conf.get("permissions", "deny_megaphone"):
        embed.add_field(name="확성기 허용", value="아니오", inline=True)
    else:
        embed.add_field(name="확성기 허용", value="예", inline=True)
    return embed

def attendance(conf, user):
    # Matt.C : 다시만들게요
    # 완성 시 def 전체 지울것
    a = []
    a = conf.get("attendance", "today").split(", ")
    if str(user.id) in a:
        embed=discord.Embed(title=m_lang.string(conf, user.id, "attendance_already"), description="누적 출석 횟수 : " + str(conf.get("attendance", str(user.id))), color=0xffff00)
    else:
        try:
            c = int(conf.get("attendance", str(user.id)))
            c += 1
            conf.set("attendance", str(user.id), str(c))
            embed=discord.Embed(title=m_lang.string(conf, user.id, "attendance_check"), description="누적 출석 횟수 : " + str(conf.get("attendance", str(user.id))), color=0x00ff00)
        except:
            conf.set("attendance", str(user.id), "1")
            embed=discord.Embed(title=m_lang.string(conf, user.id, "attendance_first"), color=0x00ff00)
        conf.set("attendance", "today", conf.get("attendance", "today") + ", " + str(user.id))
    return embed

def guild_custom_commands(client, db, message, dmchannel):
    try:
        if dmchannel:
            a = db.get("dm_custom_commands", str(message.author.id) + "_" + message.content.replace(head(db, message) + "", ""))
        else:
            a = db.get("custom_commands", str(message.guild.id) + "_" + message.content.replace(head(db, message) + "", ""))
        react = a.split(" | ")[0]
        if react.startswith("custom_embed_bind_"):
            em_code = react.replace("custom_embed_bind_", "")
            em = db.get("custom_embed", em_code)
            eml = em.split(",")
            eml2 = []
            for i in eml:
                eml2.append(m_etc.base64d(i))
            emx = m_custom_embed.convert_to_embed(message, eml2)
            return emx
        if "&&" in react:
            react = react.split("&&")
            react = random.choice(react)
        if not dmchannel:
            react = react.replace("[멘션]", message.author.mention)
            react = react.replace("[이름]", message.author.display_name)
        n = m_etc.get_name(a.split(" | ")[1])
        return react + "\n`작성자 : " + n + "`"
    except Exception as e:
        try:
            c = db.get("link_custom_commands", str(message.guild.id))
            cg = client.get_guild(int(c))
            a = db.get("custom_commands", c + "_" + message.content.replace(head(db, message) + "", ""))
            react = a.split(" | ")[0]
            if react.startswith("custom_embed_bind_"):
                em_code = react.replace("custom_embed_bind_", "")
                em = db.get("custom_embed", em_code)
                eml = em.split(",")
                eml2 = []
                for i in eml:
                    eml2.append(m_etc.base64d(i))
                emx = m_custom_embed.convert_to_embed(message, eml2)
                return emx
            if "&&" in react:
                react = react.split("&&")
                react = random.choice(react)
            react = react.replace("[멘션]", message.author.mention)
            react = react.replace("[이름]", message.author.display_name)
            n = m_etc.get_name(a.split(" | ")[1])
            return react + "\n`서버 : " + cg.name + ", 작성자 : " + n + "`"
        except Exception as e:
            return None

def make_custom_commands(db, message, dmchannel):
    if dmchannel:
        s = str(message.author.id)
        l = dict(db.items("dm_custom_commands"))
    else:
        s = str(message.guild.id)
        l = dict(db.items("custom_commands"))
    n = 0
    for a in l:
        if s in a:
            n += 1
    if n >= 4095:
        embed=discord.Embed(title=m_lang.string(db, message.author.id, "custom_command_limit_exceeded"), color=0xff0000)
    else:
        mr = message.content.replace(head(db, message) + "배워 ", "")
        m = mr.split(" | ")
        editing_m = m_lang.string(db, message.author.id, "custom_command_added")
        if mr.startswith("| ") or mr.startswith(" | ") or mr.endswith(" |") or " | " not in mr:
            embed=discord.Embed(title=m_lang.string(db, message.author.id, "custom_command_no_blank"), color=0xff0000)
        else:
            try:
                i = db.get("custom_commands", str(message.guild.id) + "_" + m[0])
                i = i.split(" | ")[1]
                editing_m = m_lang.string(db, message.author.id, "custom_command_edit")
                if dmchannel == False and message.author.guild_permissions.administrator == False and str(message.author.id) != i:
                    embed=discord.Embed(title=m_lang.string(db, message.author.id, "custom_command_not_edit"), color=0xff000)
                else:
                    raise
            except Exception as e:
                try:
                    try:
                        asdfasdf = int(m[0])
                        embed=discord.Embed(title=m_lang.string(db, message.author.id, "custom_command_no_number_only"), color=0xff000)
                    except:
                        embed=discord.Embed(title=editing_m, color=0xff77ff)
                        if m[1].startswith("임베드 "):
                            mc = m[1].replace("임베드 ", "")
                            try:
                                em = m_custom_embed.get_embed_raw(message, db, mc)
                                embed.add_field(name=m[0], value="커스텀 임베드에 연결됨", inline=False)
                            except:
                                raise NameError
                            if dmchannel:
                                db.set("dm_custom_commands", str(message.author.id) + "_" + m[0], "custom_embed_bind_" + str(message.author.id) + "_" + mc + " | " + str(message.author.id) + " | " + message.author.name)
                            else:
                                db.set("custom_commands", str(message.guild.id) + "_" + m[0], "custom_embed_bind_" + str(message.author.id) + "_" + mc + " | " + str(message.author.id) + " | " + message.author.name)
                        else:
                            if dmchannel:
                                db.set("dm_custom_commands", str(message.author.id) + "_" + m[0], m[1] + " | " + str(message.author.id) + " | " + message.author.name)
                            else:
                                db.set("custom_commands", str(message.guild.id) + "_" + m[0], m[1] + " | " + str(message.author.id) + " | " + message.author.name)
                            if "&&" in m[1]:
                                li = m[1].split("&&")
                                embed.add_field(name=m[0], value=str(len(li)) + "개의 항목 중 랜덤 출현", inline=False)
                            else:
                                embed.add_field(name=m[0], value=m[1], inline=False)
                        embed.set_footer(text="주의 : 배운 명령어는 해당 서버에서만 동작합니다")
                except Exception as e:
                    raise
                    embed=discord.Embed(title='사용 방법 : "루냥아 배워 (명령어) | (반응)"', color=0xffffff)
    return embed

def list_custom_commands(db, message, head, dmchannel):
    try:
        content = message.content.replace(head + "배운거 ", "")
        page = int(content)
    except:
        page = 1
    n = 0
    t = []
    u = []
    if dmchannel:
        s = str(message.author.id)
        l = dict(db.items("dm_custom_commands"))
        for a in l:
            if s in a:
                t.append(a.replace(s + "_", ""))
                usn = db.get("dm_custom_commands", a).split(" | ")[1]
                u.append(str(usn))
                n += 1
    else:
        s = str(message.guild.id)
        l = dict(db.items("custom_commands"))
        for a in l:
            if s in a:
                t.append(a.replace(s + "_", ""))
                usn = db.get("custom_commands", a).split(" | ")[1]
                u.append(str(usn))
                n += 1
    pages = math.ceil(n / 10)
    if page > pages:
        embed=discord.Embed(title=m_lang.string(db, message.author.id, "wrong_page_idx"))
    else:
        c = (page - 1) * 10
        ct = c + 9
        embed=discord.Embed(title="서버 지정 명령어 목록 (총 " + str(n) + "개)", color=0xffffff)
        while c <= ct:
            try:
                embed.add_field(name="#" + str(c+1) + " : " + t[c], value="작성자 : " + m_etc.get_name(u[c]), inline=False)
                c += 1
            except:
                break
        embed.set_footer(text=str(page) + ' / ' + str(pages) + ' 페이지, 다른 페이지 보기 : "루냥아 배운거 (페이지)"')
    return embed

def remove_custom_commands(db, message, dmchannel):
    m = message.content.replace(head(db, message) + "잊어 ", "")
    if not dmchannel:
        l = dict(db.items("custom_commands"))
    if dmchannel:
        try:
            db.get("dm_custom_commands", str(message.author.id) + "_" + m)
            db.remove_option("dm_custom_commands", str(message.author.id) + "_" + m)
            embed=discord.Embed(title=m_lang.string(db, message.author.id, "custom_command_deleted"), color=0xffff00)
        except:
            embed=discord.Embed(title=m_lang.string(db, message.author.id, "custom_command_not_found"), color=0xff0000)
    elif str(message.guild.id) + "_" + m in l:
        i = db.get("custom_commands", str(message.guild.id) + "_" + m)
        i = i.split(" | ")[1]
        if message.author.guild_permissions.administrator or str(message.author.id) == i:
            db.remove_option("custom_commands", str(message.guild.id) + "_" + m)
            embed=discord.Embed(title=m_lang.string(db, message.author.id, "custom_command_deleted"), color=0xffff00)
        else:
            embed=discord.Embed(title=m_lang.string(db, message.author.id, "custom_command_not_deleted"), color=0xff0000)
    else:
        embed=discord.Embed(title=m_lang.string(db, message.author.id, "custom_command_not_found"), color=0xff0000)
    return embed

def info_custom_commands(db, message, dmchannel):
    m = message.content.replace(head(db, message) + "배운거 ", "")
    try:
        if dmchannel:
            d = db.get("dm_custom_commands", str(message.author.id) + "_" + m).split(" | ")
        else:
            d = db.get("custom_commands", str(message.guild.id) + "_" + m).split(" | ")
        w = m_etc.get_name(d[1])
        mm = ""
        if "&&" in d[0]:
            dd = d[0].split("&&")
            for di in dd:
                mm += di + "\n"
        else:
            mm = d[0]
        embed = discord.Embed(title="명령어 " + m + "의 정보")
        embed.add_field(name="작성자", value=w, inline=False)
        embed.add_field(name="반응", value=mm, inline=False)
    except:
        embed=discord.Embed(title=m_lang.string(db, message.author.id, "custom_command_not_found"), color=0xff0000)
    return embed

def sleep(db, message, dt):
    try:
        a = db.get('j_sleep_cooldown', str(message.guild.id) + "_" + str(message.author.id))
        embed=discord.Embed(title=m_lang.string(db, message.author.id, "sleep_cooldown"), description = str(datetime.datetime.fromtimestamp(int(a))) + m_lang.string(db, message.author.id, "sleep_cooldown_desc"), color=0xff0000)
    except:
        embed=discord.Embed(title=str(message.author.name) + m_lang.string(db, message.author.id, "sleep_start"), description = m_lang.string(db, message.author.id, "sleep_start_desc"), color=0xffff00)
        if head(db, message) + "잠수 " in message.content:
            reason = message.content.replace(head(db, message) + "잠수 ", "")
            embed.add_field(name="사유", value=reason, inline=False)
        else:
            reason = "empty"
        db.set("sleep", str(message.author.id) + "&&" + str(message.guild.id), dt.strftime('%s') + "&&" + reason)
    return embed

def check_sleep(db, author, guild):
    try:
        s = db.get("sleep", str(author.id) + "&&" + str(guild.id))
        t = datetime.datetime.now() - datetime.datetime.fromtimestamp(int(s.split("&&")[0]))
        r = s.split("&&")[1]
        if r == "empty":
            return ["사유 없음", t]
        else:
            return [r, t]
    except:
        return None

def unsleep(db, message, dt):
    s = db.get("sleep", str(message.author.id) + "&&" + str(message.guild.id))
    t = datetime.datetime.now() - datetime.datetime.fromtimestamp(int(s.split("&&")[0]))
    r = s.split("&&")[1]
    db.remove_option("sleep", str(message.author.id) + "&&" + str(message.guild.id))
    embed=discord.Embed(title=message.author.name + m_lang.string(db, message.author.id, "sleep_end"), color=0xffff00)
    if r != "empty":
        embed.add_field(name="사유", value=r, inline=False)
    embed.add_field(name="잠수 시간", value=str(t), inline=False)
    te = datetime.datetime.now()
    te = int(te.timestamp())
    if str(message.guild.id) in db.get('etc', 'no_sleep_cooldown'):
        pass
    else:
        db.set('j_sleep_cooldown', str(message.guild.id) + "_" + str(message.author.id), str(te + 300))
        embed.set_footer(text = "다시 잠수를 하시려면 5분 뒤 다시 시도해주세요")
    return embed

def head(db, message, test_glyph=""):
    if test_glyph_2 != "_":
        try:
            hd = db.get("custom_head", str(message.guild.id))
            try:
                hd2 = db.get("user_custom_head", str(message.author.id))
            except:
                hd2 = ""
            if message.content.startswith("루냥아"):
                raise
            elif hd2 != "" and message.content.startswith(hd2):
                return hd2 + " "
            else:
                return hd + " "
        except:
            return "루냥아 "
    else:
        return "루우냥아 "

def get_guild_intro(db, id):
    try:
        i = db.get("guild_intro", id)
        return i
    except:
        return ""

def servers_list(client, page, db, id):
    n = 0
    servers = {}
    sorted_servers = {}
    lk = []
    lu = []
    lo = []
    li = []
    nd = []
    de = 0
    for s in client.guilds:
        # ! PRIVILEGED INTENTS REQUIRED !
        #try:
        #    ownername = s.owner.name
        #except:
        #    ownername = "--정지되었거나 알 수 없는 계정--"
        #if str(s.id) in db.get("etc", "ndserver"):
        #    servers[str(s)] = [str(len(s.members)), ownername, "1", get_guild_intro(db, str(s.id))]
        #else:
        #    servers[str(s)] = [str(len(s.members)), ownername, "0", get_guild_intro(db, str(s.id))]
        if str(s.id) in db.get("etc", "ndserver"):
            servers[str(s)] = [str(len(s.members)), "", "1", get_guild_intro(db, str(s.id))]
        else:
            servers[str(s)] = [str(len(s.members)), "", "0", get_guild_intro(db, str(s.id))]
        n += 1
    sorted_servers = sorted(servers)
    for k in sorted_servers:
        lk.append(k)
        lu.append(servers[k][0])
        #lo.append(servers[k][1])
        nd.append(servers[k][2])
        li.append(servers[k][3])
    pages = math.ceil(len(lk) / 10)
    if page > pages or page <= 0:
        embed=discord.Embed(title=m_lang.string(db, id, "wrong_page_idx"))
    else:
        #embed=discord.Embed(title="전체 서버 목록 (총 " + str(len(lk)) + "개)", color=0xff00ff)
        c = (page - 1) * 10
        ct = c + 9
        st = ""
        while c <= ct:
            try:
                if nd[c] == "1":
#                    embed.add_field(name="#" + str(c+1) + " : (숨겨짐)", inline=False)
                    de += 1
                else:
                    if li[c] == "":
                        #embed.add_field(name="#" + str(c+1) + " : " + lk[c], value="유저 수 : " + lu[c] + ", 서버 주인 : " + lo[c], inline=False)
                        st += "#" + str(c+1) + " : " + lk[c] + "\n"
                    else:
                        #embed.add_field(name="#" + str(c+1) + " : " + lk[c], value=li[c] + "\n유저 수 : " + lu[c] + ", 서버 주인 : " + lo[c], inline=False)
                        st += "#" + str(c+1) + " : " + lk[c] + "\n"
                c += 1
            except:
                break
        embed=discord.Embed(title="전체 서버 목록 (총 " + str(len(lk)) + "개)", description="```" + st + "```", color=0xff00ff)
        embed.set_footer(text=str(page) + ' / ' + str(pages) + ' 페이지, 다른 페이지 보기 : "루냥아 서버목록 (페이지)"')
    return embed

def servers_rank_users(client, db, page):
    servers = {}
    sorted_servers = {}
    n = 0
    for s in client.guilds:
        if str(s.id) in db.get("etc", "ndserver"):
            continue
        else:
            servers[n] = [s.name, len(s.members), s.owner.name]
        n += 1
    sorted_servers = sorted(servers.items(), key=lambda x: x[1][1], reverse=True)
    pages = math.ceil(len(servers) / 10)
    if page > pages or page <= 0:
        embed=discord.Embed(title=m_lang.string(db, id, "wrong_page_idx"))
    else:
        embed=discord.Embed(title="서버 멤버 수 랭킹", color=0xff00ff)
        embed.set_footer(text=str(page) + ' / ' + str(pages) + ' 페이지, 다른 페이지 보기 : "루냥아 서버랭킹 (페이지)"')
        c = (page - 1) * 10
        ct = c + 9
        while c <= ct:
            try:
                embed.add_field(name=str(c+1) + "등 : " + str(sorted_servers[c][1][0]), value="유저 수 : " + str(sorted_servers[c][1][1]) + ", 서버 주인 : " + str(sorted_servers[c][1][2]), inline=False)
                c += 1
            except:
                break
    return embed

def level_rank(client, db):
    users = {}
    converted_users = {}
    sorted_users = {}
    n = 0
    for i in db.items('user_level'):
        if i[1] == '2147483647' or i[0] == str(client.user.id):
            continue
        else:
            converted_users[n] = [m_etc.get_name(i[0]), int(i[1])]
        n += 1
    sorted_users = sorted(converted_users.items(), key=lambda x: x[1][1], reverse=True)
    embed=discord.Embed(title="호감도 랭킹", color=0xff00ff)
    c = 0
    while c <= 9:
        try:
            embed.add_field(name=str(c+1) + "등 : " + str(sorted_users[c][1][0]), value="호감도 : " + str(sorted_users[c][1][1]), inline=False)
            c += 1
        except:
            break
    return embed

def suggest_commands(db, message, dt):
    if not sdb.has_section(str(message.author.id)):
        sdb.add_section(str(message.author.id))
        sdb.set(str(message.author.id), "meta_name", message.author.name)
    if len(sdb.items(str(message.author.id))) >= 10:
        embed = discord.Embed(m_lang.string(db, message.author.id, "too_much_suggest"))
        embed.set_footer(text='제안 보기 : "루냥아 제안 목록", 제안 전체 삭제 : "루냥아 제안 삭제"')
    else:
        mr = message.content.replace(head(db, message) + "제안 ", "")
        sdb.set(str(message.author.id), str(dt), mr)
        embed = discord.Embed(title=m_lang.string(db, message.author.id, "suggest_command"), description=mr)
        embed.set_footer(text="운영자의 검토 이후 추가됩니다")
        with open(sdb_path, 'w') as configfile:
            sdb.write(configfile)
    return embed

def list_suggests(db, message):
    if not sdb.has_section(str(message.author.id)):
        embed=discord.Embed(title=m_lang.string(db, message.author.id, "no_suggest"))
    else:
        cc = 1
        embed=discord.Embed(title=message.author.name + " 님의 제안 목록")
        for c in sdb.items(str(message.author.id)):
            if c[0] != 'meta_name':
                embed.add_field(name="#" + str(cc), value=c[1], inline=False)
                cc += 1
    return embed

def purge_suggests(db, message):
    if not sdb.has_section(str(message.author.id)):
        embed=discord.Embed(title=m_lang.string(db, message.author.id, "no_suggest"))
    else:
        sdb.remove_section(str(message.author.id))
        embed=discord.Embed(title=m_lang.string(db, message.author.id, "purged_suggest"))
        with open(sdb_path, 'w') as configfile:
            sdb.write(configfile)
    return embed

def suggest_food(db, message, dt):
    m = message.content.replace(head(db, message) + "음식제안 ", "")
    sdb.set("food_suggests", str(message.author.id) + "_" + str(int(dt.timestamp())), m)
    embed = discord.Embed(title=m_lang.string(db, message.author.id, "suggest_food"), description=m)
    embed.set_footer(text="운영자의 검토 이후 추가됩니다")
    with open(sdb_path, 'w') as configfile:
        sdb.write(configfile)
    return embed

def set_lotto_number(db, message, dt):
    if gamemoney(db, message) < 10:
        embed=discord.Embed(title=m_lang.string(db, message.author.id, "not_enough_gamemoney"), desctiption=m_lang.string(db, message.author.id, "not_enough_gamemoney_desc"))
    else:
        gamemoney(db, message, -10)
        m = message.content.replace(head(db, message) + "로또 ", "")
        li = m.split(" ")
        if len(li) != 6:
            embed=discord.Embed(title=m_lang.string(db, message.author.id, "lotto_invalid_count"))
        else:
            try:
                lo = []
                sl = ""
                for s in li:
                    if int(s) in lo:
                        embed=discord.Embed(title=m_lang.string(db, message.author.id, "lotto_multiple_copy"))
                        return embed
                    elif int(s) > 45 or int(s) < 1:
                        embed=discord.Embed(title=m_lang.string(db, message.author.id, "lotto_invalid_number"))
                        return embed
                    else:
                        lo.append(int(s))
                for s in lo:
                    sl += str(s) + ","
                try:
                    tmp = db.get("lotto", str(message.author.id))
                    embed=discord.Embed(title=m_lang.string(db, message.author.id, "lotto_edit_successful"))
                    embed.set_footer(text='당첨 결과 확인 : "루냥아 로또 결과"')
                except:
                    embed=discord.Embed(title=m_lang.string(db, message.author.id, "lotto_successful"))
                    embed.set_footer(text='당첨 결과 확인 : "루냥아 로또 결과"')
                db.set("lotto", str(message.author.id), sl + str(dt.year) + "," + str(dt.month) + "," + str(dt.day))
            except Exception as e:
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "lotto_not_a_number"))
    return embed

def autolotto(db, message, dt):
    if gamemoney(db, message) < 10:
        embed=discord.Embed(title=m_lang.string(db, message.author.id, "not_enough_gamemoney"), desctiption=m_lang.string(db, message.author.id, "not_enough_gamemoney_desc"))
    else:
        gamemoney(db, message, -10)
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
        db.set("lotto", str(message.author.id), lotto_numbers_str + str(dt.year) + "," + str(dt.month) + "," + str(dt.day))
        embed=discord.Embed(title=m_lang.string(db, message.author.id, "lotto_successful"))
        embed.add_field(name="로또 번호", value=lotto_numbers_str[:-1])
        embed.set_footer(text='당첨 결과 확인 : "루냥아 로또 결과"')
    return embed

def get_lotto(db, message, dt, lotto_meta, lotto_dt):
    try:
        l_raw = db.get("lotto", str(message.author.id))
        l_li = l_raw.split(",")
        l_num = l_li[:6]
        l_dt = l_li[6:]
        m_num = lotto_meta.split(",")
        m_dt = lotto_dt.split(",")
        matches = 0
        m_txt = ""
        for i in l_num:
            m_txt += i + ","
        m_txt = m_txt[:-1]
        if l_dt[0] == m_dt[0] and l_dt[1] == m_dt[1] and l_dt[2] == m_dt[2]:
            for i in l_num:
                if i in m_num:
                    matches += 1
        else:
            embed=discord.Embed(title=m_lang.string(db, message.author.id, "lotto_not_attended"))
            return embed
        if matches >= 4:
            res = "1등!"
            gamemoney(db, message, 10000)
        elif matches == 3:
            res = "2등!"
            gamemoney(db, message, 5000)
        elif matches == 2:
            res = "3등!"
            gamemoney(db, message, 1000)
        elif matches <= 1:
            res = "꽝!"
        embed=discord.Embed(title=message.author.name + " 님의 금일 로또 결과")
        embed.add_field(name="응모한 번호", value=m_txt, inline=False)
        embed.add_field(name="갱신된 번호", value=lotto_meta, inline=False)
        embed.add_field(name="결과", value=res, inline=False)
        return embed
    except Exception as e:
        embed=discord.Embed(title=m_lang.string(db, message.author.id, "lotto_not_attended"))
        return embed

def gamemoney(db, message, amount=0):
    try:
        gm = int(db.get("gamemoney", str(message.author.id)))
    except:
        gm = 1000
    if amount != 0:
        gm += amount
        db.set("gamemoney", str(message.author.id), str(gm))
    return gm

def write_posts(db, message, head):
    if message.content == head + "포스트 작성":
        embed=discord.Embed(title="사용 방법 : 루냥아 포스트 작성 (임베드 코드)")
    else:
        try:
            m = str(message.author.id) + "_" + message.content.replace(head + "포스트 작성 ", "")
            em = m_custom_embed.get_embed_raw(message, db, m)
            emx = m_custom_embed.convert_to_embed(message, em)
            emt = emx.title
            while True:
                code = random.randint(1,9999)
                try:
                    _ = db.get("posts", str(message.author.id) + "_" + str(code))
                    continue
                except:
                    db.set("posts", str(message.author.id) + "_" + str(code), str(message.author.id) + "_" + message.content.replace(head + "포스트 작성 ", ""))
                    break
            embed=discord.Embed(title=m_lang.string(db, message.author.id, "post_uploaded"), description=m_lang.string(db, message.author.id, "post_uploaded_desc"))
        except:
            embed=discord.Embed(title=m_lang.string(db, message.author.id, "no_such_custom_embed_title"), description=m_lang.string(db, message.author.id, "no_such_custom_embed_desc"))
    return embed

def list_posts(db, message, head):
    try:
        content = message.content.replace(head + "포스트 목록 ", "")
        page = int(content)
    except:
        page = 1
    l = db.items("posts")
    n = 0
    lu = []
    lt = []
    for i in l:
        lx = i[0].split("_")
        lu.append(m_etc.get_name(lx[0]))
        ltx = i[1]
        em = m_custom_embed.get_embed_raw(message, db, ltx)
        emx = m_custom_embed.convert_to_embed(message, em)
        lt.append(emx.title)
        n += 1
    pages = math.ceil(n / 10)
    if page > pages:
        embed=discord.Embed(title=m_lang.string(db, message.author.id, "wrong_page_idx"))
    else:
        lu.reverse()
        lt.reverse()
        c = (page - 1) * 10
        ct = c + 9
        embed=discord.Embed(title="포스트 목록 (총 " + str(n) + "개)", color=0xffffff)
        while c <= ct:
            try:
                embed.add_field(name="#" + str(c+1) + " : " + lt[c], value="작성자 : " + lu[c], inline=False)
                c += 1
            except:
                break
        embed.set_footer(text=str(page) + ' / ' + str(pages) + ' 페이지, 다른 페이지 보기 : "루냥아 포스트 목록 (페이지)"')
    return embed

def view_posts(db, message, head):
    try:
        content = message.content.replace(head + "포스트 ", "")
        pnum = int(content)
    except:
        embed=discord.Embed(title=m_lang.string(db, message.author.id, "no_such_post_title"), description=m_lang.string(db, message.author.id, "no_such_post_desc"))
        return embed
    l = db.items("posts")
    lx = []
    for i in l:
        lx.append(i[1])
    lx.reverse()
    try:
        m = lx[pnum-1]
        em = m_custom_embed.get_embed_raw(message, db, m)
        emx = m_custom_embed.convert_to_embed(message, em)
        return emx
    except:
        embed=discord.Embed(title=m_lang.string(db, message.author.id, "no_such_post_title"), description=m_lang.string(db, message.author.id, "no_such_post_desc"))
        return embed

def search_posts(db, message, head):
    if message.content == head + "포스트 검색 ":
        embed=discord.Embed(title="사용 방법 : 루냥아 포스트 검색 (검색어)")
        return embed
    else:
        content = message.content.replace(head + "포스트 검색 ", "")
        l = db.items("posts")
        n = 0
        lx = []
        for i in l:
            lx = i[0].split("_")
            ltx = i[1]
            em = m_custom_embed.get_embed_raw(message, db, ltx)
            emx = m_custom_embed.convert_to_embed(message, em)
            lx.append([str(n+1), m_etc.get_name(lx[0]), emx.title])
            n += 1
        lxf = []
        for lxi in lx:
            if content in lxi[2]:
                lxf.append(lxi)
        if not lxf:
            embed=discord.Embed(title=m_lang.string(db, message.author.id, "not_found_anything"))
        else:
            lxf.reverse()
            embed=discord.Embed(title="검색 결과 : " + content, color=0xffffff)
            for lxx in lx:
                embed.add_field(name="#" + lxx[0] + " : " + lxx[2], value="작성자 : " + lxx[1], inline=False)
        return embed

def dday_add(db, message, head):
    if message.content == head + "디데이 추가":
        embed=discord.Embed(title="사용 방법 : 루냥아 디데이 추가 (0000-00-00) (이름)")
        embed.set_footer(text="이름을 '생일'로 지정하면 당일 루냥이를 처음 사용할 때 축하해줄 수 있습니다")
    else:
        try:
            content = message.content.replace(head + "디데이 추가 ", "")
            lst = content.split(" ")[0]
            nam_r = content.split(" ")[1:]
            nam = ""
            for i in nam_r:
                nam += i + " "
            nam = nam[:-1]
            datetime.datetime.strptime(lst, '%Y-%m-%d') # 날짜값 검사
            db.set("dday", str(message.author.id) + "_" + nam, lst)
            if nam == "생일":
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "bday_set"), description="이름 : " + nam + "\n날짜 : " + lst)
            else:
                embed=discord.Embed(title=m_lang.string(db, message.author.id, "dday_set"), description="이름 : " + nam + "\n날짜 : " + lst)
        except Exception as e:
            print(e)
            embed=discord.Embed(title="사용 방법 : 루냥아 디데이 추가 (0000-00-00) (이름)")
            embed.set_footer(text="이름을 '생일'로 지정하면 당일 루냥이를 처음 사용할 때 축하해줄 수 있습니다")
    return embed

def dday_list(db, message, head):
    try:
        content = message.content.replace(head + "디데이 ", "")
        page = int(content)
    except:
        page = 1
    l = db.items("dday")
    lx = []
    for i in l:
        if i[0].startswith(str(message.author.id) + "_"):
            lx.append([i[0].replace(str(message.author.id) + "_", ""), i[1]])
    if len(lx) == 0:
        embed=discord.Embed(title=m_lang.string(db, message.author.id, "not_found_anything"))
    else:
        # 디데이 리스팅
        # [[이름, 날짜] [이름 날짜]..]
        c = (page - 1) * 10
        ct = c + 9
        pages = math.ceil(len(lx) / 10)
        embed=discord.Embed(title="디데이 목록 (총 " + str(len(lx)) + "개)", color=0xffffff)
        while c <= ct:
            try:
                # 날짜 계산
                do = datetime.datetime.strptime(lx[c][1], '%Y-%m-%d').date()
                dt = datetime.datetime.now().date()
                ds = relativedelta(dt, do)
                dss = '%s년 %s월 %s일' %(ds.years, ds.months, ds.days)
                # 임베드 내 리스트에 표기
                embed.add_field(name="#" + str(c+1) + " : " + lx[c][0], value="날짜 : " + lx[c][1] + " (" + dss + ")", inline=False)
                c += 1
            except:
                break
        embed.set_footer(text=str(page) + ' / ' + str(pages) + ' 페이지, 다른 페이지 보기 : "루냥아 디데이 (페이지)"')
    return embed

def dday_del(db, message, head):
    if message.content == head + "디데이 삭제":
        embed=discord.Embed(title="사용 방법 : 루냥아 디데이 삭제 (번호)")
        embed.set_footer(text="번호는 '루냥아 디데이 목록'에서 확인 가능")
    else:
        try:
            idx = int(message.content.replace(head + "디데이 삭제 ", ""))
            l = db.items("dday")
            lx = []
            for i in l:
                if i[0].startswith(str(message.author.id) + "_"):
                    lx.append(i[0])
            db.remove_option("dday", lx[idx-1])
            lxs = lx[idx-1].replace(str(message.author.id) + "_", "")
            embed=discord.Embed(title=m_lang.string(db, message.author.id, "dday_deleted").replace("{1}", lxs))
        except:
            embed=discord.Embed(title=m_lang.string(db, message.author.id, "wrong_idx"))
    return embed
import discord, random, datetime, m_namebase

def set_bio(conf, user, text):
    conf.set("bio", str(user.id), text)

def get_bio(conf, user):
    try:
        s = conf.get("bio", str(user.id))
    except:
        s = '자기소개가 설정되지 않았어요!\n"루냥아 소개말 (자기소개)"로 등록할 수 있어요!'
    return s

def increase(conf, user):
    try:
        if int(conf.get("user_level", str(user.id))) < 999999999:
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
    try:
        pt = int(conf.get("user_level", str(message.author.id)))
    except:
        pt = 1
    if message.author.display_name == message.author.name:
        usrname = message.author.name
    else:
        usrname = message.author.display_name + "(" + message.author.name + ")"
    embed = discord.Embed(title=usrname + " 님의 프로필", color=0xff0080)
    embed.set_thumbnail(url=message.author.avatar_url)
    embed.add_field(name="자기소개", value=get_bio(conf, message.author), inline=False)
    # point text for current level
    if pt == 2147483647:
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
    else:
        ptstr = "안녕하세요!"
    # point text for next level
    if pt >= 5000:
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
    embed.add_field(name="호감도 목표치", value=nxtstr, inline=True)
    try:
        tr = conf.get("user_tropy", str(message.author.id))
        embed.add_field(name="칭호", value=tr, inline=True)
    except:
        tr = ""
    embed.add_field(name="Discord 가입 일시", value=message.author.created_at.isoformat(), inline=True)
    embed.add_field(name="서버 가입 일시", value=message.author.joined_at.isoformat(), inline=True)
    if message.author.guild_permissions.administrator:
        usrperm = "서버 관리자"
    else:
        usrperm = "일반"
    embed.add_field(name="서버에서의 권한", value=usrperm, inline=True)
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
        embed.add_field(name="관심 가져주기 패시브", value="호감도를 200까지 획득해주세요!", inline=False)
    return embed

def check_another(conf, user):
    try:
        pt = int(conf.get("user_level", str(user.id)))
    except:
        pt = 1
    if user.display_name == user.name:
        usrname = user.name
    else:
        usrname = user.display_name + "(" + user.name + ")"
    embed = discord.Embed(title=usrname + " 님의 프로필", color=0xff0080)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="자기소개", value=get_bio(conf, user), inline=False)
    # point text for current level
    if pt == 2147483647:
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
    else:
        ptstr = "안녕하세요!"
    embed.add_field(name="호감도", value=ptstr + "(" + str(pt) + ")", inline=True)
    try:
        tr = conf.get("user_tropy", str(user.id))
        embed.add_field(name="칭호", value=tr, inline=True)
    except:
        tr = ""
    embed.add_field(name="Discord 가입 일시", value=user.created_at.isoformat(), inline=True)
    try:
        embed.add_field(name="서버 가입 일시", value=user.joined_at.isoformat(), inline=True)
        if user.guild_permissions.administrator:
            usrperm = "서버 관리자"
        else:
            usrperm = "일반"
    except:
        pass
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
            embed = discord.Embed(title=usrname + " 님에게 관심 가져주기를 껐어요!")
        elif int(conf.get("sudden_hugging", str(user.id))) == 0:
            conf.set("sudden_hugging", str(user.id), "1")
            embed = discord.Embed(title=usrname + " 님에게 관심 가져주기를 켰어요!")
    except:
        conf.set("sudden_hugging", str(user.id), "0")
        embed = discord.Embed(title=usrname + " 님에게 관심 가져주기를 껐어요!")
    return embed

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
    embed.add_field(name="서버 생성 일시", value=message.guild.created_at.isoformat(), inline=True)
    embed.add_field(name="주인", value=message.guild.owner.name, inline=True)
    embed.add_field(name="서버 지역", value=str(message.guild.region), inline=True)
    embed.add_field(name="서버 인원 수", value=str(len(message.guild.members)), inline=True)
    embed.add_field(name="역할 수", value=str(len(message.guild.roles)), inline=True)
    embed.add_field(name="채널 수", value=str(len(message.guild.channels)), inline=True)
    embed.add_field(name="커스텀 이모지 수", value=str(len(message.guild.emojis)), inline=True)
    if message.guild.mfa_level == 1:
        mfa = "예"
    else:
        mfa = "아니오"
    embed.add_field(name="서버 2차 인증", value=mfa, inline=True)
    try:
        if int(conf.get("server_count", str(message.guild.id))) >= 0:
            embed.add_field(name="불타는 서버 패시브", value="켜짐", inline=False)
        else:
            embed.add_field(name="불타는 서버 패시브", value="꺼짐", inline=False)
    except:
        embed.add_field(name="불타는 서버 패시브", value="켜짐", inline=False)
    pst = conf.get("etc", "passive_denied")
    if str(message.guild.id) in pst:
        embed.add_field(name="유저 패시브", value="비허용", inline=False)
    else:
        embed.add_field(name="유저 패시브", value="허용", inline=False)
    return embed

def attendance(conf, user):
    a = []
    try:
        a = conf.get("attendance", "today").split(", ")
        if str(user.id) in a:
            embed=discord.Embed(title="오늘 이미 출석을 했어요!", description="누적 출석 횟수 : " + str(conf.get("attendance", str(user.id))), color=0xffff00)
        else:
            raise
    except:
        try:
            c = int(conf.get("attendance", str(user.id)))
            c += 1
            conf.set("attendance", str(user.id), str(c))
            embed=discord.Embed(title="출석 체크를 했어요!", description="누적 출석 횟수 : " + str(conf.get("attendance", str(user.id))), color=0x00ff00)
        except:
            conf.set("attendance", str(user.id), "1")
            embed=discord.Embed(title="처음으로 출석체크를 했어요!", color=0x00ff00)
        conf.set("attendance", "today", conf.get("attendance", "today") + ", " + str(user.id))
    return embed

def guild_custom_commands(db, message):
    try:
        a = db.get("custom_commands", str(message.guild.id) + "_" + message.content.replace("루냥아 ", ""))
        react = a.split(" | ")[0]
        if "&&" in react:
            react = react.split("&&")
            react = random.choice(react)
        react = react.replace("[멘션]", message.author.mention)
        react = react.replace("[이름]", message.author.display_name)
        return react
    except:
        return None

def make_custom_commands(db, message):
    m = message.content.replace("루냥아 배워 ", "")
    try:
        m = m.split(" | ")
        db.set("custom_commands", str(message.guild.id) + "_" + m[0], m[1] + " | " + str(message.author.id) + " | " + message.author.name)
        embed=discord.Embed(title="명령어를 배웠어요!", color=0xff77ff)
        if "&&" in m[1]:
            li = m[1].split("&&")
            embed.add_field(name=m[0], value=str(len(li)) + "개의 항목 중 랜덤 출현", inline=False)
        else:
            embed.add_field(name=m[0], value=m[1], inline=False)
        embed.set_footer(text="주의 : 배운 명령어는 해당 서버에서만 동작합니다")
    except:
        embed=discord.Embed(title='사용 방법 : "루냥아 배워 (명령어) | (반응)"', color=0xffffff)
    return embed

def list_custom_commands(db, message):
    s = str(message.guild.id)
    l = dict(db.items("custom_commands"))
    embed=discord.Embed(title="서버 지정 명령어 목록", color=0xffffff)
    for a in l:
        if s in a:
            tit = a.replace(s + "_", "")
            usr = m_namebase.get_name(db.get("custom_commands", a).split(" | ")[1])
            embed.add_field(name=tit, value="작성자 : " + usr, inline=False)
    return embed

def remove_custom_commands(db, message):
    m = message.content.replace("루냥아 잊어 ", "")
    l = dict(db.items("custom_commands"))
    if str(message.guild.id) + "_" + m in l:
        i = db.get("custom_commands", str(message.guild.id) + "_" + m)
        i = i.split(" | ")[1]
        if message.author.guild_permissions.administrator or str(message.author.id) == i:
            db.remove_option("custom_commands", str(message.guild.id) + "_" + m)
            embed=discord.Embed(title="명령어를 잊었어요!", color=0xffff00)
        else:
            embed=discord.Embed(title="다른 사람이 가르친 명령어는 잊을 수 없어요!", color=0xff0000)
    else:
        embed=discord.Embed(title="명령어가 존재하지 않아요!", color=0xff0000)
    return embed

def sleep(db, message, dt):
    embed=discord.Embed(title=str(message.author.name) + "님의 잠수가 시작되었어요!", description = "현재 서버에 메시지를 남기기 전까지 잠수 시간이 기록됩니다", color=0xffff00)
    if "루냥아 잠수 " in message.content:
        reason = message.content.replace("루냥아 잠수 ", "")
        embed.add_field(name="사유", value=reason, inline=False)
    else:
        reason = "empty"
    db.set("sleep", str(message.author.id) + "&&" + str(message.guild.id), dt.strftime('%s') + "&&" + reason)
    return embed

def check_sleep(db, message):
    try:
        db.get("sleep", str(message.author.id) + "&&" + str(message.guild.id))
        return True
    except:
        return False

def unsleep(db, message, dt):
    s = db.get("sleep", str(message.author.id) + "&&" + str(message.guild.id))
    t = datetime.datetime.now() - datetime.datetime.fromtimestamp(int(s.split("&&")[0]))
    r = s.split("&&")[1]
    db.remove_option("sleep", str(message.author.id) + "&&" + str(message.guild.id))
    embed=discord.Embed(title=message.author.name + " 님의 잠수가 끝났어요!", color=0xffff00)
    if r != "empty":
        embed.add_field(name="사유", value=r, inline=False)
    embed.add_field(name="잠수 시간", value=str(t), inline=False)
    return embed

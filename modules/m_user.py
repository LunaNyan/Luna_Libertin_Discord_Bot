import math, discord, random, datetime, m_etc, m_lang

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
    return embed

def check_another(conf, user, message):
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
    return embed

def accountinfo(conf, user, message):
    if user.display_name == user.name:
        usrname = user.name
    else:
        usrname = user.display_name + "(" + user.name + ")"
    embed = discord.Embed(title=usrname + " 님의 계정 정보", color=0xff0080)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="유저 ID", value=str(user.id), inline=False)
    st = str(user.status)
    if st == "online":
        sta = "온라인"
    elif st == "offline":
        sta = "오프라인"
    elif st == "idle":
        sta = "자리 비움"
    elif st == "dnd" or st == "do_not_disturb":
        sta = "방해 금지"
    embed.add_field(name="현재 상태", value=sta, inline=True)
    if str(user.id) in conf.get("etc", "createdat_nd"):
        crat = "비공개 설정됨"
    else:
        crat = user.created_at.isoformat()
    embed.add_field(name="Discord 가입 일시", value=crat, inline=True)
    if str(user.id) in conf.get("etc", "joinedat_nduser"):
        joat = "사용자에 의해 비공개 설정됨"
    elif str(message.guild.id) in conf.get("etc", "joinedat_ndserver"):
        joat = "서버 설정에 의해 비공개 설정됨"
    else:
        joat = user.joined_at.isoformat()
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
    embed.add_field(name="주인", value=message.guild.owner.name, inline=True)
    embed.add_field(name="상세 정보", value=str(len(message.guild.members)) + "명의 인원\n" + str(len(message.guild.roles)) + "개의 역할\n" + str(len(message.guild.emojis)) + "개의 서버 커스텀 이모지", inline=True)
    if str(message.guild.id) in conf.get("etc", "ndserver"):
        embed=discord.Embed(title="서버 정보를 볼 수 없습니다", description="서버 설정에 의해 정보를 볼 수 있도록 허용되지 않았습니다", color=0xff0000)
    return embed

def serversettings(conf, message):
    embed=discord.Embed(title=message.guild.name, color=0xffff00)
    if str(message.guild.id) in conf.get("etc", "ndserver"):
        embed.add_field(name="서버 공개 여부", value="비공개", inline=False)
    else:
        embed.add_field(name="서버 공개 여부", value="공개", inline=False)
    try:
        if int(conf.get("server_count", str(message.guild.id))) >= 0:
            embed.add_field(name="불타는 서버 패시브", value="켜짐", inline=False)
        else:
            embed.add_field(name="불타는 서버 패시브", value="꺼짐", inline=False)
    except:
        embed.add_field(name="불타는 서버 패시브", value="켜짐", inline=False)
    if str(message.guild.id) in conf.get("etc", "passive_denied"):
        embed.add_field(name="유저 패시브", value="비허용", inline=False)
    else:
        embed.add_field(name="유저 패시브", value="허용", inline=False)
    if str(message.guild.id) in conf.get("etc", "joinedat_ndserver"):
        embed.add_field(name="서버 구성원의 가입 일자 공개", value="비허용", inline=False)
    else:
        embed.add_field(name="서버 구성원의 가입 일자 공개", value="허용", inline=False)
    try:
        hd = db.get("custom_head", str(message.guild.id))
        if hd != "루냥아":
            embed.add_field(name="서버 지정 접두사", value=hd, inline=False)
        else:
            embed.add_field(name="서버 지정 접두사", value="없음", inline=False)
    except:
        embed.add_field(name="서버 지정 접두사", value="없음", inline=False)
    try:
        bu = db.get("server_burning", str(message.guild.id))
        embed.add_field(name="불타는 서버 지정 문구", value=bu, inline=False)
    except:
        embed.add_field(name="불타는 서버 지정 문구", value="없음", inline=False)
    if str(message.guild.id) in conf.get("etc", "pingpong_headless"):
        embed.add_field(name="일상대화 접두어", value="불필요", inline=False)
    else:
        embed.add_field(name="일상대화 접두어", value="필수", inline=False)
    if str(message.guild.id) in conf.get("etc", "guild_custom_headless"):
        embed.add_field(name="서버 지정 명령어 접두어", value="불필요", inline=False)
    else:
        embed.add_field(name="서버 지정 명령어 접두어", value="필수", inline=False)
    return embed

def attendance(conf, user):
    a = []
    try:
        a = conf.get("attendance", "today").split(", ")
        if str(user.id) in a:
            embed=discord.Embed(title=m_lang.string(conf, user.id, "attendance_already"), description="누적 출석 횟수 : " + str(conf.get("attendance", str(user.id))), color=0xffff00)
        else:
            raise
    except:
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

def guild_custom_commands(db, message):
    try:
        a = db.get("custom_commands", str(message.guild.id) + "_" + message.content.replace(head(db, message) + "", ""))
        react = a.split(" | ")[0]
        if "&&" in react:
            react = react.split("&&")
            react = random.choice(react)
        react = react.replace("[멘션]", message.author.mention)
        react = react.replace("[이름]", message.author.display_name)
        n = m_etc.get_name(a.split(" | ")[1])
        return react + "\n`작성자 : " + n + "`"
    except:
        return None

def make_custom_commands(db, message):
    m = message.content.replace(head(db, message) + "배워 ", "")
    m = m.split(" | ")
    editing_m = m_lang.string(db, message.author.id, "custom_command_added")
    try:
        i = db.get("custom_commands", str(message.guild.id) + "_" + m[0])
        i = i.split(" | ")[1]
        editing_m = m_lang.string(db, message.author.id, "custom_command_edit")
        if message.author.guild_permissions.administrator == False and str(message.author.id) != i:
            embed=discord.Embed(title=m_lang.string(db, message.author.id, "custom_command_not_edit"), color=0xff000)
        else:
            raise
    except Exception as e:
        try:
            db.set("custom_commands", str(message.guild.id) + "_" + m[0], m[1] + " | " + str(message.author.id) + " | " + message.author.name)
            embed=discord.Embed(title=editing_m, color=0xff77ff)
            if "&&" in m[1]:
                li = m[1].split("&&")
                embed.add_field(name=m[0], value=str(len(li)) + "개의 항목 중 랜덤 출현", inline=False)
            else:
                embed.add_field(name=m[0], value=m[1], inline=False)
            embed.set_footer(text="주의 : 배운 명령어는 해당 서버에서만 동작합니다")
        except:
            embed=discord.Embed(title='사용 방법 : "루냥아 배워 (명령어) | (반응)"', color=0xffffff)
    return embed

def list_custom_commands(db, message, head):
    try:
        content = message.content.replace(head + "배운거 ", "")
        page = int(content)
    except:
        page = 1
    s = str(message.guild.id)
    l = dict(db.items("custom_commands"))
    n = 0
    t = []
    u = []
    for a in l:
        if s in a:
            t.append(a.replace(s + "_", ""))
            usn = db.get("custom_commands", a).split(" | ")[1]
            u.append(str(usn))
            n += 1
    pages = math.ceil(n / 10)
    if page > pages or page <= 0:
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

def remove_custom_commands(db, message):
    m = message.content.replace(head(db, message) + "잊어 ", "")
    l = dict(db.items("custom_commands"))
    if str(message.guild.id) + "_" + m in l:
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

def sleep(db, message, dt):
    embed=discord.Embed(title=str(message.author.name) + m_lang.string(db, message.author.id, "sleep_start"), description = m_lang.string(db, message.author.id, "sleep_start_desc"), color=0xffff00)
    if head(db, message) + "잠수 " in message.content:
        reason = message.content.replace(head(db, message) + "잠수 ", "")
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
    embed=discord.Embed(title=message.author.name + m_lang.string(db, message.author.id, "sleep_end"), color=0xffff00)
    if r != "empty":
        embed.add_field(name="사유", value=r, inline=False)
    embed.add_field(name="잠수 시간", value=str(t), inline=False)
    return embed

def head(db, message, test_glyph=""):
    if test_glyph != "_":
        try:
            hd = db.get("custom_head", str(message.guild.id))
            if message.content.startswith("루냥아"):
                raise
            else:
                return hd + " "
        except:
            return "루냥아 "
    else:
        return "루우냥아 "

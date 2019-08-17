import discord

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
        if int(conf.get("user_level", str(user.id))) < 2147483647:
            pt = int(conf.get("user_level", str(user.id))) + 1
            conf.set("user_level", str(user.id), str(pt))
            return True
    except:
        return False

def ret_check(conf, user, test_glyph):
    try:
        if test_glyph != "":
            return 99999
        else:
            return int(conf.get("user_level", str(user.id)))
    except:
        return 0

def check(conf, user):
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
    if pt == 2147483647:
        ptstr = "개발자"
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
    embed.add_field(name="호감도", value=ptstr, inline=True)
    embed.add_field(name="Discord 가입 일시", value=user.created_at.isoformat(), inline=True)
    embed.add_field(name="서버 가입 일시", value=user.joined_at.isoformat(), inline=True)
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

def serverinfo(guild):
    embed=discord.Embed(title=guild.name, color=0xffff00)
    embed.set_thumbnail(url=guild.icon_url)
    embed.add_field(name="서버 생성 일시", value=guild.created_at.isoformat(), inline=True)
    embed.add_field(name="주인", value=guild.owner.name, inline=True)
    embed.add_field(name="서버 지역", value=str(guild.region), inline=True)
    embed.add_field(name="서버 인원 수", value=str(len(guild.members)), inline=True)
    embed.add_field(name="역할 수", value=str(len(guild.roles)), inline=True)
    embed.add_field(name="채널 수", value=str(len(guild.channels)), inline=True)
    embed.add_field(name="커스텀 이모지 수", value=str(len(guild.emojis)), inline=True)
    if guild.mfa_level == 1:
        mfa = "예"
    else:
        mfa = "아니오"
    embed.add_field(name="서버 2차 인증", value=mfa, inline=True)
    return embed

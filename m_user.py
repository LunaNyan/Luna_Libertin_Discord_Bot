import discord

def increase(conf, user):
    try:
        if int(conf.get("user_level", str(user.id))) < 2147483647:
            pt = int(conf.get("user_level", str(user.id))) + 1
            conf.set("user_level", str(user.id), str(pt))
            return True
    except:
        return False

def ret_check(conf, user):
    try:
        return int(conf.get("user_level", str(user.id)))
    except:
        return 0

def check(conf, user):
    firstrun = False
    try:
        pt = int(conf.get("user_level", str(user.id)))
    except:
        pt = 1
        conf.set("user_level", str(user.id), "1")
        firstrun = True
    if firstrun:
        embed = discord.Embed(title="봇을 처음 사용하시네요!", description='"루냥아 도와줘"를 입력하면 도움말을 볼 수 있어요!', color=0xff0080)
    else:
        if user.display_name == user.name:
            usrname = user.name
        else:
            usrname = user.display_name + "(" + user.name + ")"
        embed = discord.Embed(title=usrname + " 님의 프로필", color=0xff0080)
    embed.set_thumbnail(url=user.avatar_url)
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
    if user.server_permissions.administrator:
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

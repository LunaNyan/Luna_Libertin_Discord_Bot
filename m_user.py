import discord

def increase(conf, user):
    try:
        if int(conf.get("user_level", str(user.id))) < 2147483647:
            pt = int(conf.get("user_level", str(user.id))) + 1
            conf.set("user_level", str(user.id), str(pt))
            return True
    except:
        return False

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
        ptstr = "노예"
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
    embed.add_field(name="유저 ID", value=str(user.id), inline=True)
    embed.add_field(name="가입 일시", value=user.created_at.isoformat(), inline=True)
    embed.add_field(name="서버 가입 일시", value=user.joined_at.isoformat(), inline=True)
    if user.server_permissions.administrator:
        usrperm = "서버 관리자"
    else:
        usrperm = "일반"
    embed.add_field(name="서버 권한", value=usrperm, inline=True)
    return embed

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
    embed.add_field(name="호감도", value=str(pt), inline=True)
    if str(user.id) == "280306700324700160":
        embed.add_field(name="분류", value="개발자", inline=True)
    else:
        embed.add_field(name="분류", value="유저", inline=True)
    embed.add_field(name="유저 ID", value=str(user.id), inline=True)
    embed.add_field(name="가입 일시", value=user.created_at.isoformat(), inline=True)
    embed.add_field(name="서버 가입 일시", value=user.joined_at.isoformat(), inline=True)
    if user.server_permissions.administrator:
        usrperm = "서버 관리자"
    else:
        usrperm = "유저"
    embed.add_field(name="서버 권한", value=usrperm, inline=True)
    return embed

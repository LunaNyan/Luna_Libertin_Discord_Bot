import discord, m_lang
from random import randint, choice

def rps_arg(text):
    if text == " 가위":
        return 1
    elif text == " 바위":
        return 2
    elif text == " 보":
        return 3
    else:
        return False

def rps_judge(player, cpu):
    if player == 1 and cpu == 3:
        return "승리!"
    elif player == 3 and cpu == 2:
        return "승리!"
    elif player == 2 and cpu == 1:
        return "승리!"
    elif player == cpu:
        return "무승부!"
    else:
        return "패배!"

def rps(message, user, db):
    if user.display_name == user.name:
        usrname = user.name
    else:
        usrname = user.display_name + "(" + user.name + ")"
    m = message.replace("루냥아 가위바위보", "")
    m = m.replace("_", "")
    p = rps_arg(m)
    if p != False:
        while True:
            c = randint(1, 3)
            if c == 1:
                cm = "가위"
            elif c == 2:
                cm = "바위"
            elif c == 3:
                cm = "보"
            r = rps_judge(p, c)
            if r == "패배!" and randint(1, 10) >= 3:
                continue
            else:
                break
        embed=discord.Embed(title="가위바위보 결과!", color=0xffff00)
        embed.add_field(name=usrname + "의 선택", value=m, inline=True)
        embed.add_field(name="루냥이의 선택", value=cm, inline=True)
        embed.add_field(name="결과", value=r, inline=False)
    else:
        embed=discord.Embed(title=m_lang.string(db, user.id, "rps_help"), description="예시 : 루냥아 가위바위보 " + choice(["가위", "바위", "보"]))
    return embed

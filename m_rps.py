import discord
from random import randint

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

def rps(message):
    m = message.replace("루냥아 가위바위보", "")
    p = rps_arg(m)
    if p != False:
        c = randint(1, 3)
        if c == 1:
            cm = "가위"
        elif c == 2:
            cm = "바위"
        elif c == 3:
            cm = "보"
        r = rps_judge(p, c)
        embed=discord.Embed(title="가위바위보 결과!", color=0xffff00)
        embed.add_field(name="사용자의 선택", value=m, inline=True)
        embed.add_field(name="CPU의 선택", value=cm, inline=True)
        embed.add_field(name="결과", value=r, inline=False)
    else:
        embed=discord.Embed(title="선택지로 가위, 바위, 보 중 하나를 골라주세요!")
    return embed

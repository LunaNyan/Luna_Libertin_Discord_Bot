#!/usr/bin/python3

from random import randint, shuffle
import discord

winning_percentage = 7
# 승률 조정 (기본값 : 7)
# 0부터 25까지 있으며, 낮을 수록 승률이 높습니다.
# 예를 들어, 승률을 0으로 맞출 경우 CPU가 플레이어보다 낮은 패를 선택할 수 없게 되기에, 플레이어는 무조건 이기게 됩니다.
# 승률을 25로 맞출 경우, CPU는 모든 종류의 패를 선택할 수 있게 됩니다.

result_str = ""
deck = []

power_player = 0
power_cpu = 0

result_str_player = ""
result_str_cpu = ""

xa = 0
xb = 0

xaa = 0
xbb = 0

ya = 0
yb = 0

yaa = 0
ybb = 0

def seotda_calc(a, b):
    global result_str
    if a == b: #땡
        if a == 10:
            result_str = "장땡"
        elif a == 9:
            result_str = "구땡"
        elif a == 8:
            result_str = "팔땡"
        elif a == 7:
            result_str = "칠땡"
        elif a == 6:
            result_str = "육땡"
        elif a == 5:
            result_str = "오땡"
        elif a == 4:
            result_str = "사땡"
        elif a == 3:
            result_str = "삼땡"
        elif a == 2:
            result_str = "이땡"
        elif a == 1:
            result_str = "삥땡"
        sd_power = 15 + a
    elif (a == 1 and b == 2) or (a == 2 and b == 1): #중간
        result_str = "알리"
        sd_power = 15
    elif (a == 1 and b == 4) or (a == 4 and b == 1):
        result_str = "독사"
        sd_power = 14
    elif (a == 1 and b == 9) or (a == 9 and b == 1):
        result_str = "구삥"
        sd_power = 13
    elif (a == 1 and b == 10) or (a == 10 and b == 1):
        result_str = "장삥"
        sd_power = 12
    elif (a == 4 and b == 10) or (a == 10 and b == 4):
        result_str = "장사"
        sd_power = 11
    elif (a == 4 and b == 6) or (a == 6 and b == 4):
        result_str = "세륙"
        sd_power = 10
    else: #끗
        xcuta = str(a + b)[-1]
        xcut = int(xcuta)
        if xcut == 9:
            result_str = "갑오(아홉끗)"
        elif xcut == 8:
            result_str = "여덟끗"
        elif xcut == 7:
            result_str = "일곱끗"
        elif xcut == 6:
            result_str = "여섯끗"
        elif xcut == 5:
            result_str = "다섯끗"
        elif xcut == 4:
            result_str = "네끗"
        elif xcut == 3:
            result_str = "세끗"
        elif xcut == 2:
            result_str = "두끗"
        elif xcut == 1:
            result_str = "한끗"
        elif xcut == 0:
            result_str = "망통(영끗)"
        sd_power = xcut
    return sd_power

def seotda_player(aa, bb):
    global xa
    global xb
    global xaa
    global xbb
    global deck
    xa = aa
    xb = bb
    xaa = deck[aa]
    xbb = deck[bb]
    return seotda_calc(xaa, xbb)

def seotda_cpu():
    global deck
    global ya
    global yb
    global yaa
    global ybb
    while 1 == 1:
        ya = randint(0, 9)
        yb = randint(0, 9)
        if ya == yb or ya == xa or ya == xb or yb == xa or yb == xb:
            continue
        else:
            yaa = deck[ya]
            ybb = deck[yb]
            break
    return seotda_calc(yaa, ybb)

def seotda_ready():
    global deck
    for ix in range(2):
        for iy in range(10):
            deck.append(iy+1)
    shuffle(deck)
    deck = deck[:10]

def seotda(message_content, user):
    global result_str_player
    global result_str_cpu
    global winning_percentage
    if user.display_name == user.name:
        usrname = user.name
    else:
        usrname = user.display_name + "(" + user.name + ")"
    try:
        message_content = message_content.replace("_", "")
        message_content = message_content.replace("루냥아 섯다 ", "")
        x, y = message_content.split(" ")
        x = int(x)
        y = int(y)
        if x == y:
            embed = discord.Embed(title="같은 카드를 두 번 고를 수 없습니다")
        elif x < 0 or y < 0 or x > 9 or y > 9:
            embed = discord.Embed(title="0에서 9까지의 숫자 두개를 골라주세요", description="예시 : 루냥아 섯다 " + str(randint(0, 9)) + " " + str(randint(0, 9)))
        else:
            while 1 == 1:
                seotda_ready()
                power_player = seotda_player(x, y)
                result_str_player = result_str
                power_cpu = seotda_cpu()
                result_str_cpu = result_str
                if power_cpu - power_player >= winning_percentage:
                    continue
                elif power_player == power_cpu:
                    result = "비겼습니다!"
                    break
                elif power_player > power_cpu:
                    if power_player - power_cpu == 1:
                        result = "한 끗 차이로 승리!"
                    else:
                        result = "승리!"
                    break
                elif power_player < power_cpu:
                    if power_cpu - power_player == 1:
                        result = "한 끗 차이로 패배!"
                    else:
                        result = "패배!"
                    break
            embed = discord.Embed(title="섯다 진행 결과", color=0xffff00)
            embed.add_field(name=usrname + "의 선택", value=str(xa) + ", " + str(xb) + "(" + str(xaa) + "월, " + str(xbb) + "월), " + result_str_player, inline=True)
            embed.add_field(name="루냥이의 선택", value=str(ya) + ", " + str(yb) + "(" + str(yaa) + "월, " + str(ybb) + "월), " + result_str_cpu, inline=True)
            embed.add_field(name="결과", value=result, inline=True)
            d0 = ""
            d2 = 0
            for d1 in deck:
                d0 = d0 + str(d2) + "번 패 : " + str(d1) + "월\n"
                d2 = d2 + 1
            embed.add_field(name="패 목록", value=d0, inline=False)
    except ValueError:
        embed = discord.Embed(title="잘못된 카드 번호입니다")
    return embed

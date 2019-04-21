#!/usr/bin/python3

from random import randint
from random import shuffle

result_str = ""
deck = []

power_player = 0
power_cpu = 0

result_str_player = ""
result_str_cpu = ""

xa = 0
xb = 0

ya = 0
yb = 0

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
            result_str = "갑오"
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
            result_str = "망통"
        sd_power = xcut
    return sd_power

def seotda_player(aa, bb):
    global xa
    global xb
    global deck
    xa = deck[aa]
    xb = deck[bb]
    return seotda_calc(xa, xb)

def seotda_cpu():
    global deck
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

def seotda_init(message_content):
    global result_str_player
    global result_str_cpu
    try:
        message_content = message_content.replace("_", "")
        message_content = message_content.replace("루냥아 섯다 ", "")
        x, y = message_content.split(" ")
        x = int(x)
        y = int(y)
        if x == y:
            return "같은 카드를 두장 고를 수 없습니다"
        elif x < 0 or y < 0 or x > 9 or y > 9:
            return "0에서 9까지의 숫자를 골라주세요"
        else:
            seotda_ready()
            power_player = seotda_player(x, y)
            result_str_player = result_str
            power_cpu = seotda_cpu()
            result_str_cpu = result_str
            if power_player == power_cpu:
                return "비겼습니다!"
            elif power_player > power_cpu:
                return "승리!"
            elif power_player < power_cpu:
                return "패배!"
    except ValueError:
        return "숫자를 입력해주세요"

def ret_player():
    return result_str_player

def ret_cpu():
    return result_str_cpu

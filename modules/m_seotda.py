# 두장섯다 알고리즘 모듈

from random import randint, shuffle
import sys, discord, m_user

if __name__=="__main__":
    print("FATAL   : Run this bot from right way.")
    sys.exit(1)

winning_percentage = 28
# 승률 조정 (기본값 : 7, 범위 : 0 ~ 28)
# "낮을 수록" 승률이 높습니다.
# 예를 들어, 승률을 0으로 맞출 경우 CPU가 플레이어보다 낮은 패를 선택할 수 없게 되기에, 플레이어는 무조건 이기게 됩니다.
# 승률을 28로 맞출 경우, CPU는 모든 종류의 패를 선택할 수 있게 됩니다.

gd_percent = 70
# 광땡 출현 확률 조정 (기본값 : 70, 범위 : 0 ~ 100)
# "높을 수록" 광땡 출현 확률이 증가합니다.

sp_percent = 70
# 특수족보 출현 확률 조정 (기본값 : 70, 범위 : 0 ~ 100)
# "높을 수록" 특수족보 출현 확률이 증가합니다.

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

# 패 판정
def seotda_calc(a, b):
    global result_str
    if (a == 3 and b == 8) or (a == 8 and b == 3): #광땡
        if randint(1, 100) <= gd_percent:
            result_str = "3 - 8 광땡!"
            return 28
    elif (a == 1 and b == 8) or (a == 8 and b == 1):
        if randint(1, 100) <= gd_percent:
            result_str = "1 - 8 광땡!"
            return 27
    elif (a == 1 and b == 3) or (a == 3 and b == 1):
        if randint(1, 100) <= gd_percent:
            result_str = "1 - 3 광땡!"
            return 26
    elif (a == 9 and b == 4) or (a == 4 and b == 9): #특수족보
        if randint(1, 100) <= sp_percent:
            result_str = "멍구사(세끗)"
            return -1
        else:
            result_str = "구사(세끗)"
            return -2
    elif (a == 7 and b == 4) or (a == 4 and b == 7):
        if randint(1, 100) <= sp_percent:
            result_str = "7 - 4 암행어사(한끗)"
            return -3
    elif (a == 7 and b == 3) or (a == 3 and b == 7):
        if randint(1, 100) <= sp_percent:
            result_str = "7 - 3 땡잡이(망통)"
            return -4
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
    elif (a == 1 and b == 2) or (a == 2 and b == 1): #삥
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

# CPU 패 선택
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

# 무작위 패 생성
def seotda_ready():
    global deck
    for ix in range(2):
        for iy in range(10):
            deck.append(iy+1)
    shuffle(deck)
    deck = deck[:10]

def seotda(db, message, head):
    global result_str_player
    global result_str_cpu
    global winning_percentage
    message_content = message.content
    user = message.author
    if user.display_name == user.name:
        usrname = user.name
    else:
        usrname = user.display_name + "(" + user.name + ")"
    try:
        message_content = message_content.replace("_", "")
        message_content = message_content.replace(head + "섯다 ", "")
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
                if power_cpu - power_player >= winning_percentage: #승률 조정
                    if power_cpu >= 0 or power_player >= 0:
                        continue
                if power_player == -1 and power_cpu <= 24: #특수족보 처리
                    result = "비겼습니다!"
                    m_user.gamemoney(db, message, 10)
                    break
                elif power_player <= 24 and power_cpu == -1:
                    result = "비겼습니다!"
                    m_user.gamemoney(db, message, 10)
                    break
                elif power_player == -2 and power_cpu <= 15:
                    result = "비겼습니다!"
                    m_user.gamemoney(db, message, 10)
                    break
                elif power_player <= 15 and power_cpu == -2:
                    result = "비겼습니다!"
                    m_user.gamemoney(db, message, 10)
                    break
                elif power_player == -3 and power_cpu >= 26 and power_cpu <= 27:
                    result = "승리!"
                    m_user.gamemoney(db, message, 60)
                    break
                elif power_cpu == -3 and power_player >= 26 and power_player <=27:
                    result = "패배!"
                    break
                elif power_player == -4 and power_cpu >= 16 and power_cpu <= 24:
                    result = "승리!"
                    m_user.gamemoney(db, message, 60)
                    break
                elif power_cpu == -4 and power_player >= 16 and power_player <= 24:
                    result = "패배!"
                    break
                elif power_player == power_cpu: #일반족보 처리
                    result = "비겼습니다!"
                    break
                elif power_player > power_cpu:
                    if power_player - power_cpu == 1:
                        result = "한 끗 차이로 승리!"
                        m_user.gamemoney(db, message, 110)
                    else:
                        result = "승리!"
                        m_user.gamemoney(db, message, 60)
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

def lowhigh_strip(n):
    if n == 0:
        text = "A"
    elif n == 10:
        text = "J"
    elif n == 11:
        text = "Q"
    elif n == 12:
        text = "K"
    else:
        text = str(n + 1)
    return text

def lowhigh(db, message, head):
    # 1  : A
    # 10 : K
    # 11 : Q
    # 12 : J
    invalid_num = False
    m = message.content.replace(head + "로하이 ", "")
    try:
        power = int(m) - 1
        if power >= 13 or power < 0:
            invalid_num = True
        else:
            power = randint(0, 12)
    except:
        invalid_num = True
    if message.content == head + "로하이" or invalid_num:
        embed = discord.Embed(title="사용 방법", description="루냥아 로하이 (1 ~ 13)")
        return embed
    else:
        if m_user.gamemoney(db, message) < 10:
            embed=discord.Embed(title=m_lang.string(db, message.author.id, "not_enough_gamemoney"), desctiption=m_lang.string(db, message.author.id, "not_enough_gamemoney_desc"))
        else:
            m_user.gamemoney(db, message, -10)
            winrate = randint(0, 99)
            if winrate >= 50:
                cpu_power = power
            else:
                cpu_power = randint(0, 12)
            if cpu_power == power:
                result = "승리!"
                m_user.gamemoney(db, message, 40)
            else:
                result = "패배"
            embed = discord.Embed(title=result, description="플레이어가 고른 카드 : " + lowhigh_strip(power) + "\n루냥이가 고른 카드 : " + lowhigh_strip(cpu_power))
        return embed
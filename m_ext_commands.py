import random
from m_user import ret_check

comm_d = {'점프':'(쫑긋)폴짝! >_<',
          '굴러':'(쫑긋)데굴데굴~ >_<',
          '손':':raised_hand:'}

def sans():
    sans_str = ["언더테일 아시는구나! 혹시 모르시는분들에 대해 설명해드립니다 샌즈랑 언더테일의 세가지 엔딩루트중 몰살엔딩의 최종보스로 진.짜.겁.나.어.렵.습.니.다 공격은 전부다 회피하고 만피가 92인데 샌즈의 공격은 1초당 60이 다는데다가 독뎀까지 추가로 붙어있습니다.. 하지만 이러면 전대로 게임을 깰 수 가없으니 제작진이 치명적인 약점을 만들었죠. 샌즈의 치명적인 약점이 바로 지친다는것입니다. 패턴들을 다 견디고나면 지쳐서 자신의 턴을 유지한채로 잠에듭니다. 하지만 잠이들었을때 창을옮겨서 공격을 시도하고 샌즈는 1차공격은 피하지만 그 후에 바로날아오는 2차 공격을 맞고 죽습니다.",
                "와!",
                "와 샌즈!",
                "와 파피루스!",
                "와 샌즈! 와 파피루스!"]
    return random.choice(sans_str)

def imcute(conf, user, test_glyph):
    # int 500 or over
    imcute_str_1 = ["허ㅓㅓㅓㅓㅓㅓㅓㅓㅠㅠㅠㅠㅠㅠㅠㅠㅠ저 너무 끼여워여",
                  "저 너무 깜찍하고 귀여워여 ㅠㅠㅠㅠㅠㅠ",
                  "헉 ㅠ ㅜㅠㅜㅜㅜ 나 넘귀엽다 ㅠ ㅠㅠㅠ 넘귀여워 나 엄청귀엽다 :two_hearts::purple_heart::purple_heart::heart::heart:"]
    # int 100 or over
    imcute_str_2 = ["흐아아ㅠㅠㅠㅠ나 너무기엽구이뻐ㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠ흐앙하읗아ㅏㅇ훙흐아ㅠㅠㅠ사랑해ㅠㅠㅠ진짜 귀엽다ㅠㅠㅠㅠ이거완전...행복해..너무행복해..ㅠㅠㅠㅠㅠ사랑해ㅠㅠㅠ",
                   "저 ㄴ너무귀여워요오오오오오오ㅠ.ㅠ.ㅠ.ㅠ .아으 깨물어주고싶어요ㅠ.ㅠ",
                   "대박.... 나 귀엽다....진짜...최고야 !!!!!"]
    # else
    imcute_str_3 = ["우왕..! 나 귀여워..! 저 꼬리는 얼마나 폭신폭신할까..!",
                   "우응~ 어뜩해.. 하우우.."]
    if ret_check(conf, user, test_glyph) >= 500:
        s = random.choice(imcute_str_1)
    elif ret_check(conf, user, test_glyph) >= 200:
        s = random.choice(imcute_str_2)
    else:
        s = random.choice(imcute_str_3)
    return s

def pat(conf, user, test_glyph):
    # int 500 or over
    pat_str_1 =  ["언니잉!(와락",
                 "하앙~ (꼬리펑",
                 ">_<~:two_hearts:"]
    # int 200 or over
    pat_str_2 = ["(부비부비",
                ">_<~ (부비부비",
                "하앙~ (와락"]
    # else
    pat_str_3 = ["아앗.. //ㅅ//",
                "후앗.. ///",
                "앗.. :blush:"]
    if ret_check(conf, user, test_glyph) >= 500:
        s = random.choice(pat_str_1)
    elif ret_check(conf, user, test_glyph) >= 200:
        s = random.choice(pat_str_2)
    else:
        s = random.choice(pat_str_3)
    return s

def l_lv(conf, user, test_glyph):
    # int 500 or over
    lv_str_1 = ["저두우~:two_hearts:", "헤헤~(방긋"]
    # int 200 or over
    lv_str_2 = [">_<~", "헤헤~:two_hearts"]
    # else
    lv_str_3 = ["헤헤~", "후히히~"]
    if ret_check(conf, user, test_glyph) >= 500:
        s = random.choice(lv_str_1)
    elif ret_check(conf, user, test_glyph) >= 200:
        s = random.choice(lv_str_2)
    else:
        s = random.choice(lv_str_3)
    return s

def l_ping():
    lp_str = ["우웅? (쫑긋",
              "(꼬리살랑",
              "후아암~(발라당",
              "네에~?(쫑긋",
              "부르셨어요? 헤헤..(꼬리살랑"]
    return random.choice(lp_str)

def selectr(message):
    m = message
    m = m.replace("_", "")
    m = m.replace("루냥아 골라줘 ", "")
    i = m.split(" ")
    return random.choice(i)

def l_dog():
    dog_str = ["월", "멍", "왈", "애옹"]
    return random.choice(dog_str)

def l_dice():
    dice_int = random.randint(1, 6)
    return str(dice_int)

def l_ticket(message):
    a = message
    a = a.replace("루냥아 제비뽑기 ", "")
    try:
        b = a.split(',')
        a0 = b[0].split()
        b0 = b[1].split()
        if len(a0) != len(b0):
            return "선택지와 결과의 개수가 맞지 않습니다 (각 항목은 띄어쓰기로 구분합니다)"
        else:
            random.shuffle(b0)
            c = 0
            ret = "```제비뽑기 결과!\n"
            for i in a0:
               ret+= str(i) + ' : ' + str(b0[c]) + "\n"
               c = c + 1
            ret+= "```"
            return ret
    except:
        return "선택지와 결과를 구분할 때는 쉼표(,)를 입력해주세요"

def say_lv():
    say_lv_str = ["(꼬옥", "(껴안", "(쓰다듬"]
    return random.choice(say_lv_str)

def say_shuffle(message):
    q = message.content.replace("루냥아 섞어줘 ", "")
    w = q.split(" ")
    random.shuffle(w)
    r = ""
    for m in w:
        r += m + ", "
    return r[:-2]

def say_rint(message):
    return str(random.randint(1, 100))

def eat(message):
    e = message.content.replace('루냥아 ', '').replace(' 먹어', '')
    if e in ["엿", "똥", "뻐큐", "빠큐", "훠뀨", "퍼큐", "퍽유"]:
        embed = discord.Embed(title="그런 물체는 먹을 수 없어요!", color=0xff0000)
    else:
        embed = discord.Embed(title=e + "을(를) 먹었어요!", description="옴뇸뇸뇸뇸", color=0xff77ff)
    return embed

def ext_talk(message):
    m = message.content.replace("루냥아 ", "")
    if m in comm_d:
        return comm_d[m]
    else:
        return None
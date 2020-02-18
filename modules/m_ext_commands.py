import discord, random, m_etc, m_pingpong, m_lang, nekos
from m_user import ret_check

comm_d = {'점프':'(쫑긋)폴짝! >_<',
          '굴러':'(쫑긋)데굴데굴~ >_<',
          '손':':raised_hand:'}

possible = [
    'feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo',
    'solog', 'feetg', 'cum', 'erokemo', 'les', 'wallpaper', 'lewdk',
    'ngif', 'tickle', 'lewd', 'gecg', 'eroyuri', 'eron',
    'cum_jpg', 'bj', 'nsfw_neko_gif', 'solo', 'nsfw_avatar',
    'poke', 'anal', 'slap', 'hentai', 'erofeet',
    'keta', 'blowjob', 'pussy', 'tits', 'holoero', 'pussy_jpg',
    'pwankg', 'classic', 'kuni', 'femdom',
    'spank', 'cuddle', 'erok', 'boobs', 'random_hentai_gif',
    'smallboobs', 'ero', 'baka'
]

possible_pub = [
               'feed', 'kemonomimi', 'gasm', 'avatar', 'holo', 'lizard',
               'waifu', 'pat', '8ball', 'kiss', 'neko', 'fox_girl',
               'hug', 'smug', 'goose'
]

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
    embed=discord.Embed(title=s, color=0xff77ff)
    embed.set_image(url=nekos.img("pat"))
    embed.set_footer(text="powered by nekos.life")
    return embed

def hug():
    embed=discord.Embed(title="꼬옥~", color=0xff77ff)
    embed.set_image(url=nekos.img("hug"))
    embed.set_footer(text="powered by nekos.life")
    return embed

def cuddle():
    embed=discord.Embed(title="부비부비~", color=0xff77ff)
    embed.set_image(url=nekos.img("cuddle"))
    embed.set_footer(text="powered by nekos.life")
    return embed

def kiss():
    embed=discord.Embed(title="쪽~ >_<", color=0xff77ff)
    embed.set_image(url=nekos.img("kiss"))
    embed.set_footer(text="powered by nekos.life")
    return embed

def l_lv(conf, user, test_glyph):
    # int 500 or over
    lv_str_1 = ["저두우~:two_hearts:", "헤헤~(방긋"]
    # int 200 or over
    lv_str_2 = [">_<~", "헤헤~:two_hearts:"]
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

def selectr(message, head):
    m = message
    m = m.replace(head + "골라줘 ", "")
    i = m.split(" ")
    return random.choice(i)

def l_dog():
    dog_str = ["월", "멍", "왈", "애옹"]
    return random.choice(dog_str)

def l_dice():
    dice_int = random.randint(1, 6)
    return str(dice_int)

def l_ticket(message, head, db):
    a = message.content
    a = a.replace(head + "제비뽑기 ", "")
    try:
        b = a.split(',')
        a0 = b[0].split()
        b0 = b[1].split()
        if len(a0) != len(b0):
            return m_lang.string(db, message.author.id, "ticket_no_balance")
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
        return m_lang.string(db, message.author.id, "ticket_wrong_indent")

def say_lv():
    say_lv_str = ["(꼬옥", "(껴안", "(쓰다듬"]
    return random.choice(say_lv_str)

def say_shuffle(message, head):
    q = message.content.replace(head + "섞어줘 ", "")
    w = q.split(" ")
    random.shuffle(w)
    r = ""
    for m in w:
        r += m + ", "
    return r[:-2]

def say_rint(message):
    return str(random.randint(1, 100))

def eat(message, head, db):
    if message.content == head + "먹어":
        embed=discord.Embed(title="사용 방법 : 루냥아 (물체) 먹어", color=0xff77ff)
    else:
        e = message.content.replace(head, '')
        e = e.replace(' 먹어', '')
        if e in ["엿", "똥", "뻐큐", "빠큐", "훠뀨", "퍼큐", "퍽유"]:
            embed = discord.Embed(title=m_lang.string(db, message.author.id, "swearing_in_eat"), color=0xff0000)
        else:
            embed = discord.Embed(title=e + m_etc.checkTrait(e) + m_lang.string(db, message.author.id, "eat"), description="옴뇸뇸뇸뇸", color=0xff77ff)
    return embed

def bite(message, head, db):
    if message.content == head + "물어":
        embed=discord.Embed(title="사용 방법 : 루냥아 (물체) 물어", color=0xff77ff)
    else:
        e = message.content.replace(head, '')
        e = e.replace(' 물어', '')
        if e in ["엿", "똥", "뻐큐", "빠큐", "훠뀨", "퍼큐", "퍽유"]:
            embed = discord.Embed(title=m_lang.string(db, message.author.id, "swearing_in_bite"), color=0xff0000)
        else:
            embed = discord.Embed(title=e + m_etc.checkTrait(e) + m_lang.string(db, message.author.id, "bite"), description="앙~", color=0xff77ff)
    return embed

def ext_talk(client, message, head):
    m = message.content.replace(head, "")
    r = m_pingpong.react(m)
    if m in comm_d:
        embed=discord.Embed(title=comm_d[m], color=0xff7fff)
        return embed
    elif r != None:
        if not r:
            return False
        else:
            rr = random.choice(r)
            rr = rr.decode("utf-8")
            embed=discord.Embed(title=rr, color=0xff7fff)
            embed.set_footer(text="powered by PINGPONG Builder")
            return embed
    else:
        return None

def server_burning(db, id):
    try:
        b = db.get("server_burning", str(id))
    except:
        b = "저하고도 놀아줘요!"
    return b

def nsfw_neko(message, head):
    if message.content == head + "야짤":
        li = ""
        for le in possible:
            li += le + ", "
        li = li[:-2]
        embed=discord.Embed(title="사용 가능한 야짤 태그", description=li)
        embed.add_field(name="주의사항", value="야짤 기능을 사용함으로써 발생하는 모든 피해는 전적으로 명령어 사용자에게 있음을 숙지해 주시기 바랍니다\n야짤 기능을 사용한다고 해서 호감도가 깎이지는 않습니다")
    else:
        s = message.content.replace(head + "야짤 ", "")
        if s not in possible:
            embed=discord.Embed(title="사용할 수 없는 야짤 태그입니다", description='도움말 : "루냥아 야짤"')
        else:
            embed=discord.Embed(title="야짤 태그 : " + s, color=0xff77ff)
            embed.set_image(url=nekos.img(s))
            embed.set_footer(text="powered by nekos.life")
    return embed

def neko(message, head):
    if message.content == head + "짤":
        li = ""
        for le in possible_pub:
            li += le + ", "
        li = li[:-2]
        embed=discord.Embed(title="사용 가능한 짤 태그", description=li)
    else:
        s = message.content.replace(head + "짤 ", "")
        if s not in possible_pub:
            embed=discord.Embed(title="사용할 수 없는 짤 태그입니다", description='도움말 : "루냥아 야짤"')
        else:
            embed=discord.Embed(title="짤 태그 : " + s, color=0xff77ff)
            embed.set_image(url=nekos.img(s))
            embed.set_footer(text="powered by nekos.life")
    return embed

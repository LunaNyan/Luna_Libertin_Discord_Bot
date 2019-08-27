import discord, cpuinfo, psutil, os, math, m_food

patch_ver = ""

def help(user, client, text, bot_ver):
    a = text
    a = a.replace('_', '')
    a = a.replace('루냥아 도와줘', '')
    if a == '':
        embed=discord.Embed(title="기계식 루냥이를 초대해주셔서 감사합니다!", description="[민원창구](https://discordapp.com/invite/yyS9x5V), [봇 초대하기](https://discordapp.com/oauth2/authorize?client_id=598080777565241354&scope=bot&permissions=388190)", color=0xff0080)
        embed.set_author(name="기계식 루냥이 사용 방법",icon_url=client.user.avatar_url)
        embed.add_field(name="도움말", value="루냥아 도와줘 (항목), 루냥아 업데이트내역, 루냥아 누구니, 루냥아 소스코드", inline=False)
        embed.add_field(name="커뮤니티", value="루냥아 공지사항 목록, 루냥아 공지사항 (숫자), 루냥아 방명록, 루냥아 방명록 쓰기 (할 말)", inline=False)
        embed.add_field(name="프로필", value="루냥아 나 어때, 루냥아 (멘션) 어때, 루냥아 소개말 (자기소개)", inline=False)
        embed.add_field(name="정보", value="루냥아 서버정보, 루냥아 인기도, 루냥아 자가진단, 루냥아 서버목록, 루냥아 생일, 루냥아 버전, 루냥아 후원", inline=False)
        embed.add_field(name="일상", value="루냥아 출석체크, 루냥아 배고파, 루냥이 귀여워, 루냥이 쓰담쓰담, 루냥아 짖어봐, 루냥아 손, 루냥아 (물체) 먹어, 와! 샌즈!", inline=False)
        embed.add_field(name="게임", value="루냥아 섯다, 루냥아 주사위, 루냥아 제비뽑기, 루냥아 가위바위보", inline=False)
        embed.add_field(name="유용한 기능", value="루냥아 계산해줘 (계산식), 루냥아 계산해줘 이미지 (계산식), 루냥아 확성기, 루냥아 골라줘", inline=False)
        embed.add_field(name="패시브", value="관심 가져주기", inline=False)
        if user.guild_permissions.administrator:
            embed.add_field(name="관리자 기능", value="루냥아 공지채널 추가, 루냥아 공지채널 삭제, 루냥아 로그채널 생성, 루냥아 채널연결 생성, 루냥아 채널연결 접속 (코드), 루냥아 채널연결 삭제", inline=False)
        embed.set_footer(text="Copyright (C) 2017 - 2019 libertin | v" + bot_ver)
    elif a == ' 도움말':
        embed=discord.Embed(title="도움말", description="도움말 항목", color=0x8080ff)
        embed.add_field(name="루냥아 도와줘 (항목)", value="각 항목에 대한 도움말을 표시합니다\n항목을 지정하지 않았다면 전체 명령어 목록이 표시됩니다", inline=False)
        embed.add_field(name="루냥아 업데이트내역", value="업데이트 내역을 표시합니다", inline=False)
        embed.add_field(name="루냥아 누구니", value="자기소개와 제작자 목록을 표시합니다", inline=False)
        embed.add_field(name="루냥아 소스코드", value="기계식 루냥이의 GitHub 레포지토리를 표시합니다", inline=False)
    elif a == ' 커뮤니티':
        embed=discord.Embed(title="도움말", description="커뮤니티 항목", color=0x8080ff)
        embed.add_field(name="루냥아 공지사항 목록", value="공지사항 목록을 불러옵니다", inline=False)
        embed.add_field(name="루냥아 공지사항 (번호)", value="목록에 해당하는 번호의 공지사항을 읽습니다\n번호가 없으면 첫번째 공지사항을 읽습니다", inline=False)
        embed.add_field(name="루냥아 방명록", value="방명록을 표시합니다", inline=False)
        embed.add_field(name="루냥아 방명록 쓰기 (할 말)", value="방명록에 글을 씁니다", inline=False)
    elif a == ' 프로필':
        embed=discord.Embed(title="도움말", description="프로필 항목", color=0x8080ff)
        embed.add_field(name="루냥아 나 어때", value="사용자 정보를 불러옵니다", inline=False)
        embed.add_field(name="루냥아 (멘션) 어때", value="다른 사용자의 정보를 불러옵니다", inline=False)
        embed.add_field(name="루냥아 소개말 (자기소개)", value="사용자 정보에 표시되는 소개말을 설정합니다", inline=False)
    elif a == ' 정보':
        embed=discord.Embed(title="도움말", description="정보 항목", color=0x8080ff)
        embed.add_field(name="루냥아 서버정보", value="서버 정보를 불러옵니다", inline=False)
        embed.add_field(name="루냥아 인기도", value="몇개의 서버에서 몇명의 유저들이 저를 보고 있는지 알려줘요!", inline=False)
        embed.add_field(name="루냥아 자가진단", value="봇이 정상 동작할 수 있는지 점검합니다", inline=False)
        embed.add_field(name="루냥아 서버목록", value="서버 목록을 불러옵니다", inline=False)
        embed.add_field(name="루냥아 생일", value="봇이 언제 탄생했는지 알려줍니다", inline=False)
        embed.add_field(name="루냥아 버전", value="봇의 버전, 서버 상태, 제작진을 보여줍니다", inline=False)
        embed.add_field(name="루냥아 후원", value="후원 계좌와 리워드를 표시합니다", inline=False)
    elif a == ' 일상':
        embed=discord.Embed(title="도움말", description="일상 항목", color=0x8080ff)
        embed.add_field(name="루냥아 출석체크", value="출석을 체크합니다", inline=False)
        embed.add_field(name="루냥아 배고파", value="랜덤으로 음식을 추천해줍니다 (음식을 사주지는 않습니다!)", inline=False)
        embed.add_field(name="루냥이 귀여워", value="자기 자신을 귀여워합니다 (루냥이 커여워, 귀냥이 루여워, 커냥이 루여워 도 가능합니다)", inline=False)
        embed.add_field(name="루냥이 쓰담쓰담", value="자기 자신한테 사이버(?) 쓰다듬을 선물해줍니다", inline=False)
        embed.add_field(name="루냥아 짖어봐", value="멍", inline=False)
        embed.add_field(name="루냥아 손", value=":raised_hand:", inline=False)
        embed.add_field(name="루냥아 (물체) 먹어", value="물체를 먹습니다(?)", inline=False)
        embed.add_field(name="와! 샌즈!", value="언더테일 아시는구나!", inline=False)
    elif a == ' 게임':
        embed=discord.Embed(title="도움말", description="게임", color=0xffff00)
        embed.set_author(name="게임 사용 방법 보기 : 루냥아 도와줘 게임 (게임이름)")
        embed.add_field(name="섯다", value="CPU와 두장섯다를 진행합니다", inline=False)
        embed.add_field(name="제비뽑기", value="CPU가 제비뽑기를 실행합니다", inline=False)
        embed.add_field(name="주사위", value="1부터 6까지 무작위의 숫자를 출력합니다", inline=False)
        embed.add_field(name="가위바위보", value="CPU와 가위바위보를 진행합니다", inline=False)
    elif a == ' 게임 섯다':
        embed=discord.Embed(title="두장섯다 사용 방법", description="명령어 : 루냥아 섯다 (숫자1) (숫자2), 0~9까지의 숫자 두개를 입력해 진행합니다", color=0xffff00)
        embed.add_field(name="족보 순위", value="땡 > 삥 > 끗", inline=False)
        embed.add_field(name="땡", value="두 패가 같은 경우 (장땡 ~ 삥땡)", inline=False)
        embed.add_field(name="삥", value="알리(1+2), 독사(1+4), 구삥(1+9), 장삥(1+10), 장사(4+10), 세륙(4+6)", inline=False)
        embed.add_field(name="끗", value="두 패 합의 일의 자리 숫자 (갑오 ~ 망통)", inline=False)
    elif a == ' 게임 제비뽑기':
        embed=discord.Embed(title="제비뽑기 사용 방법", description="명령어 : 루냥아 제비뽑기 (선택지1) (선택지2) ... , (결과1) (결과2) ...", color=0xffff00)
        embed.add_field(name="사용 방법", value="각 항목은 띄어쓰기로 구분, 선택지와 결과는 쉼표(,)로 구분!", inline=False)
        embed.add_field(name="주의사항", value="선택지와 결과의 개수는 동일해야 합니다", inline=True)
    elif a == ' 게임 주사위':
        embed=discord.Embed(title="주사위 사용 방법", description="명령어 : 루냥아 주사위", color=0xffff00)
    elif a == ' 게임 가위바위보':
        embed=discord.Embed(title="가위바위보 사용 방법", description="명령어 : 루냥아 가위바위보 (선택지)", color=0xffff00)
        embed.add_field(name="선택지", value="가위, 바위, 보", inline=False)
    elif a == ' 유용한 기능':
        embed=discord.Embed(title="도움말", description="유용한 기능", color=0x00ff00)
        embed.add_field(name="루냥아 계산해줘 (계산식)", value="Wolfram|Alpha 계산 쿼리를 제공합니다", inline=False)
        embed.add_field(name="루냥아 계산해줘 이미지 (계산식)", value="Wolfram|Alpha 플롯 계산 쿼리를 제공합니다(실험적인 기능입니다!)", inline=False)
        embed.add_field(name="루냥아 골라줘 (선택지1) (선택지2) ...", value="어느것을 고를까요 알아맞춰 봅시다", inline=False)
        embed.add_field(name="루냥아 확성기 (할 말)", value="루냥이가 대신 말해줍니다 (혐오 단어가 감지되는 경우 거부됩니다)", inline=False)
        embed.add_field(name="루냥아 서버목록", value="이 봇이 활동중인 서버들의 목록을 불러옵니다", inline=False)
    elif a == ' 패시브':
        embed=discord.Embed(title="도움말", description="패시브", color=0x0000ff)
        embed.add_field(name="관심 가져주기", value='채팅을 많이 치고 있을 때 일정 확률로 관심을 가져줍니다\n호감도가 친구 이상일 때 동작합니다\n"루냥아 관심 가져주기"로 토글이 가능합니다', inline=False)
    elif a == ' 관리자 기능':
        if user.guild_permissions.administrator:
            embed=discord.Embed(title="도움말", description="관리자 기능", color=0xff0000)
            embed.add_field(name="루냥아 공지채널 추가", value="현재 채널을 알림 채널로 추가합니다", inline=False)
            embed.add_field(name="루냥아 공지채널 삭제", value="현재 채널을 알림 채널에서 삭제합니다", inline=False)
            embed.add_field(name="루냥아 로그채널 생성", value="메시지 수정, 삭제, 확성기 사용을 기록해주는 채널을 생성합니다", inline=False)
            embed.add_field(name="루냥아 채널연결 생성", value="채널 간 1:1 텍스트 채팅 연결을 준비합니다", inline=False)
            embed.add_field(name="루냥아 채널연결 접속 (코드)", value="부여받은 접속 코드로 채널을 연결합니다", inline=False)
            embed.add_field(name="루냥아 채널연결 삭제", value="채널 연결을 삭제합니다", inline=False)
        else:
            embed=discord.Embed(title="서버 관리자만 해당 기능을 사용할 수 있습니다", color=0xff0000)
    else:
        embed=discord.Embed(title='전체 도움말을 원하신다면 그냥 "루냥아 도와줘"라고만 입력해주세요!')
    return embed

def servers_list(client, page):
    embed=discord.Embed(title="전체 서버 목록", color=0xff00ff)
    n = 0
    servers = {}
    sorted_servers = {}
    lk = []
    lu = []
    lo = []
    for s in client.guilds:
        servers[str(s)] = [str(len(s.members)), s.owner.name]
        n += 1
    sorted_servers = sorted(servers)
    for k in sorted_servers:
        lk.append(k)
        lu.append(servers[k][0])
        lo.append(servers[k][1])
    pages = math.ceil(len(lk) / 10)
    if page > pages or page <= 0:
        embed=discord.Embed(title="잘못된 페이지 번호입니다")
    else:
        c = (page - 1) * 10
        ct = c + 9
        while c <= ct:
            try:
                embed.add_field(name="#" + str(c+1) + " : " + lk[c], value="유저 수 : " + lu[c] + ", 서버 주인 : " + lo[c], inline=True)
                c += 1
            except:
                break
        embed.set_footer(text=str(page) + ' / ' + str(pages) + ' 페이지, 다른 페이지 보기 : "루냥아 서버목록 (페이지)"')
    return embed

def test_features(bot_ver):
    embed=discord.Embed(title="기계식 루냥이 테스트존에 오신 것을 환영합니다!", description="테스트 기능 목록", color=0xff00ff)
    embed.add_field(name="루냥아 소개말 (자기소개)", value='"루냥아 나 어때", "루냥아 (멘션) 어때"에 표시될 자기소개를 입력합니다', inline=False)
    embed.add_field(name="루냥아 (멘션) 어때", value="다른 사람의 프로필을 볼 수 있습니다", inline=False)
    embed.add_field(name="루냥아 캡챠 (문장)", value="CAPTCHA 스타일의 이미지로 문장을 써줍니다", inline=False)
    embed.add_field(name="루냥아 후원", value="후원 계좌와 리워드를 표시합니다", inline=False)
    embed.add_field(name="기타 변경 사항", value="- 게임 시 상대방과 CPU의 이름 변경\n- 가위바위보 승률 상향\n- 호감도 분포 변경", inline=False)
    embed.set_footer(text="ver " + bot_ver)
    return embed

def donation():
    embed=discord.Embed(title="기계식 루냥이를 지원해주세요!", color=0xffccff)
    embed.add_field(name="후원 계좌", value="하나은행 538-910289-86107", inline=False)
    embed.add_field(name="후원 리워드", value="- 후원자 칭호\n- (10,000원 이상 후원 시) Nitro Classic 1개월, 컬쳐랜드 문화상품권 5,000원권 중 택1\n\n후원 리워드를 받으려면 [공식 트위터](https://twitter.com/luna_libertin) 또는 libertin#2340에 DM을 남겨주세요!)", inline=False)
    return embed

def ret_changelog(client, bot_ver):
    if patch_ver != "":
        patch_guide = "안정성 패치는 업데이트 내역에 나오지 않아요!"
    else:
        patch_guide = ""
    embed=discord.Embed(title="업데이트 내역", description="현재 버전은 " + bot_ver + "이예요!\n" + patch_guide, color=0xffffff)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.add_field(name="Error : failed to load list for update log", value="Value : NOT_FOUND", inline=False)
    return embed

def get_info(client, uptime, uid, hash_str, memkb, count_d, count_s, bot_ver, servers, users, pid):
    embed=discord.Embed(title="System Information")
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.add_field(name="Bot ID", value=str(uid), inline=True)
    embed.add_field(name="Uptime", value=uptime, inline=True)
    embed.add_field(name="Command count", value=str(count_d) + " (Total " + str(count_s) + ")", inline=True)
    embed.add_field(name="Instance count", value=str(servers) + " servers, " + str(users) + " users", inline=True)
    embed.add_field(name="Self MD5 Hash", value=hash_str, inline=True)
    embed.add_field(name="Environment", value=str(os.popen("uname -s").read()), inline=True)
    embed.add_field(name="Process ID", value=str(pid), inline=True)
    embed.add_field(name="Python version", value=cpuinfo.get_cpu_info()["python_version"], inline=True)
    embed.add_field(name="Processor", value=cpuinfo.get_cpu_info()["brand"], inline=True)
    embed.add_field(name="Memory", value=str(int(psutil.virtual_memory().total / 1048576)) + " MB of total RAM\n" + str(int(memkb / 1024)) + " KB using by bot", inline=True)
    embed.set_footer(text="ver " + bot_ver + ", food database ver " + m_food.DB_VERSION)
    return embed

def bday():
    embed=discord.Embed(title="저는 2017년 5월 9일에 태어났어요!", color=0xffff00)
    embed.set_footer(text="(C) 2017 - 2019 libertin")
    return embed

def get_info_public(client, bot_ver, uptime, servername):
    embed=discord.Embed(title="시스템 정보", color=0xffffff)
    embed.set_author(name="기계식 루냥이",icon_url=client.user.avatar_url)
    embed.add_field(name="버전", value="봇 시스템 버전 " + bot_ver + "\n음식 추천 데이터베이스 버전 " + m_food.DB_VERSION + " (항목 " + m_food.ELEMENT_COUNT + "개)", inline=True)
    embed.add_field(name="컨테이너", value=servername, inline=True)
    embed.add_field(name="동작 시간", value=uptime, inline=True)
    return embed

def source_code():
    embed=discord.Embed(title="소스 코드", description="[https://github.com/LunaNyan/Luna_Libertin_Discord_Bot](https://github.com/LunaNyan/Luna_Libertin_Discord_Bot)", color=0x7777ff)
    embed.add_field(name="라이센스", value="기계식 루냥이는 MIT 라이센스로 제공됩니다\n자세한 사항은 [여기를 참고해주세요](https://www.olis.or.kr/license/Detailselect.do?lId=1006&mapCode=010006)", inline=False)
    return embed

def selfintro(client, bot_ver):
    embed=discord.Embed(title="기계식 루냥이", description="우리들만의 Discord 봇", color=0xffffff)
    embed.add_field(name="제작자", value="[libertin#2340](https://twitter.com/libertin_ko)", inline=True)
    embed.add_field(name="도와주신 분들", value="[Katinor](https://twitter.com/icoRayner)\nSeia\n[perillamint](https://twitter.com/perillamint)\n[yeoncomi](https://twitter.com/yeoncomi)", inline=True)
    embed.add_field(name="유용한 링크", value="[민원창구](https://discordapp.com/invite/yyS9x5V), [봇 초대하기](https://discordapp.com/oauth2/authorize?client_id=598080777565241354&scope=bot&permissions=388190), [공식 트위터](https://twitter.com/luna_libertin)", inline=False)
    embed.add_field(name="프로그램 저작권", value="해당 봇의 프로그램 데이터는 MIT 허가서에 의해 제공됩니다\n자세한 사항은 [여기를 참고해주세요](https://www.olis.or.kr/license/Detailselect.do?lId=1006&mapCode=010006)", inline=False)
    embed.add_field(name="프로필 이미지", value="해당 봇의 프로필 이미지는 [星海恋詩의 Picrew](https://picrew.me/image_maker/79516/)로 제작되었습니다\n봇의 제작자는 Picrew 제작자로부터 아이콘 이미지로서의 일러스트 사용을 허가받았습니다", inline=False)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.set_footer(text="Copyright (C) 2017 - 2019 libertin | v" + bot_ver)
    return embed

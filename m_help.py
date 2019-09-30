import discord, cpuinfo, psutil, os, math, m_food

def help(user, client, text, bot_ver):
    a = text
    a = a.replace('루냥아 ', '')
    a = a.replace(' 도와줘', '')
    if text == '루냥아 도와줘':
        embed=discord.Embed(title="기계식 루냥이를 초대해주셔서 감사합니다!", description='루냥아 (항목) 도와줘를 입력하세요!\n전체 명령어 목록을 보시려면 "루냥아 전체 명령어 도와줘"를 입력하세요!\n[민원창구](https://discordapp.com/invite/yyS9x5V), [봇 초대하기](https://discordapp.com/oauth2/authorize?client_id=598080777565241354&scope=bot&permissions=388190), [공식 트위터](https://twitter.com/luna_libertin)', color=0xff0080)
        embed.add_field(name="도움말", value="기계식 루냥이를 이용하는 방법을 알려줘요!", inline=False)
        embed.add_field(name="커뮤니티", value="다른 서버의 사람들과 소통할 수 있는 광장", inline=False)
        embed.add_field(name="프로필", value="자기소개와 계정 정보를 볼 수 있는 곳", inline=False)
        embed.add_field(name="정보", value="기계식 루냥이에 대한 여러가지 정보", inline=False)
        embed.add_field(name="게임", value="기계식 루냥이와 놀기", inline=False)
        embed.add_field(name="대화", value="기계식 루냥이와 대화하기", inline=False)
        embed.add_field(name="유용한 기능", value="유용한 도구 모음", inline=False)
        embed.add_field(name="서버 지정 명령어", value="루냥이에게 명령어를 가르쳐보세요!", inline=False)
        embed.set_footer(text='Copyright (C) 2017 - 2019 libertin | ver ' + bot_ver)
    elif a == '전체 명령어':
        embed=discord.Embed(title="도움말", description="전체 명령어 목록", color=0x8080ff)
        embed.add_field(name="도움말", value="루냥아 (항목) 도와줘, 루냥아 누구니, 루냥아 소스코드", inline=False)
        embed.add_field(name="커뮤니티", value="루냥아 공지사항 목록, 루냥아 공지사항 (숫자), 루냥아 방명록, 루냥아 방명록 쓰기 (할 말)", inline=False)
        embed.add_field(name="프로필", value="루냥아 출석체크, 루냥아 나 어때, 루냥아 (멘션) 어때, 루냥아 소개말 (자기소개), 루냥아 거울 (멘션), 루냥아 닉변 (닉네임)", inline=False)
        embed.add_field(name="정보", value="루냥아 서버정보, 루냥아 인기도, 루냥아 서버목록, 루냥아 생일, 루냥아 버전, 루냥아 후원", inline=False)
        embed.add_field(name="대화", value="루냥아 배고파, 루냥이 귀여워, 루냥이 쓰담쓰담, 루냥이 꼬옥, 루냥이 부비부비, 루냥아 (물체) 먹어, 와! 샌즈!, 루냥아 짖어, 루냥아 손, 루냥아 점프, 루냥아 굴러", inline=False)
        embed.add_field(name="게임", value="루냥아 섯다, 루냥아 제비뽑기, 루냥아 가위바위보", inline=False)
        embed.add_field(name="유용한 기능", value="루냥아 계산해줘 (계산식), 루냥아 계산해줘 이미지 (계산식), 루냥아 확성기, 루냥아 골라줘, 루냥아 섞어줘 (선택지1) (선택지2) .., 루냥아 주사위, 루냥아 행운의숫자, 루냥아 핑", inline=False)
        embed.add_field(name="서버 지정 명령어", value="루냥아 배워, 루냥아 잊어, 루냥아 배운거", inline=False)
        embed.add_field(name="패시브", value="관심 가져주기, 불타는 서버", inline=False)
        if user.guild_permissions.administrator:
            embed.add_field(name="관리자", value='자세한 사항은 "루냥아 관리자 도와줘"를 입력하세요!', inline=False)
    elif a == '도움말':
        embed=discord.Embed(title="도움말", description="도움말 항목", color=0x8080ff)
        embed.add_field(name="루냥아 (항목) 도와줘", value="각 항목에 대한 도움말을 표시합니다\n항목을 지정하지 않았다면 도움말 홈이 표시됩니다", inline=False)
        embed.add_field(name="루냥아 누구니", value="자기소개와 제작자 목록을 표시합니다", inline=False)
        embed.add_field(name="루냥아 소스코드", value="기계식 루냥이의 GitHub 레포지토리를 표시합니다", inline=False)
    elif a == '커뮤니티':
        embed=discord.Embed(title="도움말", description="커뮤니티 항목", color=0x8080ff)
        embed.add_field(name="루냥아 공지사항 목록", value="공지사항 목록을 불러옵니다", inline=False)
        embed.add_field(name="루냥아 공지사항 (번호)", value="목록에 해당하는 번호의 공지사항을 읽습니다\n번호가 없으면 첫번째 공지사항을 읽습니다", inline=False)
        embed.add_field(name="루냥아 방명록", value="방명록을 표시합니다", inline=False)
        embed.add_field(name="루냥아 방명록 쓰기 (할 말)", value="방명록에 글을 씁니다", inline=False)
        embed.add_field(name="루냥아 거울 (멘션)", value="자신 또는 멘션된 계정의 프로필 사진을 보여줍니다", inline=False)
    elif a == '프로필':
        embed=discord.Embed(title="도움말", description="프로필 항목", color=0x8080ff)
        embed.add_field(name="루냥아 출석체크", value="출석을 체크합니다", inline=False)
        embed.add_field(name="루냥아 나 어때", value="사용자 정보를 불러옵니다", inline=False)
        embed.add_field(name="루냥아 (멘션) 어때", value="다른 사용자의 정보를 불러옵니다", inline=False)
        embed.add_field(name="루냥아 소개말 (자기소개)", value="사용자 정보에 표시되는 소개말을 설정합니다", inline=False)
        embed.add_field(name="루냥아 거울 (멘션)", value="멘션된 유저, 또는 멘션이 없는 경우 자신의 프로필 사진을 불러옵니다", inline=False)
        embed.add_field(name="루냥아 닉변 (닉네임)", value="닉네임을 변경합니다", inline=False)
    elif a == '정보':
        embed=discord.Embed(title="도움말", description="정보 항목", color=0x8080ff)
        embed.add_field(name="루냥아 서버정보", value="서버 정보를 불러옵니다", inline=False)
        embed.add_field(name="루냥아 인기도", value="몇개의 서버에서 몇명의 유저들이 저를 보고 있는지 알려줘요!", inline=False)
        embed.add_field(name="루냥아 자가진단", value="봇이 정상 동작할 수 있는지 점검합니다", inline=False)
        embed.add_field(name="루냥아 서버목록", value="서버 목록을 불러옵니다", inline=False)
        embed.add_field(name="루냥아 생일", value="봇이 언제 탄생했는지 알려줍니다", inline=False)
        embed.add_field(name="루냥아 버전", value="봇의 버전, 서버 상태, 제작진을 보여줍니다", inline=False)
        embed.add_field(name="루냥아 후원", value="후원 계좌와 리워드를 표시합니다", inline=False)
    elif a == '대화':
        embed=discord.Embed(title="도움말", description="대화 항목", color=0x8080ff)
        embed.add_field(name="루냥아 배고파", value="랜덤으로 음식을 추천해줍니다 (음식을 사주지는 않습니다!)", inline=False)
        embed.add_field(name="루냥이 귀여워", value="자기 자신을 귀여워합니다 (루냥이 커여워, 귀냥이 루여워, 커냥이 루여워 도 가능합니다)", inline=False)
        embed.add_field(name="루냥이 쓰담쓰담", value="쓰다듬는 짤을 가져옵니다", inline=False)
        embed.add_field(name="루냥이 꼬옥", value="껴안는 짤을 가져옵니다", inline=False)
        embed.add_field(name="루냥이 부비부비", value="얼굴을 부비는 짤을 가져옵니다", inline=False)
        embed.add_field(name="루냥아 (물체) 먹어", value="물체를 먹습니다(?)", inline=False)
        embed.add_field(name="와! 샌즈!", value="언더테일 아시는구나!", inline=False)
        embed.add_field(name="기타 대화 명령어", value="루냥아 짖어, 루냥아 손, 루냥아 점프, 루냥아 굴러", inline=False)
    elif a == '게임':
        embed=discord.Embed(title="도움말", description="게임", color=0xffff00)
        embed.set_author(name="게임 사용 방법 보기 : 루냥아 게임 (게임이름) 도와줘")
        embed.add_field(name="섯다", value="CPU와 두장섯다를 진행합니다", inline=False)
        embed.add_field(name="제비뽑기", value="CPU가 제비뽑기를 실행합니다", inline=False)
        embed.add_field(name="가위바위보", value="CPU와 가위바위보를 진행합니다", inline=False)
    elif a == '게임 섯다':
        embed=discord.Embed(title="두장섯다 사용 방법", description="명령어 : 루냥아 섯다 (숫자1) (숫자2), 0~9까지의 숫자 두개를 입력해 진행합니다", color=0xffff00)
        embed.add_field(name="족보 순위", value="땡 > 삥 > 끗", inline=False)
        embed.add_field(name="땡", value="두 패가 같은 경우 (장땡 ~ 삥땡)", inline=False)
        embed.add_field(name="삥", value="알리(1+2), 독사(1+4), 구삥(1+9), 장삥(1+10), 장사(4+10), 세륙(4+6)", inline=False)
        embed.add_field(name="끗", value="두 패 합의 일의 자리 숫자 (갑오 ~ 망통)", inline=False)
    elif a == '게임 제비뽑기':
        embed=discord.Embed(title="제비뽑기 사용 방법", description="명령어 : 루냥아 제비뽑기 (선택지1) (선택지2) ... , (결과1) (결과2) ...", color=0xffff00)
        embed.add_field(name="사용 방법", value="각 항목은 띄어쓰기로 구분, 선택지와 결과는 쉼표(,)로 구분!", inline=False)
        embed.add_field(name="주의사항", value="선택지와 결과의 개수는 동일해야 합니다", inline=True)
    elif a == '게임 가위바위보':
        embed=discord.Embed(title="가위바위보 사용 방법", description="명령어 : 루냥아 가위바위보 (선택지)", color=0xffff00)
        embed.add_field(name="선택지", value="가위, 바위, 보", inline=False)
    elif a == '유용한 기능':
        embed=discord.Embed(title="도움말", description="유용한 기능", color=0x00ff00)
        embed.add_field(name="루냥아 계산해줘 (계산식)", value="Wolfram|Alpha 계산 쿼리를 제공합니다", inline=False)
        embed.add_field(name="루냥아 계산해줘 이미지 (계산식)", value="Wolfram|Alpha 플롯 계산 쿼리를 제공합니다(실험적인 기능입니다!)", inline=False)
        embed.add_field(name="루냥아 골라줘 (선택지1) (선택지2) ...", value="어느것을 고를까요 알아맞춰 봅시다", inline=False)
        embed.add_field(name="루냥아 확성기 (할 말)", value="루냥이가 대신 말해줍니다 (혐오 단어가 감지되는 경우 거부됩니다)", inline=False)
        embed.add_field(name="루냥아 서버목록", value="이 봇이 활동중인 서버들의 목록을 불러옵니다", inline=False)
        embed.add_field(name="루냥아 섞어줘 (선택지1) (선택지2) ...", value="선택지들의 순서를 섞어줍니다", inline=False)
        embed.add_field(name="루냥아 주사위", value="1부터 6까지 무작위의 숫자를 출력합니다", inline=False)
        embed.add_field(name="루냥아 행운의숫자", value="1부터 100 중의 숫자를 무작위로 선택합니다", inline=False)
        embed.add_field(name="루냥아 핑", value="봇의 응답 시간을 조회합니다", inline=False)
    elif a == '서버 지정 명령어':
        embed=discord.Embed(title="서버 지정 명령어", description="서버 지정 명령어는 '루냥아 (명령어)'로 동작시킵니다\n\n루냥이가 배운 명령어는 해당 서버에서만 동작합니다\n이미 존재하는 서버 지정 명령어를 배우도록 시키면 명령어가 수정됩니다\n**봇의 기본 명령어는 배워도 동작하지 않습니다**", color=0x00ff00)
        embed.add_field(name="루냥아 배워 (명령어) | (반응)", value="서버 지정 명령어를 생성합니다\n[멘션] : 명령어 사용자의 멘션\n[이름] : 명령어 사용자의 닉네임\n여러개의 반응 중 랜덤으로 반응하기를 원할 때 && 으로 구분할 수 있습니다", inline=False)
        embed.add_field(name="루냥아 잊어 (명령어)", value="서버 지정 명령어를 삭제합니다", inline=False)
        embed.add_field(name="루냥아 배운거", value="서버 지정 명령어 목록을 확인합니다", inline=False)
    elif a == '패시브':
        embed=discord.Embed(title="도움말", description="패시브", color=0x0000ff)
        embed.add_field(name="관심 가져주기", value='채팅을 많이 치고 있을 때 일정 확률로 관심을 가져줍니다\n호감도가 친구 이상일 때 동작합니다\n"루냥아 관심 가져주기"로 토글이 가능합니다', inline=False)
        embed.add_field(name="불타는 서버", value='서버에서 명령어가 아닌 채팅을 많이 치고 있을 때 일정 확률로 관심을 가져줍니다\n관리자인 경우 "루냥아 불타는 서버"로 토글이 가능합니다', inline=False)
    elif user.guild_permissions.administrator:
        if a == '관리자':
            embed=discord.Embed(title="관리자 기능 도움말", description="명령어 목록", color=0xff0000)
            embed.add_field(name="공지", value="루냥아 공지채널 추가, 루냥아 공지채널 삭제", inline=False)
            embed.add_field(name="기록", value="루냥아 로그채널 생성", inline=False)
            embed.add_field(name="채널", value="루냥아 환영인사 (메시지), 루냥아 작별인사 (메시지), 루냥아 금지채널 추가, 루냥아 금지채널 삭제, 루냥아 채널연결 생성, 루냥아 채널연결 접속 (코드), 루냥아 채널연결 삭제", inline=False)
            embed.add_field(name="모더레이션", value="루냥아 뮤트 (멘션), 루냥아 언뮤트 (멘션), 루냥아 킥 (멘션), 루냥아 밴 (멘션 또는 고유 ID)", inline=False)
            embed.add_field(name="기타", value="루냥아 지워줘 (5~100), 루냥아 초대링크 생성, 루냥아 자가진단", inline=False)
        elif a == '관리자 공지':
            embed=discord.Embed(title="관리자 기능 도움말", description="공지", color=0xff0000)
            embed.add_field(name="루냥아 공지채널 추가", value="현재 채널을 알림 채널로 추가합니다", inline=False)
            embed.add_field(name="루냥아 공지채널 삭제", value="현재 채널을 알림 채널에서 삭제합니다", inline=False)
        elif a == '관리자 기록':
            embed=discord.Embed(title="관리자 기능 도움말", description="기록", color=0xff0000)
            embed.add_field(name="루냥아 로그채널 생성", value="메시지 수정, 삭제, 확성기 사용을 기록해주는 채널을 생성합니다\n비활성화를 원할 시 기록 채널을 삭제하면 됩니다", inline=False)
        elif a == '관리자 채널':
            embed=discord.Embed(title="관리자 기능 도움말", description="채널", color=0xff0000)
            embed.add_field(name="루냥아 환영인사 (메시지)", value="서버에 유저가 들어왔을 때 해당 채널에 표시할 메시지를 지정합니다\n'루냥아 환영인사 삭제'로 메시지를 삭제합니다\n[멘션] : 사용자 멘션\n[이름] : 사용자 이름", inline=False)
            embed.add_field(name="루냥아 작별인사 (메시지)", value="서버에서 유저가 나갔을 때 해당 채널에 표시할 메시지를 지정합니다\n'루냥아 작별인사 삭제'로 메시지를 삭제합니다\n[이름] : 사용자 이름", inline=False)
            embed.add_field(name="루냥아 금지채널 추가", value="해당 채널에서 명령어 사용을 금지합니다", inline=False)
            embed.add_field(name="루냥아 금지채널 삭제", value="해당 채널을 명령어 금지 채널에서 삭제합니다", inline=False)
            embed.add_field(name="루냥아 애드블락 추가", value="해당 채널에서 초대 링크 첨부를 금지합니다", inline=False)
            embed.add_field(name="루냥아 애드블락 삭제", value="해당 채널을 코대 링크 첨부 금지 채널에서 삭제합니다", inline=False)
            embed.add_field(name="루냥아 채널연결 생성", value="채널 간 1:1 텍스트 채팅 연결을 준비합니다", inline=False)
            embed.add_field(name="루냥아 채널연결 접속 (코드)", value="부여받은 접속 코드로 채널을 연결합니다", inline=False)
            embed.add_field(name="루냥아 채널연결 삭제", value="채널 연결을 삭제합니다", inline=False)
        elif a == '관리자 모더레이션':
            embed=discord.Embed(title="관리자 기능 도움말", description="모더레이션", color=0xff0000)
            embed.add_field(name="루냥아 뮤트 (멘션)", value="멘션된 사용자를 뮤트(채팅금지)합니다", inline=False)
            embed.add_field(name="루냥아 언뮤트 (멘션)", value="멘션된 사용자의 뮤트(채팅금지)를 해제합니다", inline=False)
            embed.add_field(name="루냥아 킥 (멘션)", value="사용자를 추방(kick)합니다", inline=False)
            embed.add_field(name="루냥아 밴 (멘션 또는 고유 ID)", value="사용자를 차단(ban)합니다", inline=False)
            embed.set_footer(text="주의 : 모든 모더레이션 기능은 사전 확인 없이 바로 진행되므로 신중히 사용하시기 바랍니다")
        elif a == '관리자 기타':
            embed=discord.Embed(title="관리자 기능 도움말", description="기타", color=0xff0000)
            embed.add_field(name="루냥아 유저패시브", value="현재 서버에서 사용자 패시브 허용 여부를 토글합니다", inline=False)
            embed.add_field(name="루냥아 지워줘 (5~100)", value="주어진 개수만큼 메시지를 삭제합니다", inline=False)
            embed.add_field(name="루냥아 초대링크 생성", value="즉석 초대 링크를 생성합니다", inline=False)
            embed.add_field(name="루냥아 자가진단", value="봇이 사용 가능한 권한을 확인합니다", inline=False)
    else:
        embed=discord.Embed(title='해당 항목에 대한 도움말을 찾을 수 없어요!', description='전체 도움말을 원하신다면 "루냥아 전체 명령어 도와줘"를 입력해주세요!')
    return embed

def servers_list(client, page):
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
        embed=discord.Embed(title="전체 서버 목록 (총 " + str(len(lk)) + "개)", color=0xff00ff)
        c = (page - 1) * 10
        ct = c + 9
        while c <= ct:
            try:
                embed.add_field(name="#" + str(c+1) + " : " + lk[c], value="유저 수 : " + lu[c] + ", 서버 주인 : " + lo[c], inline=False)
                c += 1
            except:
                break
        embed.set_footer(text=str(page) + ' / ' + str(pages) + ' 페이지, 다른 페이지 보기 : "루냥아 서버목록 (페이지)"')
    return embed

def test_features(db, bot_ver):
    embed=discord.Embed(title="기계식 루냥이 테스트존에 오신 것을 환영합니다!", description=db.get("etc", "test_features"), color=0xff00ff)
    embed.set_footer(text="ver " + bot_ver)
    return embed

def donation():
    embed=discord.Embed(title="기계식 루냥이를 지원해주세요!", color=0xffccff)
    embed.add_field(name="후원 계좌", value="하나은행 538-910289-86107", inline=False)
    embed.add_field(name="후원 리워드", value="- 후원자 칭호\n- (10,000원 이상 후원 시) Nitro Classic 1개월, 컬쳐랜드 문화상품권 5,000원권 중 택1\n\n후원 리워드를 받으려면 [공식 트위터](https://twitter.com/luna_libertin) 또는 libertin#2340에 DM을 남겨주세요!)", inline=False)
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
    embed.add_field(name="Discord.py version", value=discord.__version__, inline=True)
    embed.add_field(name="Processor", value=cpuinfo.get_cpu_info()["brand"], inline=True)
    embed.add_field(name="Memory", value=str(int(psutil.virtual_memory().total / 1048576)) + " MB of total RAM\n" + str(int(memkb / 1024)) + " KB using by bot", inline=True)
    embed.set_footer(text="ver " + bot_ver + ", food database ver " + m_food.DB_VERSION)
    return embed

def bday():
    embed=discord.Embed(title="저는 2017년 5월 9일에 태어났어요!", color=0xffff00)
    embed.set_footer(text="Copyright (C) 2017 - 2019 libertin")
    return embed

def get_info_public(client, bot_ver, servername):
    embed=discord.Embed(title="시스템 정보", color=0xffffff)
    embed.set_author(name="기계식 루냥이",icon_url=client.user.avatar_url)
    embed.add_field(name="버전", value="봇 시스템 버전 " + bot_ver + "\n음식 추천 데이터베이스 버전 " + m_food.DB_VERSION + " (항목 " + m_food.ELEMENT_COUNT + "개)", inline=True)
    embed.add_field(name="컨테이너", value=servername, inline=True)
    return embed

def source_code():
    embed=discord.Embed(title="소스 코드", description="[https://github.com/LunaNyan/Luna_Libertin_Discord_Bot](https://github.com/LunaNyan/Luna_Libertin_Discord_Bot)", color=0x7777ff)
    embed.add_field(name="라이센스", value="기계식 루냥이는 MIT 라이센스로 제공됩니다\n자세한 사항은 [여기를 참고해주세요](https://www.olis.or.kr/license/Detailselect.do?lId=1006&mapCode=010006)", inline=False)
    return embed

def selfintro(client, bot_ver):
    embed=discord.Embed(title="기계식 루냥이", color=0xffffff)
    embed.add_field(name="제작자", value="[libertin#2340](https://twitter.com/libertin_ko)", inline=True)
    embed.add_field(name="도와주신 분들", value="[Katinor](https://twitter.com/icoRayner)\nSeia\n[perillamint](https://twitter.com/perillamint)", inline=True)
    embed.add_field(name="유용한 링크", value="[민원창구](https://discordapp.com/invite/yyS9x5V), [봇 초대하기](https://discordapp.com/oauth2/authorize?client_id=598080777565241354&scope=bot&permissions=388190), [공식 트위터](https://twitter.com/luna_libertin)", inline=False)
    embed.add_field(name="프로그램 저작권", value="해당 봇의 프로그램 데이터는 MIT 허가서에 의해 제공됩니다\n자세한 사항은 [여기를 참고해주세요](https://www.olis.or.kr/license/Detailselect.do?lId=1006&mapCode=010006)", inline=False)
    embed.add_field(name="프로필 이미지", value="해당 봇의 프로필 이미지는 [星海恋詩의 Picrew](https://picrew.me/image_maker/79516/)로 제작되었습니다\n봇의 제작자는 Picrew 제작자로부터 아이콘 이미지로서의 일러스트 사용을 허가받았습니다", inline=False)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.set_footer(text="Copyright (C) 2017 - 2019 libertin | v" + bot_ver)
    return embed

def permcheck(me):
    embed=discord.Embed(title="권한 자가진단 결과", color=0xff77ff)
    heart_yes = ":green_heart: 정상"
    heart_no = ":broken_heart: 오류"
    if me.administrator:
        l_admin = heart_yes
    else:
        l_admin = heart_no
    if me.manage_channels:
        l_manch = heart_yes
    else:
        l_manch = heart_no
    if me.kick_members:
        l_kick = heart_yes
    else:
        l_kick = heart_no
    if me.ban_members:
        l_ban = heart_yes
    else:
        l_ban = heart_no
    if me.read_message_history:
        l_history = heart_yes
    else:
        l_history = heart_no
    if me.manage_messages:
        l_manm = heart_yes
    else:
        l_manm = heart_no
    if me.create_instant_invite:
        l_inv = heart_yes
    else:
        l_inv = heart_no
    embed.add_field(name="관리자", value=l_admin, inline=True)
    embed.add_field(name="채널 관리하기", value=l_manch, inline=True)
    embed.add_field(name="멤버 추방하기", value=l_kick, inline=True)
    embed.add_field(name="멤버 차단하기", value=l_ban, inline=True)
    embed.add_field(name="메시지 기록 보기", value=l_history, inline=True)
    embed.add_field(name="메시지 관리하기", value=l_manm, inline=True)
    embed.add_field(name="즉석 초대 만들기", value=l_inv, inline=True)
    return embed

def suggest_game():
    embed=discord.Embed(title="저와 게임을 해보시는건 어때요?", description='저에겐 다양한 게임 기능이 있어요!\n게임 규칙 등의 자세한 정보를 보고 싶다면 "루냥아 게임 (게임이름) 도와줘"를 입력해보세요!', color=0xffff00)
    embed.add_field(name="섯다", value="CPU와 두장섯다를 진행합니다", inline=False)
    embed.add_field(name="제비뽑기", value="CPU가 제비뽑기를 실행합니다", inline=False)
    embed.add_field(name="가위바위보", value="CPU와 가위바위보를 진행합니다", inline=False)
    return embed

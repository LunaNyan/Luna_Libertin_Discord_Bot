import discord, cpuinfo, psutil, os, math, m_food, m_lang

def help(user, client, text, bot_ver, head, mode):
    # mode interpretation
    # True    : 루냥아 ㅇㅇ 도와줘
    # False   : 루냥아 도와줘 ㅇㅇ
    a = text
    if mode == True:
        a = a.replace(head, '')
        a = a.replace(' 도와줘', '')
    else:
        a = a.replace(head + '도와줘 ', '')
    if text == head + '도와줘':
        embed=discord.Embed(title="기계식 루냥이를 초대해주셔서 감사합니다!", description='루냥아 (항목) 도와줘를 입력하세요!\n전체 명령어 목록을 보시려면 "루냥아 전체 명령어 도와줘"를 입력하세요!\n[민원창구](https://discordapp.com/invite/yyS9x5V), [봇 초대하기](https://discordapp.com/oauth2/authorize?client_id=598080777565241354&scope=bot&permissions=388190)', color=0xff0080)
        embed.add_field(name="도움말", value="기계식 루냥이를 이용하는 방법을 알려줘요!", inline=False)
        embed.add_field(name="커뮤니티", value="다른 서버의 사람들과 소통할 수 있는 광장", inline=False)
        embed.add_field(name="프로필", value="자기소개와 계정 정보를 볼 수 있는 곳", inline=False)
        embed.add_field(name="서버", value="현재 서버에 대한 정보를 볼 수 있는 곳", inline=False)
        embed.add_field(name="정보", value="기계식 루냥이에 대한 여러가지 정보", inline=False)
        embed.add_field(name="게임", value="기계식 루냥이와 놀기", inline=False)
        embed.add_field(name="대화", value="기계식 루냥이와 대화하기", inline=False)
        embed.add_field(name="유용한 기능", value="유용한 도구 모음", inline=False)
        embed.set_footer(text='Copyright (C) 2017 - 2020 STUDIO ONE | ver ' + bot_ver)
    elif a == '전체 명령어':
        embed=discord.Embed(title="도움말", description="전체 명령어 목록", color=0x8080ff)
        embed.add_field(name="도움말", value="루냥아 (항목) 도와줘, 루냥아 누구니, 루냥아 소스코드", inline=False)
        embed.add_field(name="커뮤니티", value="루냥아 공지사항 목록, 루냥아 공지사항 (숫자), 루냥아 방명록, 루냥아 방명록 쓰기 (할 말), 루냥아 서버랭킹, 루냥아 호감도랭킹", inline=False)
        embed.add_field(name="프로필", value="루냥아 출석체크, 루냥아 나 어때, 루냥아 (멘션) 어때, 루냥아 소개말 (자기소개), 루냥아 거울 (멘션), 루냥아 닉변 (닉네임), 루냥아 생성일시공개, 루냥아 반모", inline=False)
        embed.add_field(name="메모", value="루냥아 메모 (내용), 루냥아 메모 목록 (페이지), 루냥아 메모 삭제 (번호)", inline=False)
        embed.add_field(name="서버", value="루냥아 서버정보, 루냥아 서버설정, 루냥아 서버아이콘, 루냥아 가입일시공개, 루냥아 배워, 루냥아 잊어, 루냥아 배운거", inline=False)
        embed.add_field(name="정보", value="루냥아 이용약관, 루냥아 인기도, 루냥아 서버목록, 루냥아 생일, 루냥아 성능, 루냥아 후원", inline=False)
        embed.add_field(name="대화", value="루냥아 배고파, 루냥이 귀여워, 루냥이 쓰담쓰담, 루냥이 꼬옥, 루냥이 부비부비, 루냥아 (물체) 먹어, 와! 샌즈!, 루냥아 짖어, 루냥아 손, 루냥아 점프, 루냥아 굴러", inline=False)
        embed.add_field(name="게임", value="루냥아 섯다, 루냥아 제비뽑기, 루냥아 가위바위보, 루냥아 로또", inline=False)
        embed.add_field(name="유용한 기능", value="루냥아 계산해줘 (계산식), 루냥아 계산해줘 이미지 (계산식), 루냥아 확성기, 루냥아 골라줘, 루냥아 섞어줘 (선택지1) (선택지2) .., 루냥아 주사위, 루냥아 행운의숫자, 루냥아 핑, 루냥아 색상 (색상코드), 루냥아 받아쓰기 (텍스트), 루냥아 야짤 (태그)", inline=False)
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
        embed.add_field(name="루냥아 서버랭킹", value="유저 수가 가장 많은 10개의 서버 랭킹을 보여줍니다", inline=False)
        embed.add_field(name="루냥아 호감도랭킹", value="호감도가 가장 높은 10개의 유저 랭킹을 보여줍니다", inline=False)
    elif a == '프로필':
        embed=discord.Embed(title="도움말", description="프로필 항목", color=0x8080ff)
        embed.add_field(name="루냥아 출석체크", value="출석을 체크합니다", inline=False)
        embed.add_field(name="루냥아 나 어때", value="사용자 정보를 불러옵니다", inline=False)
        embed.add_field(name="루냥아 (멘션) 어때", value="다른 사용자의 정보를 불러옵니다", inline=False)
        embed.add_field(name="루냥아 소개말 (자기소개)", value="사용자 정보에 표시되는 소개말을 설정합니다", inline=False)
        embed.add_field(name="루냥아 거울 (멘션)", value="멘션된 유저, 또는 멘션이 없는 경우 자신의 프로필 사진을 불러옵니다", inline=False)
        embed.add_field(name="루냥아 닉변 (닉네임)", value="닉네임을 변경합니다", inline=False)
        embed.add_field(name="루냥아 생성일시공개", value="계정의 생성 일시 공개 여부를 토글합니다", inline=False)
        embed.add_field(name="루냥아 반모", value="반말모드 사용 여부를 토글합니다", inline=False)
    elif a == '메모':
        embed=discord.Embed(title="도움말", description="메모 항목", color=0xffff00)
        embed.add_field(name="루냥아 메모 (내용)", value="최대 30개까지 메모를 작성합니다\n작성된 메모는 목록 첫번째 위치에 기록됩니다", inline=False)
        embed.add_field(name="루냥아 메모 목록 (페이지)", value="페이지에 해당하는 메모 목록, 또는 페이지가 없는 경우 첫번째 페이지의 메모 목록을 보여줍니다", inline=False)
        embed.add_field(name="루냥아 메모 삭제 (번호)", value="목록 번호에 해당하는 메모를 삭제합니다", inline=False)
    elif a == '서버':
        embed=discord.Embed(title="도움말", description="서버 항목", color=0x8080ff)
        embed.add_field(name="루냥아 서버정보", value="서버 정보를 불러옵니다\n서버가 비공개로 설정되어 있는 경우 사용할 수 없는 명령어입니다", inline=False)
        embed.add_field(name="루냥아 서버설정", value="서버 설정을 불러옵니다", inline=False)
        embed.add_field(name="루냥아 서버아이콘", value="서버 아이콘을 불러옵니다", inline=False)
        embed.add_field(name="루냥아 가입일시공개", value="서버 가입 일시 표시 여부를 토글합니다", inline=False)
        embed.add_field(name="루냥아 배워 (명령어) | (반응)", value="서버 지정 명령어를 생성합니다\n[멘션] : 명령어 사용자의 멘션\n[이름] : 명령어 사용자의 닉네임\n여러개의 반응 중 랜덤으로 반응하기를 원할 때 && 으로 구분할 수 있습니다", inline=False)
        embed.add_field(name="루냥아 잊어 (명령어)", value="서버 지정 명령어를 삭제합니다", inline=False)
        embed.add_field(name="루냥아 배운거", value="서버 지정 명령어 목록을 확인합니다", inline=False)
    elif a == '정보':
        embed=discord.Embed(title="도움말", description="정보 항목", color=0x8080ff)
        embed.add_field(name="루냥아 이용약관", value="기계식 루냥이의 이용 약관을 표시합니다", inline=False)
        embed.add_field(name="루냥아 인기도", value="몇개의 서버에서 몇명의 유저들이 저를 보고 있는지 알려줘요!", inline=False)
        embed.add_field(name="루냥아 자가진단", value="봇이 정상 동작할 수 있는지 점검합니다", inline=False)
        embed.add_field(name="루냥아 서버목록", value="서버 목록을 불러옵니다", inline=False)
        embed.add_field(name="루냥아 생일", value="봇이 언제 탄생했는지 알려줍니다", inline=False)
        embed.add_field(name="루냥아 성능", value="봇의 버전, 서버 성능을 보여줍니다", inline=False)
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
        embed.add_field(name="로또", value="로또 게임을 진행합니다", inline=False)
    elif a == '게임 섯다' or a == '섯다':
        embed=discord.Embed(title="두장섯다 사용 방법", description="명령어 : 루냥아 섯다 (숫자1) (숫자2), 0~9까지의 숫자 두개를 입력해 진행합니다\n[확률 정보](http://121.1.120.57:50000/sd_percentage.htm)", color=0xffff00)
        embed.add_field(name="족보 순위", value="광땡 > 땡 > 삥 > 끗", inline=False)
        embed.add_field(name="3 - 8 광땡", value="3월 광 + 8월 광", inline=False)
        embed.add_field(name="1 - 8 광땡", value="1월 광 + 8월 광", inline=False)
        embed.add_field(name="1 - 3 광땡", value="1월 광 + 3월 광", inline=False)
        embed.add_field(name="땡", value="두 패의 월수가 같은 경우 (장땡 ~ 삥땡)", inline=False)
        embed.add_field(name="삥", value="알리(1+2), 독사(1+4), 구삥(1+9), 장삥(1+10), 장사(4+10), 세륙(4+6)", inline=False)
        embed.add_field(name="끗", value="두 패 합의 일의 자리 숫자 (갑오 > X끗 > 망통)", inline=False)
        embed.add_field(name="멍텅구리구사(멍구사, 9열+4열)", value="상대 족보가 9땡 이하인 경우 무승부, 이외에는 세끗", inline=False)
        embed.add_field(name="구사(9+4)", value="상대 족보가 알리 이하인 경우 무승부, 이외에는 세끗", inline=False)
        embed.add_field(name="7 - 4 암행어사(7열 + 4열)", value="상대 족보가 1 - 8 광땡 또는 1 - 3 광땡인 경우 승리, 이외에는 한끗", inline=False)
        embed.add_field(name="7 - 3 땡잡이(7열 + 3광)", value="상대 족보가 1 ~ 9땡인 경우 승리, 이외에는 망통(0끗)", inline=False)
        embed.set_footer(text="")
    elif a == '게임 제비뽑기' or a == '제비뽑기':
        embed=discord.Embed(title="제비뽑기 사용 방법", description="명령어 : 루냥아 제비뽑기 (선택지1) (선택지2) ... , (결과1) (결과2) ...", color=0xffff00)
        embed.add_field(name="사용 방법", value="각 항목은 띄어쓰기로 구분, 선택지와 결과는 쉼표(,)로 구분!", inline=False)
        embed.add_field(name="주의사항", value="선택지와 결과의 개수는 동일해야 합니다", inline=True)
    elif a == '게임 가위바위보' or a == '가위바위보':
        embed=discord.Embed(title="가위바위보 사용 방법", description="명령어 : 루냥아 가위바위보 (선택지)", color=0xffff00)
        embed.add_field(name="선택지", value="가위, 바위, 보", inline=False)
    elif a == '게임 로또' or a == '로또':
        embed=discord.Embed(title="로또 이용 방법")
        embed.add_field(name="명령어", value="루냥아 로또 (1~45 사이의 숫자 6개)", inline=False)
        embed.add_field(name="규칙", value="매일 0시에 갱신되는 로또 번호와 응모한 로또 번호가 몇 개나 동일한 지에 따라 등수가 정해집니다\n1등 : 4개 이상\n2등 : 3개\n3등 : 2개", inline=False)
        embed.add_field(name="결과 확인", value='루냥아 로또 결과', inline=False)
        embed.add_field(name="주의사항", value="같은 번호를 반복 응모할 수 없습니다")
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
        embed.add_field(name="루냥아 색상 (색상코드)", value="색상코드가 배경 색상으로 설정된 이미지를 반환합니다", inline=False)
        embed.add_field(name="루냥아 받아쓰기 (텍스트)", value="받은 텍스트를 이미지로 변환합니다", inline=False)
        embed.add_field(name="루냥아 야짤 (태그)", value="태그에 해당하는 야짤을 보여줍니다\n서버 관리자가 허용한 채널에 한해서만 동작합니다", inline=False)
    elif a == '패시브':
        embed=discord.Embed(title="도움말", description="패시브", color=0x0000ff)
        embed.add_field(name="관심 가져주기", value='채팅을 많이 치고 있을 때 일정 확률로 관심을 가져줍니다\n호감도가 친구 이상일 때 동작합니다\n"루냥아 관심 가져주기"로 토글이 가능합니다', inline=False)
        embed.add_field(name="불타는 서버", value='서버에서 명령어가 아닌 채팅을 많이 치고 있을 때 일정 확률로 관심을 가져줍니다\n관리자인 경우 "루냥아 불타는 서버"로 토글이 가능합니다', inline=False)
    elif user.guild_permissions.administrator:
        if a == '관리자':
            embed=discord.Embed(title="관리자 기능 도움말", description="명령어 목록", color=0xff0000)
            embed.add_field(name="공지", value="루냥아 공지채널 추가, 루냥아 공지채널 삭제", inline=False)
            embed.add_field(name="기록", value="루냥아 로그채널 생성", inline=False)
            embed.add_field(name="채널", value="루냥아 환영인사 (메시지), 루냥아 작별인사 (메시지), 루냥아 금지채널 추가, 루냥아 금지채널 삭제, 루냥아 채널연결 생성, 루냥아 채널연결 접속 (코드), 루냥아 채널연결 삭제, 루냥아 채널연결 정보, 루냥아 야짤채널, 루냥아 비밀채널 (숫자)", inline=False)
            embed.add_field(name="모더레이션", value="루냥아 뮤트 (멘션), 루냥아 언뮤트 (멘션), 루냥아 킥 (멘션), 루냥아 밴 (멘션 또는 고유 ID)", inline=False)
            embed.add_field(name="기타", value="루냥아 지워줘 (5~100), 루냥아 초대링크 생성, 루냥아 자가진단, 루냥아 서버공개, 루냥아 가입일시 전체공개, 루냥아 접두어 설정 (접두어), 루냥아 불타는 서버 문구, 루냥아 일상대화 접두어, 루냥아 서버 지정 명령어 접두어", inline=False)
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
            embed.add_field(name="루냥아 채널연결 정보", value="연결된 채널의 정보를 봅니다", inline=False)
            embed.add_field(name="루냥아 야짤채널", value="현재 채널의 야짤기능 허용 여부를 결정합니다", inline=False)
            embed.add_field(name="루냥아 비밀채널 (숫자)", value="현재 채널에 사라지는 메시지 기능을 활성화합니다", inline=False)
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
            embed.add_field(name="루냥아 서버공개", value="서버 공개 여부를 토글합니다\n서버가 비공개로 전환되는 경우 서버 목록에서 (비공개)로 표시되며 서버 정보 명령어를 입력할 수 없게 됩니다", inline=False)
            embed.add_field(name="루냥아 가입일시 전체공개", value="모든 사용자의 서버 가입 일시 공개 여부를 토글합니다", inline=False)
            embed.add_field(name="루냥아 접두어 설정 (접두어)", value="서버 지정 접두어를 설정합니다", inline=False)
            embed.add_field(name="루냥아 불타는 서버 문구", value="불타는 서버 패시브의 문구를 지정합니다", inline=False)
            embed.add_field(name="루냥아 일상대화 접두어", value="일상대화에 접두어를 필수로 요구할지 결정합니다", inline=False)
            embed.add_field(name="루냥아 서버 지정 명령어 접두어", value="서버 지정 명령어에 접두어를 필수로 요구할지 결정합니다", inline=False)
    else:
        embed=discord.Embed(title='해당 항목에 대한 도움말을 찾을 수 없어요!', description='전체 도움말을 원하신다면 "루냥아 전체 명령어 도와줘"를 입력해주세요!')
    return embed

def test_features(db, bot_ver):
    embed=discord.Embed(title="기계식 루냥이 테스트존에 오신 것을 환영합니다!", description=db.get("etc", "test_features"), color=0xff00ff)
    embed.set_footer(text="ver " + bot_ver)
    return embed

def donation():
    embed=discord.Embed(title="기계식 루냥이를 지원해주세요!", color=0xffccff)
    embed.add_field(name="후원 계좌", value="하나은행 538-910289-86107", inline=False)
    embed.add_field(name="후원 리워드", value="- 후원자 칭호\n- (10,000원 이상 후원 시) Nitro Classic 1개월, 컬쳐랜드 문화상품권 5,000원권 중 택1\n\n후원 리워드를 받으려면 libertin#2340에 DM을 남겨주세요!)", inline=False)
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

def get_info_public(uptime, servername, bot_ver):
    embed=discord.Embed(title="기계식 루냥이의 시스템 성능")
    embed.add_field(name="서버 이름", value=servername, inline=False)
    embed.add_field(name="CPU", value=cpuinfo.get_cpu_info()["brand"], inline=False)
    embed.add_field(name="RAM 용량", value=str(int(psutil.virtual_memory().total / 1048576)) + " MB")
    embed.add_field(name="Python 버전", value=cpuinfo.get_cpu_info()["python_version"].replace(".final.0", ""), inline=False)
    embed.add_field(name="Discord.py 버전", value=discord.__version__, inline=False)
    embed.add_field(name="동작 시간", value=uptime, inline=False)
    embed.add_field(name="버전", value="봇 시스템 버전 " + bot_ver + "\n음식 추천 데이터베이스 버전 " + m_food.DB_VERSION + " (항목 " + m_food.ELEMENT_COUNT + "개)", inline=True)
    return embed

def bday():
    embed=discord.Embed(title="저는 2017년 5월 9일에 태어났어요!", color=0xffff00)
    embed.set_footer(text="Copyright (C) 2017 - 2020 STUDIO ONE")
    return embed

def source_code():
    embed=discord.Embed(title="소스 코드", description="[https://github.com/LunaNyan/Luna_Libertin_Discord_Bot](https://github.com/LunaNyan/Luna_Libertin_Discord_Bot)", color=0x7777ff)
    embed.add_field(name="라이센스", value="기계식 루냥이는 MIT 라이센스로 제공됩니다\n자세한 사항은 [여기를 참고해주세요](https://www.olis.or.kr/license/Detailselect.do?lId=1006&mapCode=010006)", inline=False)
    return embed

def selfintro(client, bot_ver, message):
    embed=discord.Embed(title="기계식 루냥이", color=0xffffff)
    embed.add_field(name="총괄 관리자", value="[libertin](https://www.facebook.com/profile.php?id=100016101485889)", inline=True)
    embed.add_field(name="프로그래머", value="[Katinor](https://twitter.com/icoRayner)\n[Seia](https://twitter.com/Seia_Soto)", inline=True)
    embed.add_field(name="특별 감사", value="[SQUARE PIXELS](https://ez2ac.co.kr)\n[Scatter Lab](https://scatterlab.co.kr)\n" + message.author.name, inline=True)
    embed.add_field(name="유용한 링크", value="[민원창구](https://discordapp.com/invite/yyS9x5V), [봇 초대하기](https://discordapp.com/oauth2/authorize?client_id=598080777565241354&scope=bot&permissions=388190)", inline=False)
    embed.add_field(name="프로그램 저작권", value="해당 봇의 프로그램 데이터는 MIT 허가서에 의해 제공됩니다\n자세한 사항은 [여기를 참고해주세요](https://www.olis.or.kr/license/Detailselect.do?lId=1006&mapCode=010006)", inline=False)
    embed.add_field(name="프로필 이미지", value="해당 봇의 프로필 이미지는 [十九의 Picrew](https://picrew.me/image_maker/79516)로 제작되었습니다\n봇의 제작자는 Picrew 제작자로부터 아이콘 이미지로서의 일러스트 사용을 허가받았습니다", inline=False)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.set_footer(text="Copyright (C) 2017 - 2020 STUDIO ONE | ver " + bot_ver)
    return embed

def permcheck(me):
    embed=discord.Embed(title="권한 자가진단 결과", color=0xff77ff)
    heart_yes = ":green_heart: 정상"
    heart_no = ":broken_heart: 사용 불가능"
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

def suggest_game(db, id):
    embed=discord.Embed(title=m_lang.string(db, id, "suggest_game"), description=m_lang.string(db, id, "suggest_game_desc"), color=0xffff00)
    embed.add_field(name="사용 가능한 게임 종류", value="섯다, 가위바위보, 주사위", inline=False)
    return embed

def bot_welcome_message(client, bot_ver):
    des = '기계식 루냥이는 각종 유저 편의 기능과 서버 관리 기능을 포함하고 있는 종합 봇이예요!\n\n간단한 사용 방법은 **"루냥아 도와줘"**를 입력해 보세요!\n이용 약관은 **"루냥아 이용약관"**을 참조하세요!'
    embed=discord.Embed(title="기계식 루냥이를 초대해주셔서 감사합니다!", description=des)
    embed.add_field(name="봇을 설정하기 전에", value='기능 추가 등의 소식을 받아보려면 공지 받기를 원하는 채널에서 "루냥아 공지채널 추가"를 입력해주세요!')
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.set_footer(text="Copyright (C) 2017 - 2020 STUDIO ONE | ver " + bot_ver)
    return embed

def tos():
    embed=discord.Embed(title="기계식 루냥이 이용 약관")
    embed.add_field(name="수집하는 정보", value="기계식 루냥이는 서비스 제공을 위해 다음과 같은 정보를 수집합니다.\n- 봇이 반응하는 대화에 포함된 데이터\n- 채팅이 보내진 시간\n- 작성자의 고유번호\n- 작성된 서버의 고유번호\n- 작성된 서버내의 채널의 고유번호", inline=False)
    embed.add_field(name="수집된 정보의 사용", value="기계식 루냥이는 수집되는 정보를 본 용도로만 사용하며, 아래 명시된 용도 외에는 보관 및 사용되지 않습니다.\n- 방명록 등의 서비스를 위한 사용 내역 기록\n- 서비스 제공 (프로필, 게임) 등을 위한 데이터베이스 구축", inline=False)
    embed.add_field(name="이용약관의 동의", value="본 봇을 그룹에 초대하는 행위를 한다면 본 약관에 동의한 것으로 간주합니다.", inline=False)
    embed.add_field(name="이용계약의 해지", value="사용자가 이용약관에 반대할 경우 언제든지 서비스 받기를 중단할 수 있습니다. 이를 위해서는 그저 사용자가 초대한 서버/그룹/채널에서 본 봇을 내보내기만 하면 됩니다. 본 봇을 서버에서 내보낼 경우 관련된 데이터는 지체 없이 파기됩니다. 특별한 사유가 있다면 관리자에게 문의해주시기 바랍니다.")
    return embed

import discord

def help(client, text, bot_ver):
    a = text
    a = a.replace('_', '')
    a = a.replace('루냥아 도와줘', '')
    if a == '':
        embed=discord.Embed(title="기계식 루냥이를 초대해주셔서 감사합니다!", description="[민원창구](https://discordapp.com/invite/yyS9x5V) [봇 초대하기](https://discordapp.com/oauth2/authorize?client_id=598080777565241354&scope=bot&permissions=388160)", color=0xff0080)
        embed.set_author(name="기계식 루냥이 사용 방법",icon_url=client.user.avatar_url)
        embed.add_field(name="도움말", value="루냥아 도와줘 (항목), 루냥아 업데이트내역, 루냥아 나 어때", inline=False)
        embed.add_field(name="일상", value="루냥아 배고파, 루냥이 귀여워, 루냥이 쓰담쓰담, 루냥아 짖어봐, 루냥아 손, 루냥아 주사위, 루냥아 인기도, 와! 샌즈!", inline=False)
        embed.add_field(name="게임", value="루냥아 섯다", inline=False)
        embed.add_field(name="유용한 기능", value="루냥아 계산해줘 (계산식), 루냥아 계산해줘 이미지 (계산식), 루냥아 확성기, 루냥아 골라줘, 루냥아 서버목록", inline=False)
        embed.add_field(name="패시브", value="관심 가져주기", inline=False)
        embed.set_footer(text="Copyright (C) 2017 - 2019 libertin | v" + bot_ver)
    elif a == ' 일상':
        embed=discord.Embed(title="도움말", description="일상 항목", color=0x8080ff)
        embed.add_field(name="루냥아 배고파", value="랜덤으로 음식을 추천해줍니다 (음식을 사주지는 않습니다!)", inline=False)
        embed.add_field(name="루냥이 귀여워", value="자기 자신을 귀여워합니다 (루냥이 커여워, 귀냥이 루여워, 커냥이 루여워 도 가능합니다)", inline=False)
        embed.add_field(name="루냥이 쓰담쓰담", value="자기 자신한테 사이버(?) 쓰다듬을 선물해줍니다", inline=False)
        embed.add_field(name="루냥아 짖어봐", value="멍", inline=False)
        embed.add_field(name="루냥아 손", value=":raised_hand:", inline=False)
        embed.add_field(name="루냥아 인기도", value="몇개의 서버에서 몇명의 유저들이 저를 보고 있는지 알려줘요!", inline=False)
        embed.add_field(name="와! 샌즈!", value="언더테일 아시는구나!", inline=False)
    elif a == ' 게임':
        embed=discord.Embed(title="도움말", description="게임", color=0xffff00)
        embed.set_author(name="게임 사용 방법 보기 : 루냥아 도와줘 게임 (게임이름)")
        embed.add_field(name="섯다", value="CPU와 두장섯다를 진행합니다", inline=False)
        embed.add_field(name="제비뽑기", value="CPU가 제비뽑기를 실행합니다", inline=False)
        embed.add_field(name="루냥아 주사위", value="1부터 6까지 무작위의 숫자를 출력합니다", inline=False)
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
    else:
        embed=discord.Embed(title='전체 도움말을 원하신다면 그냥 "루냥아 도와줘"라고만 입력해주세요!')
    return embed

def servers_list(client):
    embed=discord.Embed(title="전체 서버 목록", color=0xff00ff)
    members_sum = 0
    for s in client.servers:
        embed.add_field(name=str(s), value="유저 수 : " + str(len(s.members)), inline=True)
        members_sum+= len(s.members)
    embed.set_footer(text="전제 서버 수 : " + str(len(client.servers)) + ", 전체 유저 수 : " + str(members_sum))
    return embed

def test_features(bot_ver):
    embed=discord.Embed(title="기계식 루냥이 테스트존에 오신 것을 환영합니다!", description="테스트 기능 목록", color=0xff00ff)
    embed.add_field(name="루냥아 서버목록", value="전체 서버 목록과 유저 수를 볼 수 있습니다", inline=False)
    embed.add_field(name="루냥아 나 어때", value="호감도와 프로필을 보여줍니다", inline=False)
    embed.set_footer(text="ver " + bot_ver)
    return embed

def ret_changelog():
    changelog = "```v1.10.0 (2019-07-31)\n"
    changelog+= "- 명령어 2개 추가\n"
    changelog+= "- 봇 동작 안정화```"
    return changelog


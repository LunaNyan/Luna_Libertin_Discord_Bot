# 기계식 루냥이 퍼블릭 버전

[봇 입양하기](https://discordapp.com/oauth2/authorize?client_id=598080777565241354&scope=bot&permissions=388190)

[지원 서버](https://discordapp.com/invite/yyS9x5V)

# 서버 구축에 필요한 자원
- 리눅스 탑재 시스템

 권장 : Debian, Ubuntu / x86-64

- 인터넷 연결

- Python 3.5+

 권장 : 3.6, 3.7

- Discord 봇 토큰

- (가능한 경우) Wolfram|Alpha 앱 토큰

# 서버 구축 방법
1. `sudo pip3 install -r requirements.txt`를 실행합니다. 이 명령어는 기계식 루냥이를 동작시키는 데 필요힌 모든 모듈 패키지를 설치합니다.

2. config.ini를 vim, nano 등의 에디터로 실행해 토큰을 입력합니다.

3. `./luna_libertin_prod_public.py & disown`을 입력해 봇을 가동합니다.

# 유용한 팁
- 주기적으로 db.dat를 백업하는 crontab을 만들어 사용하시는 것을 추천드립니다. 제작자가 벌레 잡다 날려먹은 적이 한번 있었습니다.

# 라이센스
이 봇은 MIT License를 사용하고 있으며, 프로그램의 변형 가동 등이 자유롭게 허용되나, 봇을 통해 이루어지는 모든 손해에 대해서는 어떠한 보증도 주어질 수 없습니다.

자세한 사항은 LICENSE 파일을 참조하십시오.

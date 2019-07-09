import psutil
import random

def checkIfProcessRunning(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

def sans():
    sans_str = ["언더테일 아시는구나! 혹시 모르시는분들에 대해 설명해드립니다 샌즈랑 언더테일의 세가지 엔딩루트중 몰살엔딩의 최종보스로 진.짜.겁.나.어.렵.습.니.다 공격은 전부다 회피하고 만피가 92인데 샌즈의 공격은 1초당 60이 다는데다가 독뎀까지 추가로 붙어있습니다.. 하지만 이러면 전대로 게임을 깰 수 가없으니 제작진이 치명적인 약점을 만들었죠. 샌즈의 치명적인 약점이 바로 지친다는것입니다. 패턴들을 다 견디고나면 지쳐서 자신의 턴을 유지한채로 잠에듭니다. 하지만 잠이들었을때 창을옮겨서 공격을 시도하고 샌즈는 1차공격은 피하지만 그 후에 바로날아오는 2차 공격을 맞고 죽습니다.",
                "와!",
                "와 샌즈!",
                "와 파피루스!",
                "와 샌즈! 와 파피루스!"]
    return random.choice(sans_str)

def imcute():
    imcute_str = ["그쵸 루냥이 진짜 너무 귀여워요 ㅠㅜ",
                  "아웅 루냥이 너무 큐트뽀쟉해 지구뿌셔ㅠㅠㅜ",
                  "저 루냥이 꼬리 잡아당겨본 적 있는데 그때 진짜 심장멎을뻔했어요ㅠㅠ:heart_eyes:",
                  "루냥이 쓰다듬다가 좋아하는 표정 보고 심쿵:heart_eyes: 골골송 하는것도 너무 큐트해ㅠㅜ",
                  "아웅 어뜩행 ㅠㅜ 너무 귀여워 ㅠㅜ",
                  "루냥이 너무 귀여워! :heart_eyes:"]
    return random.choice(imcute_str)

def pat():
    pat_str =  [">_<~ :two_hearts:",
                "냐앙~ :heart_eyes: :two_hearts:",
                "하우우..:blush:",
                "하앙~(꼬리펑"]
    return random.choice(pat_str)

def l_ping():
    lp_str = ["우웅? (쫑긋",
              "(꼬리살랑",
              "후아암~(발라당",
              "네에~?(쫑긋",
              "부르셨어요? 헤헤..(꼬리살랑"]
    return random.choice(lp_str)

def ret_help():
    help = "```명령어 목록\n"
    help+= "루냥아 도와줘 : 이 메시지를 표시합니다\n"
    help+= "루냥아 배고파 : 랜덤으로 음식을 추천해줍니다\n"
    help+= "루냥아 섯다 : CPU와 두장섯다를 진행합니다\n"
    help+= "              진행 방법은 1에서 10까지의 숫자 두개를 선택합니다 (예 : 루냥아 섯다 3 5)\n"
    help+= "루냥아 확성기 (할 말) : 기계식 루냥이가 대신 말해줍니다\n"
    help+= "루냥아 계산해줘 (계산식) : Wolfram|Alpha 계산을 수행합니다\n"
    help+= "루냥아 골라줘 (선택1) (선택2) .. : 무작위로 선택지를 골라줍니다"
    help+= "\n\n이외에도 숨겨진 명령어가 몇개 있으니 찾아보세요!\n"
    help+= "\n오류 발생이나 기타 건의사항은 chkong1998@gmail.com으로 문의 바랍니다```"
    return help

def selectr(message):
    m = message
    m = m.replace("_", "")
    m = m.replace("루냥아 골라줘 ", "")
    i = m.split(" ")
    return random.choice(i)

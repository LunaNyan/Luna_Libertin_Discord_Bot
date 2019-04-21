from random import randint

# Input Legend
# 1 : Rock
# 2 : Scissors
# 3 : Paper

# Result Legend
# 0 = draw
# 1 = player win
# 2 = CPU win

result_str = ""

def rps_run(message_content):
    message_sanitize = message_content
    message_sanitize = message_sanitize.replace("_", "")
    message_sanitize = message_sanitize.replace("루냥아 가위바위보 ", "")
    if message_sanitize == "가위":
        inp = 1
    elif message_sanitize == "바위":
        inp = 2
    elif message_sanitize == "보":
        inp = 3
    else:
        inp = randint(1, 3)
    oup = randint(1, 3)
    if inp == oup:
        result = 0
    elif inp == 1 and oup == 2:
        result = 1
    elif inp == 1 and oup == 3:
        result = 2
    elif inp == 2 and oup == 1:
        result = 2
    elif inp == 2 and oup == 3:
        result = 1
    elif inp == 3 and oup == 1:
        result = 1
    elif inp == 3 and oup == 2:
        result = 2
    if oup == 1:
        oup_str = "가위"
    elif oup == 2:
        oup_str = "바위"
    elif oup == 3:
        oup_str = "보"
    if result == 0:
        result_str = "상대방 : " + oup_str + "\n비겼습니다!"
    elif result == 1:
        result_str = "상대방 : " + oup_str + "\n상대방이 졌습니다!"
    elif result == 2:
        result_str = "상대방 : " + oup_str + "\n상대방이 이겼습니다!"
    return result_str

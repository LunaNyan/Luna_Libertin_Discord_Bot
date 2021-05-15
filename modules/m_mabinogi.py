import sys, discord, random
import Crypto.Random as crandom

if __name__=="__main__":
    print("FATAL   : Run this bot from right way.")
    sys.exit(1)

def sujeong(yg_amount, yg_count, yg_factor, lucky): # 회당 야금 채집량, 회당 야금술 횟수, 야금술 성공율, 행운
    ndrop_c = 0 # 일반드랍 횟수
    ldrop_c = 0 # 럭키드랍 횟수
    hdrop_c = 0 # 휴즈드랍 횟수
    ndrop_a = 0 # 일반드랍 수정 개수
    ldrop_a = 0 # 럭키드랍 수정 개수
    hdrop_a = 0 # 휴즈드랍 수정 개수
    yg_suc = 0 # 야금 성공 횟수
    yg_fai = 0 # 야금 실패 횟수
    lucky_real = lucky / 2000
    if lucky_real > 0.25: # 럭키 뜰확률
        lucky_real = 0.25
    huge_real = lucky / 25000 # 휴즈 뜰확률
    if huge_real > 0.08:
        huge_real = 0.08
    for _ in range(yg_count): # 채집 n번
        s = random.randint(0, 100) # 야금술 성골율 스펙트럼
        if s <= yg_factor: # 야금 성공시
            yg_suc += 1
            if random.randint(0, 100) / 100 <= 0.055: # 수정 볼 확률 5.5% (2020년 10월 기준)
                i = random.randint(0, 100) / 100 # 야금술 성공 시 확률 스펙트럼
                if i <= huge_real: # 휴즈
                    hdrop_c += 1
                    hdrop_a += 20
                elif i <= lucky_real: # 럭키
                    ldrop_c += 1
                    ldrop_a += random.randint(1, yg_amount)
                else: # 일반
                    d = random.randint(1, yg_amount)
                    ndrop_c += 1
                    ndrop_a += d
        else: # 야금 실패시
            yg_fai += 1
    return [[ndrop_c, ldrop_c, hdrop_c], [ndrop_a, ldrop_a, hdrop_a], [yg_suc, yg_fai]]

def multi_sujeong(yg_amount, yg_count, yg_factor, lucky, amount): # 회당 야금 채집량, 회당 야금술 횟수, 야금술 성공율, 행운, 수정노기 한 횟수
    cnt = 0 # 회차
    tot = 0 # 총 개수
    tot_ni = 0 # 누적 일반드랍 횟수
    tot_li = 0 # 누적 럭키드랍 횟수
    tot_hi = 0 # 누적 휴즈드랍 횟수
    tot_na = 0 # 누적 일반드랍 개수
    tot_la = 0 # 누적 럭키드랍 개수
    tot_ha = 0 # 누적 휴즈드랍 개수
    amounts = yg_count * amount # 야금술을 한 최종 횟수
    lucky_real = lucky / 2000
    if lucky_real > 0.25: # 럭키 뜰확률
        lucky_real = 0.25
    huge_real = lucky / 25000 # 휴즈 뜰확률
    if huge_real > 0.08:
        huge_real = 0.08
    ps = "== 수정노기 결과 =="
    ps+= "\r\n주의 : 해당 결과는 시뮬레이션 결과로, 실제 상황 대비 정확하지 않을 수 있습니다."
    ps+= "\r\n야금술 채집량 : " + str(yg_amount) + "\r\n회차당 야금술 횟수 : " + str(yg_count) + "\r\n야금술 성공율 : " + str(yg_factor) + "%\r\n행운 : " + str(lucky) + "\r\n수정노기 한 횟수 : " + str(amount)
    ps+= "\r\n\r\n럭키 뜰 확률 : " + str(lucky_real * 100) + "%\r\n휴즈 뜰 확률 : " + str(huge_real * 100) + "%"
    ps+= "\r\n==================="
    for _ in range(amount):
        cnt += 1
        res = sujeong(yg_amount, yg_count, yg_factor, lucky)
        totl = res[1][0] + res[1][1] + res[1][2]
        tot += totl
        tot_ni += res[0][0]
        tot_li += res[0][1]
        tot_hi += res[0][2]
        tot_na += res[1][0]
        tot_la += res[1][1]
        tot_ha += res[1][2]
        ps += "\r\n- " + str(cnt) + "회차"
        ps += "\r\n  일반드랍 횟수 : " + str(res[0][0]) + ", 수정 " + str(res[1][0]) + "개"
        ps += "\r\n  럭키드랍 횟수 : " + str(res[0][1]) + ", 수정 " + str(res[1][1]) + "개"
        ps += "\r\n  휴즈드랍 횟수 : " + str(res[0][2]) + ", 수정 " + str(res[1][2]) + "개"
        ps += "\r\n  야금술 성공 : " + str(res[2][0]) + "회, 실패 " + str(res[2][1]) + "회"
        ps += "\r\n  얻은 수정 개수 : " + str(totl) + "개"
        ps += "\r\n"
    ps += "==================="
    ps += "\r\n야금술을 총 " + str(amounts) + "회 했습니다."
    ps += "\r\n총 일반드랍 : " + str(tot_ni) + "회 (수정 " + str(tot_na) + "개)"
    ps += "\r\n총 럭키드랍 : " + str(tot_li) + "회 (수정 " + str(tot_la) + "개)"
    ps += "\r\n총 휴즈드랍 : " + str(tot_hi) + "회 (수정 " + str(tot_ha) + "개)"
    ps += "\r\n\r\n최종적으로 얻은 수정 개수 : " + str(tot)
    pf = open("sujeong.txt", "w")
    pf.write(ps)
    pf.close()
    ps = "" # 메모리 단편화 방지
    # 임베드 제목이 수정노기 횟수 * 야금술 횟수에 따라 바뀜
    if amounts >= 800000:
        tit = "저기.. 그냥 재미로만 하시는거죠?"
    elif amounts >= 500000:
        tit = "저기.. 괜찮으신가요? 사람 맞죠?"
    elif amounts >= 300000:
        tit = "저기.. 현생은 잘 살아있나요?"
    elif amounts >= 150000:
        tit = "진심으로 뇌를 수정노기에 업로드하셨군요!"
    elif amounts >= 100000:
        tit = "밥만 먹고 수정을 하셨군요!"
    elif amounts >= 70000:
        tit = "하루종일 수정을 하셨군요!"
    elif amounts <= 69999:
        tit = "수정노기를 끝냈어요!"
    # Discord 임베드 생성
    embed=discord.Embed(title=tit)
    embed.add_field(name="일반드랍", value="횟수 : " + str(tot_ni) + ", 개수 : " + str(tot_na))
    embed.add_field(name="럭키드랍", value="횟수 : " + str(tot_li) + ", 개수 : " + str(tot_la))
    embed.add_field(name="휴즈드랍", value="횟수 : " + str(tot_hi) + ", 개수 : " + str(tot_ha))
    embed.add_field(name="총 획득량", value=str(tot) + "개")
    embed.set_footer(text="자세한 결과는 첨부된 텍스트 파일을 참조해주세요!")
    return embed

def settings(db, message, head):
    try:
        m = message.content.replace(head + "수정노기 설정 ", "")
        ml = m.split(" ")
        if len(ml) != 4:
            raise # 덜 or 더 입력된 파라미터
        if int(ml[0]) < 1 or int(ml[0]) > 6 or int(ml[1]) < 1 or int(ml[1]) > 1000 or int(ml[2]) < 0 or int(ml[2]) > 100 or int(ml[3]) < 0 or int(ml[3]) > 2000:
            raise # 잘못된 파라미터 or 파라미터가 숫자가 아님
        db.set("mabinogi_sujeong", str(message.author.id), m)
        embed=discord.Embed(title="성공적으로 설정되었어요!")
    except:
        embed=discord.Embed(title="사용 방법 : 루냥아 수정노기 설정 (야금술 채집량 1 ~ 6) (회당 야금술 횟수 1 ~ 1000) (야금술 성공율 0 ~ 100) (행운 0 ~ 2000)")
        embed.add_field(name="야금술 채집량", value="본인이 야금술 1랭일시 기본 3개\n채집2 야금채 사용시 +2 = 5개\n채집3 야금채 사용시 +3 = 6개")
        embed.add_field(name="야금술 성공율", value="메이킹 1랭 15% + 야금술 1랭 50% + 풍년가 5% = 기본 성공율 70%\n벨몬셋 10% 야금성공 1랩당 1.25% 추가")
        embed.set_footer(text="참고자료 : https://m.blog.naver.com/wowo367/220938750583")
    return embed

def do_sujeong(db, message, head):
    # 설정을 불러옴
    try:
        ss = db.get("mabinogi_sujeong", str(message.author.id))
        sl = ss.split(" ")
    except:
        embed=discord.Embed(title="설정을 먼저 해주세요", description="도움말 : 루냥아 수정노기 설정")
        return [embed, False]
    # 수정노기 개수 파싱
    m = message.content.replace(head + "수정노기 ", "")
    try:
        mx = int(m)
    except: # 횟수가 숫자가 아닌 경우
        embed=discord.Embed(title="사용 방법 : 루냥아 수정노기 (횟수)")
        return [embed, False]
    if mx < 1 or mx > 1000: # 횟수가 1 ~ 1000이 아닌 경우
        embed=discord.Embed(title="횟수는 1부터 1000까지 가능합니다")
        return [embed, False]
    # 가져온 설정 데이터로 수정노기 개시
    re = multi_sujeong(int(sl[0]), int(sl[1]), int(sl[2]), int(sl[3]), mx)
    return [re, True]
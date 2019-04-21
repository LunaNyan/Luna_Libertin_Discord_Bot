import datetime
from datetime import date
import time

def return_lifetime(precense):
    if precense == "":
        now = datetime.datetime.now()
        lw_h = now.hour
        lw_w = date.isoweekday(date.today())
        if lw_w == 1: #월요일
            if lw_h >= 3 and lw_h <= 10:
                return_string = "자고있음"
            elif lw_h >= 13 and lw_h <= 17:
                return_string = "무인항공기운영실습 강의시간임"
            elif lw_h >= 18 and lw_h <= 20:
                return_string = "근무중임 방해ㄴㄴ"
            else:
                return_string = "한가하거나 이지투하고있거나 둘중하나임"
        elif lw_w == 2: #화요일
            if lw_h >= 2 and lw_h <= 7:
                return_string = "자고있음"
            elif lw_h >= 9 and lw_h <= 12:
                return_string = "항공전기전자 강의시간임"
            elif lw_h == 13:
                return_string = "학식먹는중"
            else:
                return_string = "한가함 어쨌든 한가함"
        elif lw_w == 3: #수요일
            if lw_h >= 3 and lw_h <= 11:
                return_string = "자고있음"
            elif lw_h >= 14 and lw_h <= 16:
                return_string = "항공역학 강의시간임"
            elif lw_h == 17 or lw_h == 18:
                return_string = "근무중임 방해ㄴㄴ"
            else:
                return_string = "지금 얘기하면 받아줄거같음"
        elif lw_w == 4: #목요일
            if lw_h >= 2 and lw_h <= 11:
                return_string = "자고있음"
            else:
                return_string = "우주공강임 개꿀"
        elif lw_w == 5: #금요일
            if lw_h >= 2 and lw_h <= 10:
                return_string = "자고있음"
            elif lw_h >= 11 and lw_h <= 14:
                return_string = "항공기상 강의시간임"
            elif lw_h == 16 and lw_h == 17:
                return_string = "근무시간임 방해ㄴㄴ"
            else:
                return_string = "존나즐거움 메챠쿠챠 타노시쟝"
        else: #주말
            return_string = "니가 물어보셈"
        return return_string
    else:
        return precense

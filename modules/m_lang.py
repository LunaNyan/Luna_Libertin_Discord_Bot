import sys, configparser

if __name__=="__main__":
    print("FATAL   : Run this bot from right way.")
    sys.exit(1)

kr_def = configparser.ConfigParser()
kr_ban = configparser.ConfigParser()
en_def = configparser.ConfigParser()

kr_def.read("lang/kr_default.lld")
kr_ban.read("lang/kr_lower.lld")
en_def.read("lang/en_default.lld")

def string(db, id, call):
    try:
        l = db.get("lang", str(id))
    except:
        l = "default"
    s = ""
    if l == "default":
        try:
            s = kr_def.get("string", call)
            s = s.replace("&nbsp", "\n")
        except:
            s = "내부 시스템 오류 : 언어 " + l + "에서 스트링 " + call + "을 찾을 수 없습니다"
    elif l == "ban":
        try:
            s = kr_ban.get("string", call)
            s = s.replace("&nbsp", "\n")
        except:
            s = "내부 시스템 오류 : 언어 " + l + "에서 스트링 " + call + "을 찾을 수 없습니다"
    elif l == "en":
        try:
            s = en_def.get("string", call)
            s = s.replace("&nbsp", "\n")
        except:
            s = "내부 시스템 오류 : 언어 " + l + "에서 스트링 " + call + "을 찾을 수 없습니다"
    return s

def check_lang(db, id):
    try:
        l = db.get("lang", str(id))
    except:
        l = "default"
    if l == "default":
        return "한국어(기본)"
    elif l == "ban":
        return "한국어(반말모드)"
    elif l == "en":
        return "English(Development Only)"

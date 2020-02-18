import psutil, base64, os, sys, hashlib
from PIL import Image, ImageDraw, ImageFont
import configparser

db_path = "db/username_db.dat"

db = configparser.ConfigParser()
db.read(db_path)

def getHash(path, blocksize=65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

def base64e(s):
    e = base64.b64encode(s.encode('utf-8'))
    e = str(e).replace("b'", "")
    e = e.replace("'", "")
    return e

def base64d(b):
    return str(base64.b64decode(b).decode('utf-8'))

def checkIfProcessRunning(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

def checkTrait(text):
    c = text[-1:]
    if int((ord(c) - 0xAC00) % 28) != 0:
        return "을"
    else:
        return "를"

def outline_draw(d, text, x, y, rb=0, gb=0, bb=0, rf=255, gf=255, bf=255):
    d.text((x-1, y), text, fill=(rb, gb, bb))
    d.text((x+1, y), text, fill=(rb, gb, bb))
    d.text((x, y-1), text, fill=(rb, gb, bb))
    d.text((x, y+1), text, fill=(rb, gb, bb))
    d.text((x-1, y-1), text, fill=(rb, gb, bb))
    d.text((x+1, y-1), text, fill=(rb, gb, bb))
    d.text((x-1, y-1), text, fill=(rb, gb, bb))
    d.text((x+1, y+1), text, fill=(rb, gb, bb))
    d.text((x, y), text, fill=(rf, gf, bf))

def make_color(text, head):
    m = text.replace(head + "색상 ", "")
    m = m.upper()
    ms = "color hex #" + m
    h = tuple(int(m[i:i+2], 16) for i in (0, 2, 4))
    img = Image.new('RGB', (200, 120), color = h)
    d = ImageDraw.Draw(img)
    outline_draw(d, ms, 10, 10)
    outline_draw(d, "red   : " + str(h[0]) + "(" + str(int((h[0] / 255) * 100)) + "%)", 10, 24, 255, 0, 0)
    outline_draw(d, "green : " + str(h[1]) + "(" + str(int((h[1] / 255) * 100)) + "%)", 10, 38, 0, 255, 0)
    outline_draw(d, "blue  : " + str(h[2]) + "(" + str(int((h[2] / 255) * 100)) + "%)", 10, 52, 0, 0, 255)
    d.text((10, 66), "white text", fill=(255, 255, 255))
    d.text((10, 80), "black text", fill=(0, 0, 0))
    img.save('pil_color.png')
    return "pil_color.png"

def make_pil(text, head):
    m = text.replace(head + "받아쓰기 ", "")
    m = m.encode('utf-8')
    font = ImageFont.truetype("font/kopub.ttf", 20, encoding='unic')
    img = Image.new('RGB', (320, 240), color = (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((10, 10), m.decode('utf-8'), fill=(0, 0, 0), font=font)
    img.save('pil_color.png')
    return "pil_color.png"

def get_name(id):
    try:
        n = db.get("name", str(id))
        return n
    except:
        return None

def set_name(message):
    db.set("name", str(message.author.id), str(message.author.name))
    with open(db_path, 'w') as configfile:
        db.write(configfile)
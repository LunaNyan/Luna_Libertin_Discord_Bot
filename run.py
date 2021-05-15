#!/usr/bin/python3
bootstrapper_ver = "1.41"

import sys, os, os.path, configparser, fcntl, hashlib, shutil
from datetime import datetime

pid_file = 'lunabot.lock'
fp = open(pid_file, 'w')

try:
    fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
    print("FATAL   : Another bot isntance is running!")
    print("          Terminate another bot and try again.")
    sys.exit(1)

print("System Bootstrapper, ver " + bootstrapper_ver)

def bootup():
    while True:
        try:
            import main
        except Exception as e:
            if(str(e)) == "rebootme":
                continue
            else:
                print(traceback.format_exc())
                break

def getHash(path, blocksize=65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

def check_parts():
    # 시스템 정보 확인
    print("Checking system.")
    if sys.platform != "linux":
        print("FATAL   : This application is ONLY for Linux. NOT for Windows or other.")
        sys.exit(1)
    else:
        print("Success.")
    
    if sys.version_info[0] != 3 or sys.version_info[1] < 6:
        print("FATAL   : This script requires Python version 3.6")
        sys.exit(1)
    
    # 모듈 검사
    print("Checking required modules.")
    try:
        import asyncio, discord, requests, xmltodict, wolframalpha, cpuinfo, PIL
        print("Success.")
    except Exception as e:
        print(str(e))
        print("Some required module(s) is not found. Trying to installing it. Please wait.")
        os.system("python3 -m pip install -r ./requirements.txt")
    
    # MD5 확인, 변경 있을경우 즉시 백업
    print("application auto backup secuence initialized")
    dt = datetime.now()
    dt = str(int(dt.timestamp()))
    md5_store = configparser.ConfigParser()
    md5_store.read("../backups/app/hash.dat")
    md5_list = os.listdir("./modules/")
    for ff in md5_list:
        if ff == "__pycache__" or ff == ".ipynb_checkpoints":
            continue
        try:
            hash_origin = md5_store.get("hash", ff)
        except:
            hash_origin = ""
        hash_target = getHash("./modules/" + ff)
        if hash_origin != hash_target:
            dtdir = "../backups/app/" + dt
            if not os.path.isdir(dtdir):
                os.mkdir(dtdir)
            shutil.copy2("./modules/" + ff, dtdir + "/" + ff)
            print(ff + " : " + hash_target + ", changes detected")
            print("origin MD5 : " + hash_origin + ", backuping to " + dt)
            md5_store.set("hash", ff, hash_target)
        else:
            print(ff + " : " + hash_target + ", no changes detected")
    with open("../backups/app/hash.dat", 'w') as configfile:
        md5_store.write(configfile)
    
    # 설정파일 검사
    print("Reading configuration file.")
    if not os.path.isfile("config.ini"):
        print("FATAL   : No configuration file found.")
        sys.exit(1)
    else:
        check_conf = configparser.ConfigParser()
        check_conf.read("config.ini")
        print("Checking configuration file.")
        if check_conf.get("config", "bot_token") == "":
            print("FATAL   : No bot token found. Make your bot application and fetch token from https://discordapp.com/developers/applications/")
            sys.exit(1)
        elif check_conf.get("config", "bot_owner") == "":
            print("FATAL   : Administrator account ID is not provided.")
            sys.exit(1)
        elif check_conf.get("wolframalpha", "appid") == "":
            print("WARN   : No Wolfram|Alpha App ID found. this means users cannot use Wolfram|Alpha related functions.")
        else:
            print("Configuration file check success.")
    
    print("Loading Bot application. Please Wait..")
    sys.path.append('./modules/')
    
    bootup()

check_parts()
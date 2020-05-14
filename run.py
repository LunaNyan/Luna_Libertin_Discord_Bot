#!/usr/bin/python3

bootstrapper_ver = "1.00"

print("System Bootstrapper, ver " + bootstrapper_ver)

import sys, os, os.path, configparser

# 시스템 정보 확인
print("Checking system.")
if sys.platform != "linux":
    print("FATAL : This application is ONLY for Linux. NOT for Windows or other.")
    sys.exit(1)
else:
    print("Success.")

# 모듈 검사
print("Checking required modules.")
try:
    import asyncio, discord, requests, xmltodict, wolframalpha, cpuinfo, PIL
    print("Success.")
except Exception as e:
    print(str(e))
    print("Some required module(s) is not found. Trying to installing it. Please wait.")
    os.system("python3 -m pip install -r ./requirements.txt")

# 설정파일 검사
print("Reading configuration file.")
if not os.path.isfile("config.ini"):
    print("FATAL : No configuration file found.")
    sys.exit(1)
else:
    check_conf = configparser.ConfigParser()
    check_conf.read("config.ini")
    print("Checking configuration file.")
    if check_conf.get("config", "bot_token") == "":
        print("FATAL : No bot token found. Make your bot application and fetch token from https://discordapp.com/developers/applications/")
        sys.exit(1)
    elif check_conf.get("config", "bot_owner") == "":
        print("FATAL : Administrator account ID is not provided.")
        sys.exit(1)
    elif check_conf.get("wolframalpha", "appid") == "":
        print("WARN : No Wolfram|Alpha App ID found. this means users cannot use Wolfram|Alpha related functions.")
    else:
        print("Configuration file check success.")

print("Loading Bot application. Please Wait..")
sys.path.append('./modules/')
try:
    import main
except Exception as e:
    if(str(e)) == "rebootme":
        import main
    else:
        print(str(e))
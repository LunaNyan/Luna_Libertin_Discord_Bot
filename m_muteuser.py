import configparser

conf = configparser.ConfigParser()
conf.read("luna_config.txt")

def mute_user(id):
    try:
        if conf.get("user_mute", str(id)) == "1":
            return "this user is already muted"
        else:
            conf.set("user_mute", str(id), "1")
            return "user muted"
    except:
        conf.set("user_mute", str(id), "1")
        return "user muted"
    with open("luna_config.txt", 'w') as configfile:
        conf.write(configfile)

def unmute_user(id):
    try:
        if conf.get("user_mute", str(id)) == "0":
            return "this user is not muted"
        else:
            conf.set("user_mute", str(id), "0")
            return "user unmuted"
    except:
        conf.set("user_mute", str(id), "0")
        return "this user is not muted"
    with open("luna_config.txt", 'w') as configfile:
        conf.write(configfile)

def check_muted(id):
    try:
        if conf.get("user_mute", str(id)) == "1":
            return True
        else:
            return False
    except:
        conf.set("user_mute", str(id), "0")
        return False
    with open("luna_config.txt", 'w') as configfile:
        conf.write(configfile)

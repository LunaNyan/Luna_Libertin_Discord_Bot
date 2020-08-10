import random

prev_code = ""

def generate_code(guild, conf):
    global prev_code
    a = conf.items("server_code")
    b = []
    c = []
    for ai in a:
        b.append(ai[0])
        c.append(ai[1])
    if str(guild.id) in b:
        prev_code = c[b.index(str(guild.id))]
        return False
    else:
        while True:
            #generating raw code
            code = ""
            lb = 5
            while lb > 0:
                while True:
                    ch = chr(random.randint(ord('A'), ord('Z')))
                    if ch == "I" or ch == "O":
                        continue
                    else:
                        code += ch
                        break
                lb -= 1
            code += "-"
            code = code[:-1]
            if code in b:
                continue
            else:
                break
    conf.set("server_code", str(guild.id), code)
    return code

def get_code(guild, db):
    code = db.get("server_code", str(guild.id))
    return code
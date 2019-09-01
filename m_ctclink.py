import random

def generate_code(channel, conf):
    a = conf.items("ctclink")
    b = []
    c = []
    for ai in a:
        b.append(ai[1].replace("pending_", ""))
        c.append(ai[0])
    if str(channel) in c:
        raise
    else:
        while True:
            #generating raw code
            code = ""
            la = 2
            while la > 0:
                lb = 3
                while lb > 0:
                    code += chr(random.randint(ord('A'), ord('Z')))
                    lb -= 1
                code += "-"
                la -= 1
            code = code[:-1]
            if code in b:
                continue
            else:
                break
    conf.set("ctclink", str(channel), "pending_" + code)
    return code

def get_channel_code(channel, code, conf):
    a = conf.items("ctclink")
    b = []
    c = []
    for s in a:
        b.append(s[0])
        c.append(s[1].replace("pending_", ""))
    if code in c:
        ci = c.index(code)
        conf.set("ctclink", b[ci], str(channel))
        return b[ci]
    else:
        return False

def get_link(channel, conf):
    a = conf.items("ctclink")
    b = []
    c = []
    for s in a:
        b.append(s[0])
        c.append(s[1])
    if str(channel) in b:
        ci = b.index(str(channel))
        return c[ci]
    elif str(channel) in c:
        bi = c.index(str(channel))
        return b[bi]
    else:
        return False

def remove_link(channel, conf):
    a = conf.items("ctclink")
    b = []
    c = []
    for s in a:
        b.append(s[0])
        c.append(s[1])
    if str(channel) in b:
        conf.remove_option("ctclink", str(channel))
        return True
    elif str(channel) in c:
        bi = c.index(str(channel))
        conf.remove_option("ctclink", b[bi])
        return True
    else:
        return False

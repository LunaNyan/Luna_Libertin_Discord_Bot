import random

prev_code = ""

def generate_code(channel, conf):
    global prev_code
    a = conf.items("ctclink_pending")
    b = []
    c = []
    for ai in a:
        b.append(ai[0])
        c.append(ai[1])
    if str(channel) in b:
        prev_code = c[b.index(str(channel))]
        return False
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
    conf.set("ctclink_pending", str(channel), code)
    return code

def get_channel_code(channel, code, conf):
    a = conf.items("ctclink_pending")
    b = []
    c = []
    for s in a:
        b.append(s[0])
        c.append(s[1])
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
    d = conf.items("ctclink_pending")
    e = []
    for t in d:
        e.append(t[0])
    if str(channel) in b:
        conf.remove_option("ctclink", str(channel))
        conf.remove_option("ctclink_pending", str(channel))
        return True
    elif str(channel) in c:
        bi = c.index(str(channel))
        conf.remove_option("ctclink", b[bi])
        conf.remove_option("ctclink_pending", b[bi])
        return True
    else:
        return False

def remove_pending(channel, conf):
    a = conf.items("ctclink_pending")
    b = []
    for ai in a:
        b.append(ai[0])
    if str(channel) in b:
        conf.remove_option("ctclink_pending", str(channel))
        return True
    else:
        return False
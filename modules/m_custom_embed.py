import sys, random, discord, m_etc, math, m_lang

if __name__=="__main__":
    print("FATAL   : Run this bot from right way.")
    sys.exit(1)

def get_embed_raw(message, db, code):
    # set code as None to use NVRAM
    try:
        if code == None:
            l = db.get("custom_embed_nvram", str(message.author.id))
        else:
            l = db.get("custom_embed", code)
        l = l.split(",")
        lx = []
        for i in l:
            lx.append(m_etc.base64d(i))
        return lx
    except:
        return ["", "", str(message.author.id)]

def commit_embed(message, db, container, nvram):
    container_t = ""
    try:
        test = container[2]
    except:
        container[2] = str(message.author.id)
    for i in container:
        container_t += m_etc.base64e(i) + ","
    if nvram:
        db.set("custom_embed_nvram", str(message.author.id), container_t[:-1])
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
            try:
                db.get("custom_embed", str(message.author.id) + "_" + code)
                continue
            except:
                break
        db.set("custom_embed", str(message.author.id) + "_" + code, container_t)
        return code

def convert_to_embed(message, container):
    if len(container) % 2 == 0:
        container_v = container[:-1]
    else:
        container_v = container
    ti = container_v[0]
    if " && " in ti:
        ti = ti.split(" && ")
        ti = random.choice(ti)
    ti.replace("[이름]", message.author.name)
    de = container_v[1]
    if " && " in de:
        de = de.split(" && ")
        de = random.choice(de)
    de.replace("[이름]", message.author.name)
    de.replace("[멘션]", message.author.mention)
    if container_v[1] == "":
        embed=discord.Embed(title=ti)
    else:
        embed=discord.Embed(title=ti, description=de)
    embed.set_footer(text="작성자 : " + m_etc.get_name(container_v[2]))
    del container_v[2]
    del container_v[1]
    del container_v[0]
    cnt = 0
    while True:
        try:
            na = container_v[cnt]
            if " && " in na:
                na = na.split(" && ")
                na = random.choice(na)
            il = container_v[cnt+1]
            if " && " in il:
                il = il.split(" && ")
                il = random.choice(il)
            il.replace("[이름]", message.author.name)
            il.replace("[멘션]", message.author.mention)
            embed.add_field(name=na, value=il, inline=False)
            cnt += 2
        except Exception as e:
            break
    return embed

def list_embeds(message, head, db):
    try:
        m = message.content.replace(head + "임베드 목록 ", "")
        page = int(m)
    except:
        page = 1
    l = db.items("custom_embed")
    n = 0
    lx = []
    cx = []
    for i in l:
        if i[0].startswith(str(message.author.id)):
            code = i[0].replace(str(message.author.id) + "_", "")
            cx.append(code)
            lx.append(i[1])
            n += 1
    pages = math.ceil(n / 10)
    if page > pages:
        embed=discord.Embed(title=m_lang.string(db, message.author.id, "wrong_page_idx"))
    else:
        c = (page - 1) * 10
        ct = c + 9
        embed=discord.Embed(title="커스텀 임베드 목록 (총 " + str(n) + "개)", color=0xffffff)
        while c <= ct:
            try:
                title = lx[c].split(",")
                title = title[0]
                title = m_etc.base64d(title)
                try:
                    desc = title[1]
                    desc = m_etc.base64d(desc)
                except:
                    desc = "개요 없음"
                embed.add_field(name=cx[c].upper() + " : " + title, value=desc, inline=False)
                c += 1
            except Exception as e:
                break
        embed.set_footer(text=str(page) + ' / ' + str(pages) + ' 페이지, 다른 페이지 보기 : "루냥아 임베드 목록 (페이지)"')
    return embed

def set_title(message, head, db):
    l = get_embed_raw(message, db, None)
    m = message.content.replace(head + "임베드 제목 ", "")
    l[0] = m
    commit_embed(message, db, l, True)

def set_desc(message, head, db):
    l = get_embed_raw(message, db, None)
    m = message.content.replace(head + "임베드 개요 ", "")
    l[1] = m
    commit_embed(message, db, l, True)

def add_content(message, head, db):
    l = get_embed_raw(message, db, None)
    lx = l[:3]
    try:
        ly = l[3:]
    except:
        ly = []
    m = message.content.replace(head + "임베드 내용추가 ", "")
    m = m.split(" | ")
    ly.append(m[0])
    ly.append(m[1])
    commit_embed(message, db, lx + ly, True)

def purge_nvram(message, db):
    db.remove_option("custom_embed_nvram", str(message.author.id))
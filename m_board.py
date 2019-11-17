import configparser, discord, math, datetime, m_etc, m_lang

memo_temp_title = "66mU66qoIOyCrOyaqSDrsKnrspU="
memo_temp_content = "IuujqOuDpeyVhCDrqZTrqqggKOuCtOyaqSkiIDog66mU66qoIOyekeyEse2VmOq4sAoi66Oo64Ol7JWEIOuplOuqqCDrqqnroZ0gKO2OmOydtOyngCkiIDog66mU66qoIOuqqeuhnSDrs7TquLAKIuujqOuDpeyVhCDrqZTrqqgg7IKt7KCcICjrsojtmLgpIiA6IOuqqeuhnSDrsojtmLjsl5Ag7ZW064u57ZWY64qUIOuplOuqqCDsgq3soJw="

db_path = "board_db.dat"

db = configparser.ConfigParser()
db.read(db_path)

def read(no, db, id):
    if no < 1 or no > 10:
        embed=discord.Embed(title=m_lang.string(db, id, "undefined_article_num_title"), description = m_lang.string(db, id, "notice_wrong_idx_desc"), color=0xffff00)
    else:
        article_title = db.get("article_" + str(no), "title")
        article_content = db.get("article_" + str(no), "content")
        article_dt = db.get("article_" + str(no), "datetime")
        if article_title == "empty":
            embed=discord.Embed(title=m_lang.string(db, id, "undefined_article_num_title"), description = m_lang.string(db, id, "notice_wrong_idx_desc"), color=0xffff00)
        else:
            embed=discord.Embed(title="#" + str(no) + " : " + article_title, description=article_content, color=0xffffff)
            embed.set_footer(text="작성일자 : " + article_dt)
    return embed

def write(title, content):
    # shifting article list
    # this function will delete oldest article in the list
    shift_i = 9
    while shift_i >= 1:
        db.set("article_" + str(shift_i + 1), "title", db.get("article_" + str(shift_i), "title"))
        db.set("article_" + str(shift_i + 1), "content", db.get("article_" + str(shift_i), "content"))
        db.set("article_" + str(shift_i + 1), "datetime", db.get("article_" + str(shift_i), "datetime"))
        shift_i -= 1
    db.set("article_1", "title", title)
    db.set("article_1", "content", content)
    db.set("article_1", "datetime", str(datetime.datetime.now().isoformat()))
    with open(db_path, 'w') as configfile:
        db.write(configfile)

def amend(no, title, content):
    db.set("article_" + no, "title", title)
    db.set("article_" + no, "content", content)
    db.set("article_" + no, "datetime", str(datetime.datetime.now().isoformat()))
    with open(db_path, 'w') as configfile:
        db.write(configfile)

def list():
    embed = discord.Embed(title="공지사항 목록", color=0xffffff)
    i = 1
    while i <= 10:
        title = db.get("article_" + str(i), "title")
        dtstr = db.get("article_" + str(i), "datetime")
        if title != "empty":
            embed.add_field(name = "#" + str(i) + " : " + title, value="작성일자 : " + dtstr, inline=False)
        i += 1
    return embed

def clear():
    i = 1
    while i <= 10:
        db.set("article_" + str(i), "title", "empty")
        db.set("article_" + str(i), "content", "empty")
        db.set("article_" + str(i), "datetime", "empty")
        i += 1

def gbook_view(page, db, id):
    try:
        content = str(db.get("gbook", "content")).split(", ")
        author = str(db.get("gbook", "author")).split(", ")
        dtstr = str(db.get("gbook", "datetime")).split(", ")
    except:
        l_content = [str(db.get("gbook", "content"))]
        l_author = [str(db.get("gbook", "author"))]
        l_dtstr = [str(db.get("gbook", "datetime"))]
    pages = math.ceil(len(content) / 10)
    if page > pages or page <= 0:
        embed=discord.Embed(title=m_lang.string(db, id, "wrong_page_idx"))
    else:
        embed = discord.Embed(title="방명록", color=0xffffff)
        c = (page - 1) * 10
        ct = c + 9
        while c <= ct:
            try:
                try:
                    nn = m_etc.base64d(author[c])
                    nm = int(nn)
                    nm = m_etc.get_name(nm)
                except:
                    nm = nn
                embed.add_field(name = "#" + str(c+1) + " : " + m_etc.base64d(content[c]), value = "작성자 : " + nm + ", 작성 일자 : " + m_etc.base64d(dtstr[c]), inline=False)
                c += 1
            except:
                break
        embed.set_footer(text=str(page) + ' / ' + str(pages) + ' 페이지, 다른 페이지 보기 : "루냥아 방명록 (페이지)"')
    return embed

def gbook_write(content, author):
    try:
        l_content = str(db.get("gbook", "content")).split(", ")
        l_author = str(db.get("gbook", "author")).split(", ")
        l_dtstr = str(db.get("gbook", "datetime")).split(", ")
    except:
        l_content = [str(db.get("gbook", "content"))]
        l_author = [str(db.get("gbook", "author"))]
        l_dtstr = [str(db.get("gbook", "datetime"))]
    if len(l_content) == 100:
        del l_content[99]
        del l_author[99]
        del l_dtstr[99]
    l_content.insert(0, m_etc.base64e(content))
    l_author.insert(0, m_etc.base64e(str(author)))
    l_dtstr.insert(0, m_etc.base64e(str(datetime.datetime.now().isoformat())))
    n = 0
    s_content = ""
    s_author = ""
    s_dtstr = ""
    for c in l_content:
        s_content += c + ", "
        s_author += l_author[n] + ", "
        s_dtstr += l_dtstr[n] + ", "
        n += 1
    db.set("gbook", "content", s_content[:-2])
    db.set("gbook", "author", s_author[:-2])
    db.set("gbook", "datetime", s_dtstr[:-2])
    with open(db_path, 'w') as configfile:
        db.write(configfile)

def memo_view(message, head, db):
    try:
        content = message.content.replace(head + "메모 목록 ", "")
        page = int(content)
    except:
        page = 1
    try:
        content = str(db.get("memo_" + str(message.author.id), "content")).split(", ")
        dtstr = str(db.get("memo_" + str(message.author.id), "datetime")).split(", ")
    except:
        db.add_section("memo_"+ str(message.author.id))
        l_content = [memo_temp_title]
        l_dtstr = [memo_temp_content]
    pages = math.ceil(len(content) / 10)
    if page > pages or page <= 0:
        embed=discord.Embed(title=m_lang.string(db, message.author.id, "wrong_page_idx"))
    else:
        embed = discord.Embed(title=message.author.name + " 님의 메모 목록 (총 " + str(len(content)) + "개)", color=0xffffff)
        c = (page - 1) * 10
        ct = c + 9
        while c <= ct:
            try:
                embed.add_field(name = "#" + str(c+1) + " : " + m_etc.base64d(content[c]), value ="작성 일자 : " + m_etc.base64d(dtstr[c]), inline=False)
                c += 1
            except:
                break
        embed.set_footer(text=str(page) + ' / ' + str(pages) + ' 페이지, 다른 페이지 보기 : "루냥아 메모 목록 (페이지)"')
    return embed

def memo_write(message, head, db):
    content = message.content.replace(head + "메모 ", "")
    try:
        l_content = str(db.get("memo_"+ str(message.author.id), "content")).split(", ")
        l_dtstr = str(db.get("memo_"+ str(message.author.id), "datetime")).split(", ")
    except:
        db.add_section("memo_"+ str(message.author.id))
        l_content = [memo_temp_title]
        l_dtstr = [memo_temp_content]
    if len(l_content) == 30:
        embed=discord.Embed(title=m_lang.string(db, message.author.id, "memo_amount_exceeded"), description=m_lang.string(db, message.author.id, "delete_obsolete_memo"), color=0xff0000)
    else:
        l_content.insert(0, m_etc.base64e(content))
        l_dtstr.insert(0, m_etc.base64e(str(datetime.datetime.now().isoformat())))
        n = 0
        s_content = ""
        s_dtstr = ""
        for c in l_content:
            s_content += c + ", "
            s_dtstr += l_dtstr[n] + ", "
            n += 1
        db.set("memo_"+ str(message.author.id), "content", s_content[:-2])
        db.set("memo_"+ str(message.author.id), "datetime", s_dtstr[:-2])
        embed=discord.Embed(title=m_lang.string(db, message.author.id, "saved_memo"), description=m_lang.string(db, message.author.id, "saved_memo_desc"), color=0xffff00)
        with open(db_path, 'w') as configfile:
            db.write(configfile)
    return embed

def memo_remove(message, head, db):
    try:
        content = message.content.replace(head + "메모 삭제 ", "")
        num = int(content) - 1
    except:
        embed=discord.Embed(title=m_lang.string(db, message.author.id, "wrong_idx"), content=0xff0000)
        return embed
    try:
        content = str(db.get("memo_" + str(message.author.id), "content")).split(", ")
        dtstr = str(db.get("memo_" + str(message.author.id), "datetime")).split(", ")
    except:
        embed=discord.Embed(title=m_lang.string(db, message.author.id, "no_memo_wrote"), description='메모 작성 방법 : "루냥아 메모 (내용)"', content=0xff0000)
        return embed
    try:
        del content[num]
        del dtstr[num]
    except:
        embed=discord.Embed(title=m_lang.string(db, message.author.id, "wrong_idx"), content=0xff0000)
        return embed
    n = 0
    s_content = ""
    s_dtstr = ""
    for c in content:
        s_content += c + ", "
        s_dtstr += dtstr[n] + ", "
        n += 1
    db.set("memo_"+ str(message.author.id), "content", s_content[:-2])
    db.set("memo_"+ str(message.author.id), "datetime", s_dtstr[:-2])
    embed=discord.Embed(title=_lang.string(db, message.author.id, "memo_deleted"), color=0xffff00)
    with open(db_path, 'w') as configfile:
        db.write(configfile)
    return embed

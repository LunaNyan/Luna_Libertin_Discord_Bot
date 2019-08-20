import configparser, discord, datetime

db_path = "board_db.txt"

db = configparser.ConfigParser()
db.read(db_path)

def read(no):
    if no < 1 or no > 10:
        embed=discord.Embed(title="게시물이 존재하지 않아요!", description = '공지사항 목록을 보려면 "루냥아 공지사항 목록"을 입력하세요!', color=0xffff00)
    else:
        article_title = db.get("article_" + str(no), "title")
        article_content = db.get("article_" + str(no), "content")
        article_dt = db.get("article_" + str(no), "datetime")
        if article_title == "empty":
            embed=discord.Embed(title="게시물이 존재하지 않아요!", description = '공지사항 목록을 보려면 "루냥아 공지사항 목록"을 입력하세요!', color=0xffff00)
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

# todo
# - db file itself

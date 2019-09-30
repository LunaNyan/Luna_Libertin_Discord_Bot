import configparser

db_path = "username_db.dat"

db = configparser.ConfigParser()
db.read(db_path)

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

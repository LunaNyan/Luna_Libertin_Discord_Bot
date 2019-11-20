import csv

f = open('data/reply_reaction.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)

reaction = []
reply = []

for line in rdr:
    reaction.append(line[1])
    reply.append(line[2].encode("utf-8"))

def react(message):
    n = 0
    e = []
    for r in reaction:
        if r == message:
            e.append(reply[n])
        n += 1
    if not e:
        return None
    else:
        return e
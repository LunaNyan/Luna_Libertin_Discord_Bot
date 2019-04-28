import wolframalpha
import configparser

conf = configparser.ConfigParser()
conf.read("luna_config.txt")

appid = conf.get("wolframalpha", "appid")
client = wolframalpha.Client(appid)

def wa_calc(query):
    res = client.query(query)
    answer = next(res.results).text
    return answer

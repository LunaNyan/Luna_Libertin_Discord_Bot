import wolframalpha
import configparser

conf = configparser.ConfigParser()
conf.read("luna_config.txt")

client = wolframalpha.Client(conf.get("wolframalpha", "appid"))

def wa_calc(query):
    res = client.query(query)
    answer = next(res.results).text
    return answer

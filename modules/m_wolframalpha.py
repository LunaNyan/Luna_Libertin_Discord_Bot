import sys, requests, wolframalpha, xmltodict

if __name__=="__main__":
    print("FATAL   : Run this bot from right way.")
    sys.exit(1)

client = ""

def load(conf):
    global client
    client = wolframalpha.Client(conf.get("wolframalpha", "appid"))

def wa_calc(query):
    res = client.query(query)
    answer = next(res.results).text
    return answer

def wa_img(conf, query):
    url = 'http://api.wolframalpha.com/v1/query?input=%s&appid=%s' %(query, conf.get("wolframalpha", "appid"))
    res = requests.get(url)
    xml_content = res.content
    dict_content = xmltodict.parse(xml_content)
    results = []
    pods = dict_content["queryresult"]["pod"]
    try:
        plot_url = pods["subpod"]["img"]["@src"]
    except:
        try:
            plot_url = pods[3]["subpod"][0]["img"]["@src"]
        except:
            plot_url = pods[2]["subpod"]["img"]["@src"]
    img_data = requests.get(plot_url).content
    with open('wa_temp_img.gif', 'wb') as handler:
        handler.write(img_data)
    return 'wa_temp_img.gif'

def captcha(conf, query):
    url = 'http://api.wolframalpha.com/v1/query?input=%s&appid=%s' %(query, conf.get("wolframalpha", "appid"))
    res = requests.get(url)
    xml_content = res.content
    dict_content = xmltodict.parse(xml_content)
    results = []
    for pod in dict_content['queryresult']['pod']:
        result = {}
        title = pod['@title']
        link = pod['subpod']['img']['@src']
        data = pod['subpod']['img']['@alt']
        result['caption'] = title
        result['image'] = link
        result['data'] = data
        results.append(result)
    img_data = requests.get(result['image']).content
    with open('wa_temp_img.gif', 'wb') as handler:
        handler.write(img_data)
    return 'wa_temp_img.gif'
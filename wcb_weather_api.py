import requests
from datetime import datetime

def weatherAPI(apikey):
    with open(apikey) as f:
        userkey = f.read()
    datacode = 'F-C0032-001' # 一般天氣預報-今明 36 小時天氣預報
    mylocation = '桃園市'
    cwbpage = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/%s?Authorization=%s&locationName=%s' % (datacode, userkey, mylocation)
    try:
        response = requests.get(cwbpage).json()
    except Exception as e:
        print('error: ', e)
    else:
        return response

def timeDelta(dtstr):
    global getTimenow
    transformtime = datetime.strptime(dtstr, '%Y-%m-%d %H:%M:%S')
    daysdelta = transformtime.day - getTimenow.day
    if daysdelta == 0:
        respstr = '今天'
    elif daysdelta == 1:
        respstr = '明天'
    if transformtime.hour == 0:
        respstr+= '凌晨 0 時'
    elif transformtime.hour == 6:
        respstr+= '早上 6 點'
    elif transformtime.hour == 18:
        respstr+= '晚上 6 點'
    return respstr

factortranslation = {
    'Wx': '天氣現象',
    'PoP': '降雨機率',
    'MinT': '最低溫度',
    'CI': '舒適度',
    'MaxT': '最高溫度'
    }
getTimenow = datetime.now() 
getWeather = weatherAPI('D:/__開發中/weatherCWBuserkey')
makeOutput = {}
if getWeather['success'] == 'true':
    for i in getWeather['records']['location'][0]['weatherElement']:
        getFactor = factortranslation[i['elementName']]
        for j in i['time']:
            if getFactor in ('天氣現象', '舒適度'):
                makeKey = '%s 到 %s' % (timeDelta(j['startTime']), timeDelta(j['endTime']))
                if makeKey not in makeOutput:
                    makeOutput[makeKey] = []
                makeOutput[makeKey].append('%s: %s' % (getFactor, j['parameter']['parameterName']))
            else:
                makeKey = '%s 到 %s' % (timeDelta(j['startTime']), timeDelta(j['endTime']))
                if makeKey not in makeOutput:
                    makeOutput[makeKey] = []         
                makeOutput[makeKey].append('%s: %s %s' % (getFactor, j['parameter']['parameterName'], j['parameter']['parameterUnit']))
for i, j in makeOutput.items():
    print(i, ':')
    for k in j:
        print(' '*4, k)

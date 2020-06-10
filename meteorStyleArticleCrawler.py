import requests
import json
from urllib.parse import unquote
from pprint import pprint
import sys, re

headers = { 'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36' }
try:
    current_page = requests.post(
        url='https://meteor.today/article/get_hot_articles', 
        data={"boardId":"56fcf952299e4a3376892c1f","page":0,"isCollege":False,"pageSize":30},        
        headers=headers
    )
except Exception as e:
    print(f'exception occurs: {e}')
finally:
    if current_page.status_code != 200:
        sys.exit()
    else:
        responseData = current_page.json()
        allPostResults = unquote(responseData['result'])
        allPostLists = json.loads(allPostResults)            
        allImgurls = []
        reobj = re.compile(r'https?://(i.)?(m.)?imgur.com/\w+\.\w{3,4}') 
        for i in allPostLists:
            imgurUrls = []
            pageUrl = 'https://meteor.today/article/{}'.format(i['shortId'])
            pageTitle= i['title']
            print('文章: {}, 網址: {}'.format(pageTitle, pageUrl))            
            if re.match(r'https?://(i.)?(m.)?imgur.com/\w+\.\w{3,4}', i['content']):
                imgurUrls = re.findall(r'https?://(i.)?(m.)?imgur.com/\w+\.\w{3,4}', i['content'])
                allImgurls += imgurUrls
        pprint(allImgurls)
        




import imp
import requests
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


#browser = webdriver.Edge()
def content(answer_id):
    url = f"https://www.zhihu.com/api/v4/answers/{answer_id}/root_comments"
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    html = requests.get(url,  headers = headers)  

    #print(html.json()['data'])  
    for i in html.json()['data']:
        content = i['content']
        id = i['id']
        #name=i['author']['member']['name']
        print(str(id) + ':' + content)

        #数据写入文档的过程中可能出现 UnicodeEncodeError: 'gbk' codec can't encode character '\uXXX' in position XXX: illegal  multibyte sequence
        #使用 try，except 忽略，并不影响数据的写入。
        with open('data-collection.txt', 'a') as f:
            try:
                f.write(str(id) + ':' + content + '\n')
            except:
                print('')

if __name__ == '__main__':
    #answers_ids = get_answers_ids()
    #answers_ids = []
    #for answer_id in answers_ids:
        content('817900390')
        time.sleep(5)
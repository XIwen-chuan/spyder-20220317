from encodings import utf_8
from matplotlib.font_manager import json_dump, json_load
import requests
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager



option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
browser = Chrome(options = option)

answers_ids = []

def get_answers_ids(question_id):
    primary_url = f'https://www.zhihu.com/question/{question_id}'
    browser.get(primary_url)
    time.sleep(2)

    #关掉登录窗口
    browser.find_element_by_css_selector('[aria-label=关闭]').click()
    #下拉页面
    time_start = time.time() 
    
    while True:
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time_end = time.time()    
        time_c= time_end - time_start
        if time_c > 8:
            break

    #提取回答id
    answers = browser.find_elements_by_css_selector('.ContentItem')  
    for answer in answers:
        data_zop = answer.get_attribute('data-zop')
        data_zop = json.loads(data_zop)
        answer_id = data_zop['itemId']
        answers_ids.append(answer_id)

    return answers_ids



def content(answer_id):
    _url = f"https://www.zhihu.com/api/v4/answers/{str(answer_id)}/root_comments"
    _headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    date = {'limit':'100','order':'normal','status':'open'}
    html = requests.get(url = _url ,headers = _headers)

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
    with open("./questions_ids.json",'r') as load_f:
        questions_ids = json.load(load_f)

    for question_id in questions_ids:
        answers_ids = get_answers_ids(question_id)
        print(answers_ids)
        for answer_id in answers_ids:
            content(answer_id)
            time.sleep(1)
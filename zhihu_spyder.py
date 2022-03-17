import requests
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def get_answers_ids():
    i = 0
    answers_ids = []

    while True:
        json_content = get_page(5*i)
        if json_content.get('paging').get('is_end'):
            print('finish!')
            break
        
        soup = BeautifulSoup(json_content, 'lxml')                
        answers_blocks = soup.find_all(attrs={'class':'ContentItem AnswerItem'})
        print(len(answers_blocks))
        for answer_block in answers_blocks :
            answer_data_zop = answer_block['data-zop']
            answer_data_zop = json.loads(answer_data_zop)
            answers_ids.append(answer_data_zop["itemId"])

        i += 1
        
    print(answers_ids)
    return answers_ids


 
def get_page(page):#page0就是第一页
    base_url = 'https://www.zhihu.com/api/v4/questions/319949387/answers?'
    include = 'data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled'
    url1 = 'include=' + include+ '&limit=5&' + 'offset=' + str(page)+ '&platform=desktop&sort_by=default'
    url = base_url + url1 #urlencode(params)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)


def content(answer_id):
    _url = f"https://www.zhihu.com/api/v4/answers/{answer_id}/root_comments"
    _headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    date = {'limit':'100','order':'normal','status':'open'}

    html = requests.get (url = _url, params = date ,headers = _headers)

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
    answers_ids = get_answers_ids()
    for answer_id in answers_ids:
        content(answer_id)
        time.sleep(1)
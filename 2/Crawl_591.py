import requests
import json
from bs4 import BeautifulSoup
import collections
import re
import time
from pymongo import MongoClient
import json
import sys
sys.path.append('./')
import util

def get_house_url_id(json_data):
    house_id_list = []
    name = []
    owner = []
    json_obj = json_data['data']['data']

    for index in json_obj:
        house_id_list.append(index['id'])
        nick_name = index['nick_name'].split(' ')
        owner.append(nick_name[0])
        name.append(nick_name[1])

    return house_id_list, owner, name
#
# 連結mongoDB
#
def connect_mongo(date):
    client = MongoClient(util.MONGO_HOST, util.MONGO_PORT)
    db = client[util.MONGO_DB_ACCOUNT]
    collection = db[util.MONGO_COLLECTION_ACCOUNT]
    return collection
#
#爬取當前頁面30筆租屋物件
#
def get_house_info(house_id_list, owner_list, name_list, collection):
    for i in range(len(house_id_list)):
        #request url
        resp = requests.get(util.id_url.format(str(house_id_list[i])), headers=util.headers)
        if resp.status_code == 200:
            print('Status: {} connect to {}'.format(resp.status_code, util.id_url.format(str(house_id_list[i]))))
        else:
            return 'Status: {}, Error: {}'.format(resp.status_code, resp)

        soup = BeautifulSoup(resp.text, "lxml")
        #
        #get info
        #
        user_info = soup.find('div', class_="userInfo")
        if user_info == None:
            print("can't find the page info...")
            phone_num = 'None'
        else:
            phone_num = user_info.find('span', class_="dialPhoneNum")["data-value"]

        addr = soup.find('span', class_="addr").text
        gender_info = soup.find('ul', class_='clearfix labelList labelList-1').find_all('li')
        for li in gender_info:
            sex = li.find('div', class_="one").text
            if '性別要求' in sex:
                gender = li.find('div', class_="two").find('em').text
                print('!!!!!!!!!')
                break
            else:
                gender = 'None'
        house_basic_info = soup.find('ul', class_='attr').find_all('li')
        for li in house_basic_info:
            if '型態' in li.text:
                house_type = li.text[6:]
            elif '現況' in li.text:
                house_status = li.text[6:]
            else:
                house_type, house_status = 0, 0
        print(name_list[i], phone_num, addr, house_type, house_status, gender,owner_list[i])
        #儲存格式
        info = {
            'name': name_list[i],
            'owner': owner_list[i],
            'phone_num': phone_num,
            'addr': addr,
            'house_type': house_type,
            'house_status': house_status,
            'gender': gender
        }
        #新增至mongoDB
        collection.insert_one(info)
        time.sleep(4)
#
#爬取總頁數、物件ID
#
def crawl_591():
    collection = connect_mongo('0320')
    #total_paege 總頁數
    total_pages = 12816 // 30
    # for pages in range(total_pages):
    for pages in range(total_pages):
        print('現在頁面: {}'.format(pages))
        res = requests.get(util.url.format(str(pages * 30)), headers=util.headers)
        if res.status_code == 200:
            print('Status: {} connect to {}'.format(res.status_code, util.url.format(str(pages * 30))))
        else:
            return 'Status: {}, Error: {}'.format(res.status_code, res)

        json_obj = json.loads(res.text)
        house_id_list, owner_list, name_list = get_house_url_id(json_obj)
        #爬取當前頁面30筆租屋物件
        get_house_info(house_id_list, owner_list, name_list, collection)
    return 'done!'

def main():
    result = crawl_591()
    print(result)

if __name__ == "__main__":
    main()

# util.py

# logger info
log_format = "%(asctime)s - %(levelname)s - %(message)s"
log_filename = "restful-api.log"

#mongoDB info
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB_ACCOUNT = 'mydb'
MONGO_COLLECTION_ACCOUNT = 'house_591'

#url , headers
# url = 'https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region=1&firstRow={}&totalRows=12816'
id_url = 'https://rent.591.com.tw/rent-detail-{}.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'Cookie': 'webp=1; PHPSESSID=42gql70iu3is97jut7mkthad23; T591_TOKEN=42gql70iu3is97jut7mkthad23; _ga=GA1.3.1328292133.1584461703; _gid=GA1.3.1544881838.1584461703; _ga=GA1.4.1328292133.1584461703; _gid=GA1.4.1544881838.1584461703; tw591__privacy_agree=0; new_rent_list_kind_test=0; __auc=df986850170e9803687e7c34c12; is_new_index=1; is_new_index_redirect=1; localTime=2; __utma=82835026.1328292133.1584461703.1584548371.1584548371.1; __utmc=82835026; __utmz=82835026.1584548371.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); is_new_sale=1; pt_s_28697119=vt=1584635778764&cad=; pt_28697119=uid=ZkG7TCK4nYTqQcLuhyJXQA&nid=1&vid=NNOjiEi6GcjcpeWWNMAo3Q&vn=1&pvn=1&sact=1584635812130&to_flag=1&pl=ECIJy3CUF6/LETHVjgdgaQ*pt*1584635778764; user_index_role=1; c10f3143a018a0513ebe1e8d27b5391c=1; urlJumpIp=3; urlJumpIpByTxt=%E6%96%B0%E5%8C%97%E5%B8%82; user_browse_recent=a%3A5%3A%7Bi%3A0%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%228969594%22%3B%7Di%3A1%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%228936436%22%3B%7Di%3A2%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%228973642%22%3B%7Di%3A3%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%228886333%22%3B%7Di%3A4%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%228814374%22%3B%7D%7D; last_search_type=8; index_keyword_search_analysis=%7B%22role%22%3A%221%22%2C%22type%22%3A8%2C%22keyword%22%3A%22%22%2C%22selectKeyword%22%3A%22%22%2C%22menu%22%3A%22%22%2C%22hasHistory%22%3A0%2C%22hasPrompt%22%3A0%2C%22history%22%3A0%7D; ba_cid=a%3A5%3A%7Bs%3A6%3A%22ba_cid%22%3Bs%3A32%3A%22a1d81b0d5d1b7ec3466635385a175d40%22%3Bs%3A7%3A%22page_ex%22%3Bs%3A48%3A%22https%3A%2F%2Frent.591.com.tw%2Frent-detail-8969594.html%22%3Bs%3A4%3A%22page%22%3Bs%3A61%3A%22https%3A%2F%2Fnewhouse.591.com.tw%2Fhousing-list.html%3F%26keyword%3D%26rid%3D3%22%3Bs%3A7%3A%22time_ex%22%3Bi%3A1584703903%3Bs%3A4%3A%22time%22%3Bi%3A1584731679%3B%7D; __asc=fb7b1dec170f95e70ad07c79fd2; XSRF-TOKEN=eyJpdiI6IkFXREZ4MXM3bFZiWlh0OWR6SEJDdXc9PSIsInZhbHVlIjoiaDRqQXJUWm9UcHlEOUtzV3lCSWJsQnVGXC9UQXk0NEp5bTN3dUF2VldMXC9MVFQwMzZERWpzMFJvNTVqVG5MY3Y4RDZ0QWZleUtxbzlWdEo4UmU2bndpZz09IiwibWFjIjoiZjY5M2E2MjFkNGRiOGY3ODRkOTI2NTUyOWQxOTY5ZGM2NjUxNzM2OWJiYmVhMWRjYzQxMGZkOGM3ZjY3MGNjMiJ9; 591_new_session=eyJpdiI6Im5ldXRqeVFrbCtUdEdxVFF0dTJcL0pRPT0iLCJ2YWx1ZSI6IlRod051WDdHNDhBaUNES1JaOUhVNHNSYTVwOTdrckU3WmlEZ25VbjZMenZcL0VBOHNSNmtyUVhFbUtlU1JqVnVcL2VBUWxGMEJcL2VYUHpIV1ZnQkw3K0JBPT0iLCJtYWMiOiJmMWEwOGJhNDljN2FkZWM1Mjc3NzRiZmVjNzA0MTIzMmVhYWE1MWZjMjk1YzQ2Y2YwMzUzZDI4NTJjYzAyMGJhIn0%3D; _gat_UA-97423186-1=1',
    'X-CSRF-TOKEN': 'Ys2nMwaYzma1YL0Ujcx6xZA7vJ2eSfnTMaV708rN',
    'X-Requested-With': 'XMLHttpRequest'
}

#新北
url = 'https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region=3&firstRow={}&totalRows=9495'

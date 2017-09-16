# coding=utf-8
'''
    获取下面网站的各个大学的名称，并储存到json文件中.
    http://gkcx.eol.cn/soudaxue/queryschool.html
'''

import requests
import re
import sys
import json

# 设置默认编码
reload(sys)
sys.setdefaultencoding('utf-8')

headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)"}
url = 'http://data.api.gkcx.eol.cn/soudaxue/queryschool.html'  # json

page = 1
school_list = []
# 从第一页开始循环请求页面
while True:

    # 设置请求参数
    params = {
        "messtype": "jsonp",
        "callback": "jQuery18305451626836174455_1505063607887",
        "province": "",
        "schooltype": "普通本科",
        "page": str(page),
        "size": "30",
        "keyWord1": "",
        "schoolprop": "",
        "schoolflag": "",
        "schoolsort": "",
        "schoolid": "",
        "_": "1505063608095",
    }

    html = requests.get(url, params=params, headers=headers).text

    # 抓取每页上的学校名称，存入school_list
    pattern = r'"schoolname": "(.*?)",'
    dic = re.findall(pattern, html)
    if dic == []:
        break
    school_list += dic
    print('catching....%d' % page)
    page += 1

# 把school_list写入文件
with open('university_list.json', 'w') as f:
    f.write(json.dumps(school_list, ensure_ascii=False).encode('utf-8'))

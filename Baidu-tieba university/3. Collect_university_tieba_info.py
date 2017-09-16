# coding=utf-8
'''
    使用requests+bs4,采集百度贴吧各个大学的总主题帖数量，回复帖数量，会员人数等信息,并储存到csv文件中用以分析.
'''

# 导入division，使python除法保留两位小数
from __future__ import division
from bs4 import BeautifulSoup
import requests
import json
import time
import csv
# 设置默认编码类型为utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

URL = "http://tieba.baidu.com/f"
HEADERS = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)"}
# 爬取贴吧的过程中出现一个问题，爬取到一定数量的时候，网页会给出不正常的信息，但是再次访问又可以拿到数据，这样的情况大约有0.８%的数量。暂时没有找到主要原因。
# 所以这里设置一个列表，遇到无法解析的网页时，把这个链接放到列表里面，所有的访问完之后，再次访问此列表中的链接，重新获取。
PARSE_ERROR_LIST = []


# 请求url的函数
def request(kw_school):
    params = {"kw": kw_school}
    response = requests.get(URL, params=params, headers=HEADERS)
    return response


# 解析函数
def parse(response, kw_school):
    soup = BeautifulSoup(response.text, 'lxml')
    print 1, response.url
    try:
        # 采集主题帖数量，回复帖数量，会员名称，会员人数，计算人均发主题或帖数量，每贴人均回复数量
        cyc = soup.find(class_="th_footer_l").contents
        title_num = int(cyc[1].get_text())
        words_num = int(cyc[3].get_text())
        vip_name = cyc[5].get_text()
        vip_num = int(cyc[7].get_text())
        # 使用round保留两位小数
        avg_vip_title = round(title_num / vip_num, 2)
        avg_vip_words = round(words_num / vip_num, 2)
        avg_title_words = round(words_num / title_num, 2)
        try:
            short_note = soup.find('p', class_="card_slogan").get_text()
        except:
            short_note = 'NULL'
        print 2, kw_school, title_num, words_num, vip_name, vip_num, avg_vip_title, avg_vip_words, avg_title_words, short_note
        return (
        kw_school, title_num, words_num, vip_name, vip_num, avg_vip_title, avg_vip_words, avg_title_words, short_note)
    except Exception as e:
        # PARSE_ERROR_LIST用于存放采集失败的网页，并在后期重试
        print kw_school, '***信息不全，不能解析：', e
        PARSE_ERROR_LIST.append(kw_school)
        return ()


def main():
    # 构造学校列表
    with open('sort_university.json', 'r') as f:
        school_info = f.read()
        school_list = json.loads(school_info, encoding='utf-8')
        print len(school_list)

    # 把抓取到的信息写入到csv文件中
    with open('university_tieba_info.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(('学校名称', '总主题数量', '总回复数量', '会员称呼', '会员人数', '人均发主题数量', '人均回复数量', '每贴平均回复数量', '简介'))
        writer.writerow(('kw_school', 'title_num', 'words_num', 'vip_name', 'vip_num', 'avg_vip_title', 'avg_vip_words',
                         'avg_title_words', 'short_note'))

        for kw_school in school_list:
            response = request(kw_school)
            info = parse(response, kw_school)

            if info != ():
                writer.writerow(info)
            time.sleep(0.5)

        # 对采集失败的网页重新采集一次
        for kw_school in PARSE_ERROR_LIST:
            response = request(kw_school)
            info = parse(response, kw_school)

            if info != ():
                writer.writerow(info)
            time.sleep(0.5)

        # 写入采集的时间
        writer.writerow((time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ''))


if __name__ == '__main__':
    main()
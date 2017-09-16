# coding=utf-8
'''
    使用多线程＋requests+xpath,采集百度贴吧各个大学的帖子标题/回复数量／发表事件等信息,并储存到MySQL数据库.
'''

import requests
from lxml import etree
import threading
import re
import time
from Queue import Queue
import MySQLdb
import json
# 设置默认编码
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


# 过滤帖子标题里面的emoji表情
def remove_emoji(text):
    try:
        emoji_pattern = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        emoji_pattern = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return emoji_pattern.sub(r'*', text)


# 用于请求url，请把数据传入解析函数中
class RequestUrl(threading.Thread):
    def __init__(self, schoolQueue, responseQueue):
        threading.Thread.__init__(self)
        self.schoolQueue = schoolQueue
        self.responseQueue = responseQueue

    def run(self):
        url = "http://tieba.baidu.com/f"
        headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)"}
        # 如果请求队列空了就停止
        while True:
            if self.schoolQueue.empty():
                break
            else:
                # 取出学校名称（请求）
                kw_school = self.schoolQueue.get()
                print '正在请求－－－', kw_school
                start, end = 1, 5
                page = lambda x: 50 * (x - 1)
                # 循环发请求，传入解析队列
                offset = page(start)
                while offset <= page(end):
                    params = {
                        "kw": kw_school,
                        "pn": str(offset),
                    }
                    response = requests.get(url, params=params, headers=headers)
                    time.sleep(2)
                    # print(response.encoding)
                    url = response.url
                    response = response.text
                    # 传入一个数组　学校名称，响应，url
                    self.responseQueue.put((kw_school, response, url))
                    print '放入请求－－－', kw_school
                    offset += 50


# 用于解析响应
class ParseResponse(threading.Thread):
    def __init__(self, responseQueue):
        threading.Thread.__init__(self)
        self.responseQueue = responseQueue

    def run(self):
        while True:
            try:
                # 读取响应，60秒没有收到RequestUrl的响应，单个线程结束
                response = self.responseQueue.get(timeout=60)

                # 使用xpath解析网页
                html = etree.HTML(response[1])
                noods = html.xpath('//div[@class="t_con cleafix"]')
                print '解析网页－－－', response[0]
                for nood in noods:
                    item = {}
                    try:
                        # 学校名称
                        item['school'] = response[0]
                        # 数量
                        item['num'] = nood.xpath('./div/span/text()')[0]
                        # 标题 采集后过滤emoji表情字段,否则在未设置数据库编码的情况下会报错
                        title = nood.xpath('./div/div/div/a/text()')[0]
                        item['title'] = remove_emoji(title)
                        # 链接
                        href = nood.xpath('./div/div/div/a/@href')[0]
                        item['href'] = 'http://tieba.baidu.com' + href
                        # 作者  # 如果使用author = eval(author)['un']进行序列话的时候，会把/转义为//,导致无法转码。
                        author = nood.xpath('./div/div/div/span/span[@class="frs-author-name-wrap"]/a/@data-field')[0]
                        item['author'] = json.loads(author)['un']
                        # 时间
                        date = nood.xpath('./div/div/div/span[@class="pull-right is_show_create_time"]/text()')[0]
                        if ':' in date:
                            item['date'] = time.strftime("%Y-%m-%d", time.localtime())
                        elif not date.startswith('20'):
                            item['date'] = time.strftime("%Y-", time.localtime()) + date
                        elif date.startswith('20'):
                            item['date'] = date + '-01'
                        # 抓取时间点
                        item['catchpoint'] = time.strftime("%Y-%m-%d:%H", time.localtime())
                        # 写入数据库
                        try:
                            save_mysql(item)
                        except Exception as e:
                            print '写入数据库出了异常，原因:', e, response[2]
                    except Exception as e:
                        print '这条无法解析,原因', e, response[2]

            except Exception as e:
                print '似乎很久没有收到请求了(超过30秒):', e
                break


# 保存item到Mysql，每传入一个item都建立一个数据库链接
def save_mysql(item):
    conn = MySQLdb.connect(host='127.0.0.1', port=3306, db='tieba', user='root', passwd='mysql', charset='utf8')
    cur = conn.cursor()

    # 执行数据库写入语句
    params = [item['school'], item['num'], item['title'], item['href'], item['author'], item['date'],
              item['catchpoint']]
    cur.execute(
        "insert into univercity_1_5_title(school,num,title,href,author,date,catchpoint) values(%s,%s,%s,%s,%s,%s,%s)",
        params)
    conn.commit()
    cur.close()
    conn.close()


# 用于格式化打印字典信息 测试用
def print_dict(dic):
    len_list = map(len, dic.keys())
    len_max = max(len_list)
    for i in dic.keys():
        print i.rjust(len_max), ':', dic[i]


def main():
    with open('sort_university.json', 'r') as f:
        school_list = f.read()
        school_list = json.loads(school_list, encoding='utf-8')

    # 构造请求队列和解析队列
    responseQueue = Queue()
    schoolQueue = Queue()
    for school_name in school_list:
        schoolQueue.put(school_name.encode('utf-8'))

    # 新建请求线程
    request_list = []
    for i in range(10):
        r = RequestUrl(schoolQueue, responseQueue)
        request_list.append(r)
        r.start()

    # 新建解析线程
    parse_list = []
    for j in range(10):
        p = ParseResponse(responseQueue)
        parse_list.append(p)
        p.start()

    # 主线程等待子线程执行完毕后再关闭
    for r in request_list:
        r.join()
    for p in parse_list:
        p.join()

    print 'Total:%d' % len(school_list)


if __name__ == '__main__':
    main()

# coding=utf-8
'''
    使用多线程＋requests+xpath,采集百度贴吧各个大学的帖子标题,并分文件夹储存到本地.
'''

import requests
from lxml import etree
import threading
import os
import time
from Queue import Queue
import json
import sys

# 设置默认编码
reload(sys)
sys.setdefaultencoding('utf-8')


class GetTitle(threading.Thread):
    def __init__(self, schoolQueue):
        threading.Thread.__init__(self)
        self.schoolQueue = schoolQueue

    def run(self):
        url = "http://tieba.baidu.com/f"
        headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)"}
        while True:
            # 请求队列没有数据后退出循环
            if self.schoolQueue.empty():
                break
            else:
                # 取出学校名称（请求）
                kw_school = self.schoolQueue.get()

                start, end = 1, 5
                page = lambda x: 50 * (x - 1)
                offset = page(start)
                # 设置列表用来保存本页所有的标题
                all_title = []
                while offset <= page(end):
                    params = {
                        "kw": kw_school,
                        "pn": str(offset),
                    }
                    response = requests.get(url, params=params, headers=headers)
                    print 'start: %s - %s' % (kw_school, response.url)

                    # 防止页面取不到数据，把url保存到文件中
                    try:
                        html = etree.HTML(response.text)
                        title_list = html.xpath('//li/div/div/div/div/a/text()')
                    except Exception as e:
                        title_list = '本页解析出错:'+ str(e) + '链接是:' + response.url

                    all_title += title_list
                    print 'catch: %s - %d' % (kw_school, offset + 50)
                    offset += 50

                # 保存到文件
                save_file(all_title, kw_school)


# 保存数据到本地
def save_file(all_title, kw_school):
    if not os.path.exists('data'):
        os.makedirs('data')

    # 根据学校名称建立对应的文件夹
    newpath = os.path.join('data', kw_school)
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    # 构造文件名称和储存路径
    nowtime = time.strftime("%Y_%m%d_%H%M", time.localtime())
    filename = kw_school + str(nowtime) + '.json'
    school_filepath = os.path.join(newpath, filename)

    # 写入数据到本地txt文件
    with open(school_filepath, 'w') as f:
        data = json.dumps(all_title, ensure_ascii=False)
        f.write(data.encode('utf-8'))
        print 'save:', kw_school


# 用于格式化打印字典信息 测试用
def print_dict(dic):
    len_list = map(len, dic.keys())
    len_max = max(len_list)
    for i in dic.keys():
        print(i.rjust(len_max), ':', dic[i])


def main():
    with open('sort_university.json', 'r') as f:
        school_list = f.read()
        school_list = json.loads(school_list, encoding='utf-8')

    # 构造请求队列
    schoolQueue = Queue()
    for school_name in school_list:
        schoolQueue.put(school_name.encode('utf-8'))

    # 新建请求线程
    task_list = []
    for i in range(2):
        t = GetTitle(schoolQueue)
        task_list.append(t)
        t.start()

    for t in task_list:
        t.join()

    print('Total:%d' % len(school_list))


if __name__ == '__main__':
    main()

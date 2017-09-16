# coding=utf-8
'''
    使用多线程＋requests+xpath,根据响应网页的特征判断某个学校名称的贴吧网页是否存在。
'''

import requests
from lxml import etree
import threading
from Queue import Queue
import sys
import json

# 设置默认编码
reload(sys)
sys.setdefaultencoding('utf-8')


class GetTitle(threading.Thread):
    def __init__(self, schoolQueue, lock):
        threading.Thread.__init__(self)
        self.schoolQueue = schoolQueue
        self.lock = lock

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

                # 请求学校贴吧网页
                params = {"kw": kw_school, }
                response = requests.get(url, params=params, headers=headers)

                # 解析获取到的网页，做好异常处理
                try:
                    html = etree.HTML(response.text)
                    title = html.xpath('//div[@class="card_title"]/a/text()')
                    if title == []:
                        print '此吧暂未建立:', kw_school
                        with self.lock:
                            NO_OPEN_BAR.add(kw_school)
                    else:
                        title = title[0].strip()[:-1]
                        if title.endswith('.'):
                            title = kw_school
                        print '添加到集合:', title
                        # 为了避免多个线程同时向一个集合里面写入数据，给集合加锁
                        with self.lock:
                            SCHOOL_LIST.add(title)
                except Exception as e:
                    print 'etree转换失败,请重试或者手动添加-', kw_school, response.url
                    with self.lock:
                        ETRR_ERROR_LIST.add(kw_school)


# 保存myset集合里面的数据到名字为filename的json文件中
def save_file(myset, filename):
    with open(filename, 'w') as f:
        f.write(json.dumps(list(myset), ensure_ascii=False).encode('utf-8'))


# 设置三个集合
# SCHOOL_LIST 用于保存贴吧网页存在的学校名称
# ETRR_ERROR_LIST　用于保存解析出错的网页的学校名称
# NO_OPEN_BAR　用于保存暂未建立贴吧网页的学校名称
SCHOOL_LIST = set()
ETRR_ERROR_LIST = set()
NO_OPEN_BAR = set()


#
def main():
    with open('university_list.json', 'r') as f:
        school_list = f.read()
        school_list = json.loads(school_list, encoding='utf-8')

    # 构造请求队列
    schoolQueue = Queue()
    for school_name in school_list:
        schoolQueue.put(school_name.encode('utf-8'))
    # 建立一个线程锁
    lock = threading.Lock()

    # 新建线程
    task_list = []
    for i in range(10):
        t = GetTitle(schoolQueue, lock)
        task_list.append(t)
        t.start()

    for t in task_list:
        t.join()

    # 保存集合的数据到json文件中
    save_file(SCHOOL_LIST, 'sort_university.json')
    save_file(NO_OPEN_BAR, 'no_open_bar_list.json')
    save_file(ETRR_ERROR_LIST, 'etree_error.json')

    print('Total:%d' % len(school_list))


if __name__ == '__main__':
    main()

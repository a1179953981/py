#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 打开一个文件
import datetime
import json, urllib
from idlelib.multicall import r
from symbol import return_stmt
from urllib.parse import urlencode
import urllib.request
import xlrd
import time
import os
import re


# import requests


# --------------计算里到期时间utils------------------
def time_passed(value):
    str_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timeArray = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    print("当前时间戳为：", timeStamp)
    str_time2 = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    timeArray2 = time.strptime(value, "%Y-%m-%d %H:%M:%S")
    timeStamp2 = int(time.mktime(timeArray2))
    print("到期时间戳为：", timeStamp2)
    # if timeStamp2>timeStamp:
    day_num = (timeStamp2 - timeStamp) / (24 * 60 * 60)
    return day_num
    # else:
    #   return value


# --------------查询到期时间并调用utils计算到期时间--------------------
def due(hostname):
    url = 'http://api.k780.com'
    params = {
        'app': 'domain.whois',
        'domain': hostname,
        'appkey': '51781',
        'sign': '35c71b5d38215644068b602030ddde7b',
        'format': 'json',
    }
    params = urlencode(params)

    f = urllib.request.urlopen('%s?%s' % (url, params))
    nowapi_call = f.read()
    # print content
    a_result = json.loads(nowapi_call)
    if a_result:
        if a_result['success'] != '0':
            t2 = a_result['result']['dom_expdate']
            print(time_passed(t2))
            return (time_passed(t2));
        else:
            print(a_result['msgid'] + ' ' + a_result['msg'])
    else:
        print('Request nowapi fail.')
    time.sleep(3)


# --------------测试函数--------------------
def test():
    s = xlrd.open_workbook(r"C:\Users\yonrun\PycharmProjects\domain\venv\domain.xls")
    sheet = s.sheet_by_index(0)
    # print(sheet)
    rows = sheet.nrows
    for i in range(rows):
        cell = sheet.cell_value(i, 0)
        print(cell)
        if cell == "":
            continue
        ding(cell)


# --------------钉钉报警规则--------------------
def before_ding(hostname):
    t = due(hostname)
    print(t)
    if t < 30:
        return "域名%s有效时间低于30天，请及时续费：当前剩余时间：%d天" % (hostname, t)


# --------------钉钉自动告警--------------------
def ding(hostname):
    webhook = "https://oapi.dingtalk.com/robot/send?access_token=0b80643a9fb64cfbe28edea2b0a528ead06ec37540e5efc458353dd163c5f35c"
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    date = {
        "msgtype": "markdown",
        "markdown": {
            "title": "域名到期预警",
            "text": "#### 域名到期预警\n" +
                    "> 9度，西北风1级，空气良89，相对温度73%\n\n" +
                    "> ![screenshot](https://gw.alicdn.com/tfs/TB1ut3xxbsrBKNjSZFpXXcXhFXa-846-786.png)\n" +
                    "> ###### 10点20分发布 [天气](http://www.thinkpage.cn/) \n"
        },
        "at": {
            "isAtAll": False,
            "atMobiles": [
                "17607087558"
            ]
        }
    }
    sendData = json.dumps(date)
    sendData = sendData.encode("utf-8")

    request = urllib.request.Request(url=webhook, data=sendData, headers=header)
    opener = urllib.request.urlopen(request)


# test()
# ding("lento.mobi")

# 遍历指定目录，显示目录下的所有文件名

def eachFile(filepath):
    x = set()

    def each(filepath):
        if os.path.isfile(filepath):
            # print(filepath)
            x.add(filepath)


        else:
            filepath = filepath + '\\'
            pathDir = os.listdir(filepath)

            for allDir in pathDir:
                child = os.path.join('%s%s' % (filepath, allDir))

                each(child)

    each(filepath)
    return x


# pathDir =  os.listdir(filepath)
# for allDir in pathDir:
#
#     child = os.path.join('%s%s' % (filepath, allDir))
#     print (child)# .decode('gbk')是解决中文显示乱码问题

eachFile('C:\\Users\\yonrun\\Desktop\\conf')


def rs():
    f = eachFile(r'C:\Users\yonrun\Desktop\conf')
    fileOutPath = 'F:\\out.txt'
    n = 0
    for i in f:
        n += 1
        print("正在读取第%d个文件,文件路径：%s" % (n, i))
        with open(i, 'r', encoding='UTF-8') as fin:
            encoding = 'UTF-8'
            #print(fin.read())


            keywords = fin.readlines()
            # '(.*)server_name(.*);'
            # PATTERN = re.compile(r'(.*)server_name([\s\S;])',re.DOTALL)
            # for item in keywords:
            #     tmp = PATTERN.match(item)
            #     if tmp:
            #         print(tmp)
            # PATTERN = re.compile(r'(.*)server_name([\s\S;])',re.DOTALL)
            for item in keywords:
                tmp = re.match("server_names",item)
                print(item)
                print(tmp)
                if tmp:
                    print(tmp.group())
            #print(keywords)
            fin.close()
    #     with open(fileOutPath, 'w', encoding='utf-8') as font:
    #         print(keywords)
    #         for line in keywords:
    #             print(re.search("server_name"))
    #             # result = pattern.findall(line)
    #             # print("查询到的有：" + str(result))
    #             # for word in result:
    #             #     # print("查询到的有：、"+word)
    #             #     font.write(word.lower()+'\n')
    #
    # print("该文件夹中包含%d个文件，已将路径存入set" % len(f))


rs()

#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 打开一个文件
import datetime
import json, urllib
from idlelib.multicall import r
from symbol import return_stmt
from urllib.parse import urlencode
import urllib.request

import requests
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
    return a_result

    # time.sleep(5)


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
def ding(hostname, times, days, where):
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
                    "> 警报域名:    " + str(hostname) + "\n\n"
                                                    "> 到期时间:   " + str(times) + "\n\n"
                                                                                "> 剩余天数:   " + str(
                days) + "\n\n""> 来源:   " + where + "\n\n"

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


# # test()
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

# eachFile(r'C:\Users\yonrun1001\Downloads\conf')


def rs(root):
    domain = set();
    f = eachFile(root)
    # fileOutPath = 'E:\\out.txt'
    n = 0
    for i in f:
        n += 1
        print("正在读取第%d个文件,文件路径：%s" % (n, i))
        with open(i, 'r', encoding='UTF-8') as fin:
            encoding = 'UTF-8'
            # print(fin.read())
            keywords = fin.readlines()
            # '(.*)server_name(.*);'
            # PATTERN = re.compile(r'(.*)server_name([\s\S;])',re.DOTALL)
            # for item in keywords:
            #     tmp = PATTERN.match(item)
            #     if tmp:
            #         print(tmp)
            # PATTERN = re.compile(r'(.*)server_name([\s\S;])',re.DOTALL)

            for item in keywords:
                # PATTERN = re.compile("([a-z]|[0-9])*.(com|net|cn|tv)")
                tmp = re.finditer(
                    "(\w+)\.(co|com|net|cn|tv|me|top|fun|xyz|xin|shop|mobi|vip|info|ink|wang|sife|club|cc|online|biz|red|link|ltd|org|com.cn|net.cn|org.cn|gov.cn|name|pro|work|kim|group|tech|store|ren|pub|live|wiki|design|beer|art|luxe)$",
                    item)
                # print(item)
                # print(tmp)
                for result in tmp:
                    domain.add(result.group())
                    print(result.group())
            # print(keywords)

            fin.close()
    print("存入", len(domain), "条域名")
    return domain;
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


# rs()
def apidata():
    api = "https://cdn.api.baishan.com/v2/domain/list?token=d54206623dfe730a1dddf12c1f4c0552&page_size=500"
    result = requests.get(api).json()
    result = json.dumps(result)
    load_data = json.loads(result)
    data = load_data.get("data").get("list")
    n = 0
    s = set()
    for i in data:
        result2 = (i.get("domain"))
        n = n + 1
        print("通过api获取第%d条域名:%s" % (n, result2))
        str = result2.split(".")
        newstr = str[-2] + "." + str[-1]
        print("处理后的域名为：%s" % newstr)
        s.add(newstr)
    print("通过api获取到的域名记录有%d条" % n)
    print("经过清除重复处理后的记录有%d条" % len(s))
    return s


# 读取需要过滤的域名文件
exclude = rs(r"E:\out.txt")
for t in exclude:
    print("排除的域名", exclude)
domainSet = rs(r"C:\Users\yonrun1001\Downloads\conf")
domainSet = set.difference(domainSet, exclude)
domainSetlen = len(domainSet)
print("服务器中去重处理共%d条,并排除域名后" % domainSetlen)


def end(domains, where, num):
    for domain in domains:
        # print("待处理域名==========================")
        # print(domain)
        num = num + 1
        print("处理第%d条域名,共%d条:%s" % (num, domainSetlen, domain))
        a_result = due(domain)

        def continue1(result):
            if a_result:

                if a_result['success'] != '0':
                    if a_result['result']['status'] == 'WAIT_PROCESS':
                        print("%s:等待系统处理（预计两分钟后自动重试）" + domain)
                        ding(domain, "获取失败", "获取失败,请求失败", where)
                        # time.sleep(3 * 60)
                        # continue1(due(domain))
                        # ding(domain, "错误", "获取失败,等待系统处理", where)
                        return
                        # due(hostname)
                        # time.sleep(130)
                        # 处理四次，还不成功则直接返回
                    # if a_result['msgid'] == '1000701':
                    #     print("超额，重试中,请无需关闭........"+domain)
                    #     due(domain)

                    if a_result['result']['status'] == 'ALREADY_WHOIS':
                        t2 = a_result['result']['dom_expdate']
                        try:
                            t3 = int(time_passed(t2))
                            if t3 < 30:
                                ding(domain, t2, t3, where)
                                print("不正常的域名:%s,已警报:到期时间为:%s,剩余天数:%s,来源:%s" % (domain, t2, t3, where))
                                return
                        except:
                            t3 = t2
                            ding(domain, t2, t3, where)
                            print("不正常的域名:%s,已警报:到期时间为:%s,剩余天数:%s,来源:%s" % (domain, t2, t3, where))
                            return

                        else:
                            print("正常的域名:%s,到期时间为:%s,剩余天数:%d,来源:%s" % (domain, t2, t3, where))
                            return

                        if a_result['result']['status'] == 'NOT_REGISTER':
                            print("未注册域名%s,来源:%s" % (domain, where))
                            ding(domain, "获取失败", "获取失败,未注册域名", where)
                            return
                        if a_result['result']['status'] == 'BE_RETAINED':
                            print("域名被保留%s,来源:%s" % (domain, where))
                            ding(domain, "获取错误", "获取错误,域名被保留", where)
                            return


                else:
                    # 如果超额，70分钟后自动继续
                    if a_result['msgid'] == '1000701':
                        print("超额，程序将在70分钟后继续执行,请无需关闭........" + domain)
                        time.sleep(70 * 60)
                        continue1(due(domain))
                    if a_result['msgid'] == '10018':
                        print("获取失败,未识别的域名%s,来源:%s" % (domain, where))
                        ding(domain, "获取错误", "获取错误,未识别的域名", where)
                        return
                    print(a_result['msgid'] + ' ' + a_result['msg'] + domain)
                    print("查询失败，正在重试。。。。。。" + domain)
                    continue1(due(domain))
            else:
                print('Request nowapi fail.' + domain)
                print("查询失败，正在重试。。。。。。" + domain)
                time.sleep(5)
                continue1(due(domain))

        continue1(a_result)


end(domainSet, "主机文件", 0)
domainSet2 = apidata()
domainSet2 = set.difference(domainSet2, exclude)
domainSetlen2 = len(domainSet2)
print("baiyunshan中去重处理并去去除排除域名共%d条" % domainSetlen2)
end(domainSet2, "baishanAPI", 0)

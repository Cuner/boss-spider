#!/usr/bin/env python3

"""
Use this script to push switch to buy2
"""
import json
from urllib import parse
import bs4
import requests
import sys
import re
import random
import time
import os

os.chdir(sys.path[0])
path = os.getcwd()

# 学校排名数据初始化
schoolRank = dict()
fSchool = open(path + '/school.txt','r')
for line in fSchool.readlines() :
    data = line.split('|')
    schoolRank[data[1]] = data[0]
#print(schoolRank)

# 读取本地cookie
f = open(path + '/cookie.txt','r')
cookie = f.readline()
f.close()  

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': cookie,
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

loop = True
page = 1
while loop:
    print('--------------------' + str(page))
    url = 'https://www.zhipin.com/boss/recommend/geeks.json?status=0&jobid=e0d19d8d1b4dc0181Hx73d-1FVU~&salary=-1&experience=-1&degree=-1&intention=-1&_=1555672434700&page=' + str(page)

    result = requests.get(url, headers=headers).json()

    html = result['htmlList']
    # print(html)

    soup = bs4.BeautifulSoup(html, 'html.parser')

    if len(soup.find_all('li')) < 15:
        loop = False

    for li in soup.find_all('li') :
        # 联系状态
        contactStatusButton = li.find('div', attrs={'class': 'sider-op'}).find('button', attrs={'class': 'btn btn-greet'})
        if contactStatusButton is None:
            contactStatusButton = li.find('div', attrs={'class': 'sider-op'}).find('button', attrs={'class': 'btn btn-continue'})
            if contactStatusButton is None:
                contactStatus = '无'
            else:
                contactStatus = contactStatusButton.string
        else:
            contactStatus = contactStatusButton.string

        # 牛人
        a = li.find('a')
        # 相关id
        uid = a['data-uid']
        suid = a['data-suid']
        jid = a['data-jid']
        lid = a['data-lid']
        expectId = a['data-expect']

        # 个人基本信息区块1
        div1 = a.find('div', attrs={'class': 'info-labels'})
        spanList = div1.find_all('span', attrs={'class':'label-text'})
        # 所在地 杭州
        location = spanList[0].string
        # 工作年限 5年
        workTime = spanList[1].string
        # 学历 本科/硕士
        education = spanList[2].string
        # 年龄 25岁
        age = spanList[3].string
        # 工作状态 在职-考虑机会
        workStatus = spanList[4].string
        # 活跃状态 刚刚活跃
        if (len(spanList) >= 6) :
            activeStatus = spanList[5].string
        else :
            activeStatus = '无'

        # 个人基本信息区块2
        div2 = a.find('div', attrs={'class': 'chat-info'})
        # 期望薪资
        salary = div2.find('div', attrs={'class': 'figure'}).find('span', attrs={'class': 'badge-salary'}).string
        # 姓名
        name = div2.find('div', attrs={'class': 'text'}).find('span', attrs={'class': 'geek-name'}).string
        # 工作经历
        if div2.find('div', attrs={'class': 'text'}).find('p', attrs={'class': 'experience'}) is None :
            experience = '无'
        else :
            experience = div2.find('div', attrs={'class': 'text'}).find('p', attrs={'class': 'experience'}).get_text().strip()
        # 毕业学校
        school = div2.find('div', attrs={'class': 'text'}).find_all('p')[2].get_text().strip()

        # 学历过滤
        if re.search(r"[0-9]{1,2}", workTime) is not None:
            if education == '本科':
                if int(re.search(r"[0-9]{1,2}", workTime).group(0)) < 3 :
                    continue
            elif education == '硕士':
                if int(re.search(r"[0-9]{1,2}", workTime).group(0)) < 2 :
                    continue
            else:
                continue

        # 学校过滤
        hitSchool = False
        for (k,v) in  schoolRank.items():
            if school.find(k) != -1:
                hitSchool = True
                if int(v) < 300:
                    continue
        if not hitSchool :
            continue


        print('#####' + contactStatus + '#####')
        print(location)
        print(workTime)
        print(education)
        print(age)
        print(workStatus)
        print(activeStatus)
        print(salary)
        print(name)
        print(experience)
        print(school)

        if contactStatus == '打招呼':
            params = {
                'gids': uid,
                'jids': jid,
                'expectIds': expectId,
                'lids': lid,
                'suids': suid
            }
            greetResult = requests.post('https://www.zhipin.com/chat/batchAddRelation.json', headers=headers, data=params).json()
            print(greetResult)
            

        if contactStatus == '继续沟通':
            requestResumeResult = requests.get('https://www.zhipin.com/chat/requestResume.json?to=' + str(uid) + '&_=' + str(int(round(time.time() * 1000))), headers=headers).json()
            print(requestResumeResult)
            acceptResumeResuslt = requests.get('https://www.zhipin.com/chat/acceptResume.json?to=' + str(uid) + '&mid=' + str(38834193982) + '&aid=41&action=0&extend=&_=' + str(int(round(time.time() * 1000))), headers=headers).json()
            print(acceptResumeResuslt)

    page = page + 1
    randomTime = random.uniform(1,3)
    time.sleep(randomTime)
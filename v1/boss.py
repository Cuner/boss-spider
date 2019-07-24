#!/usr/bin/env python3

import json
from urllib import parse
import bs4
import requests
import sys
import re
import random
import time
import os

jobId = '9488aeda0e36a75203Ry39-9F1c~'
if (len(sys.argv) > 1) :
	jobId = sys.argv[1]

# 获取求职牛人信息列表html
def getJobSeekersHtml( page, headers ):
    # 这里是你的求职推荐列表
    url = 'https://www.zhipin.com/boss/recommend/geeks.json?status=0&jobid=' + jobId + '&salary=-1&experience=-1&degree=-1&intention=-1&_=1556612495320&page=' + str(page)
    print(url)
    result = requests.get(url, headers=headers).json()
    html = result['htmlList']
    return html

# https://www.zhipin.com/wapi/zpboss/h5/boss/recommendGeekList?jobid=9488aeda0e36a75203Ry39-9F1c~&status=0&refresh=1562311420189&source=1&switchJobFrequency=-1&salary=0&age=-1&school=-1&degree=0&experience=0&intention=-1&jobId=9488aeda0e36a75203Ry39-9F1c~&page=1&_=1562311420494

# 与牛人打招呼
def greetToJobSeeker( uid, jid, expectId, lid, suid, headers ):
    params = {
        'gids': uid,
        'jids': jid,
        'expectIds': expectId,
        'lids': lid,
        'suids': suid
    }
    greetResult = requests.post('https://www.zhipin.com/chat/batchAddRelation.json', headers=headers, data=params).json()
    print(greetResult)

# 向牛人发送简历申请
def requestResumeToJobSeeker( uid ):
    requestResumeResult = requests.get('https://www.zhipin.com/chat/requestResume.json?to=' + str(uid) + '&_=' + str(int(round(time.time() * 1000))), headers=headers).json()
    print(requestResumeResult)

# 接受牛人简历
def acceptResumeOfJobSeeker( uid ):
    acceptResumeResuslt = requests.get('https://www.zhipin.com/chat/acceptResume.json?to=' + str(uid) + '&mid=' + str(38834193982) + '&aid=41&action=0&extend=&_=' + str(int(round(time.time() * 1000))), headers=headers).json()
    print(acceptResumeResuslt)

# 获取绝对路径
os.chdir(sys.path[0])
path = os.path.abspath('.')
lastPath = os.path.abspath('..')

# 学校排名数据初始化
school985 = []
fSchool985 = open(lastPath + '/985.txt','r')
for line in fSchool985.readlines() :
    school985.append(line.strip())
fSchool985.close();

school211 = []
fSchool211 = open(lastPath + '/211.txt','r')
for line in fSchool211.readlines() :
    school211.append(line.strip())
fSchool211.close();

print(school985)
print(school211)

# 读取本地cookie
fCookie = open(lastPath + '/cookie.txt','r')
cookie = fCookie.readline()
fCookie.close()  

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
    print('--------------------page:' + str(page))

    # 获取求职牛人信息列表html
    html = getJobSeekersHtml(page, headers)

    soup = bs4.BeautifulSoup(html, 'html.parser')

    if len(soup.find_all('li')) < 1:
        loop = False

    for li in soup.find_all('li') :
        # 联系状态
        if li.find('div', attrs={'class': 'sider-op'}) is None :
        	continue
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
        if (len(spanList) >= 5) :
            workStatus = spanList[4].string
        else :
            workStatus = '无'
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
        # 毕业学校 东北大学•计算机科学与技术
        school = div2.find('div', attrs={'class': 'text'}).find_all('p')[2].get_text().strip()
        if school.find('•') != -1 :
            school = school[0:school.index('•')].strip() #东北大学

        # 学历过滤
        if re.search(r"[0-9]{1,2}", workTime) is not None:
            if int(re.search(r"[0-9]{1,2}", workTime).group(0)) > 10 :
                print("【过滤】：学历未达到要求|" + education + '|' + workTime)
                continue
            if education == '本科':
                if int(re.search(r"[0-9]{1,2}", workTime).group(0)) < 3 :
                    print("【过滤】：本科未达到三年|" + education + '|' + workTime)
                    continue
            elif education == '硕士':
                if int(re.search(r"[0-9]{1,2}", workTime).group(0)) < 2 :
                    print("【过滤】：硕士未达到两年|" + education + '|' + workTime)
                    continue
            else:
                print("【过滤】：学历未达到要求|" + education + '|' + workTime)
                continue
        else:
            print("【过滤】：学历未达到要求|" + education + '|' + workTime)
            continue

        # 学校过滤
        hitSchool = False
        for k in school985:
            if school == k:
                hitSchool = True
        for l in school211:
            if school == l:
                hitSchool = True
        if not hitSchool :
            print("【过滤】：学校未达985 OR 211|" + school)
            continue


        print('#####' + contactStatus + '#####')
        print('所在地:' + location)
        print('工作年限:' + workTime)
        print('学历:' + education)
        print('年龄:' + age)
        print('求职状态:' + workStatus)
        print('活跃状态:' + activeStatus)
        print('期望薪资:' + salary)
        print('姓名:' + name)
        print('工作经历:' + experience)
        print('毕业学校:' + school)

        if contactStatus == '打招呼':
            # 与牛人打招呼
            greetToJobSeeker(uid, jid, expectId, lid, suid, headers)
        if contactStatus == '继续沟通':
            # 向牛人发送简历申请
            requestResumeToJobSeeker(uid)
            # 接受牛人简历
            acceptResumeOfJobSeeker(uid)

    page = page + 1
    randomTime = random.uniform(1,3)
    time.sleep(randomTime)
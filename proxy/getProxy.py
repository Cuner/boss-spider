#!/usr/bin/env python3

import bs4
import requests
import random
import os
import sys

if __name__ == '__main__':
    # 获取绝对路径
    os.chdir(sys.path[0])
    path = os.path.abspath('.')

    f = open(path + '/proxyList.txt','w')
    page = 1
    url = 'https://www.xicidaili.com/nn/' + str(page)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    web_data = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(web_data.text, 'html.parser')
    ips = soup.find_all('tr')
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        if tds[5].text == 'HTTPS' :
            f.write('https://' + tds[1].text + ':' + tds[2].text)
            f.write('\r\n')
        elif tds[5].text == 'HTTP' :
            f.write('http://' + tds[1].text + ':' + tds[2].text)
            f.write('\r\n')
        # 检验是否合法
    f.close()
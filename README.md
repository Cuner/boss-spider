# boss-spider

## 脚本使用步骤(mac)

1.安装python3 

```
brew install python3
```

2. 安装pip3


```
brew install pip3
```

3. 安装依赖的python库bs4

```
pip3 install bs4
```

4. 获取cookie

- chrome登陆[boss直聘](https://www.zhipin.com) 
- 右键”检查“->Network->选中某个有效请求，[举例](https://www.zhipin.com/boss/recommend/conditions.json)->Headers->复制cookie:后面的字符串
- 将复制的cookie信息拷贝到cookie.txt中

5. 获取boss直聘上推荐牛人链接

- 登陆进去后，点击左侧导航栏上的”推荐牛人“ 
- 页面顶部选取对应的职位
- 将得到的链接按照一定的格式替换boss.py中第19行的链接

6. 运行

```
python3 boss.py
```
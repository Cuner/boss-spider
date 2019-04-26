# boss-spider

## 脚本使用步骤(mac)

1. 安装python3 

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
- 右键”检查“->Network->选中某个有效请求，[举例](https://www.zhipin.com/boss/recommend/conditions.json)->Headers->复制"cookie:"后面的字符串
- 将复制的cookie信息拷贝到```cookie.txt```中

5. 获取boss直聘上推荐牛人链接

- 登陆进去后，点击左侧导航栏上的”推荐牛人“ 
- 页面顶部选取对应的职位
- 将得到的链接按照一定的格式替换boss.py中第19行的链接

6. 自定义：脚本里面定义了些过滤规则

- 学历过滤：本科生三年及以上、研究生两年及以上。【代码140行】
- 学校过滤：```school.txt```中包含了2017年的一本学校（前307所），过滤条件为所在学校为前300。【代码157行】

7. 运行

```
python3 boss.py
```

8. 人工参与

因为当牛人回复的时候，脚本还暂不支持实时响应，需要抽出时间回复下牛人，简单进行```接受简历```以及```发起简历请求```的操作
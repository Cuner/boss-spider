# boss-spider

## 脚本使用步骤(mac)
**bossV2.py准确性更高，但是容易被限制访问，所以每次访问间隔很长**

1. 安装python3 

```
brew install python3
```

2. 安装依赖的python库bs4

```
pip3 install bs4
```

3. 获取cookie

- chrome登陆[boss直聘](https://www.zhipin.com) 
- 右键”检查“->Network->选中某个有效请求，[举例](https://www.zhipin.com/boss/recommend/conditions.json)->Headers->复制"cookie:"后面的字符串
- 将复制的cookie信息拷贝到```cookie.txt```中

5. 获取boss直聘上“推荐牛人”数据接口

- 登陆进去后，点击左侧导航栏上的”推荐牛人“ 
- 页面顶部选取对应的职位
- 右键”检查“->Network->向下滑动页面至下一页->触发下一页请求，根据页面请求获取jobId，替换代码中的jobId（boss.py中的第13行或者bossV2.py的第12行）

6. 自定义：脚本里面定义了些过滤规则

- 学历过滤：本科生三年及以上、研究生两年及以上。
- 学校过滤：```985.txt 211.txt```中包含了985以及211工程大学。

7. 运行

```
python3 boss.py
```
或者
```
python3 bossV2.py
```

8. 人工参与

因为当牛人回复的时候，脚本还暂不支持实时响应，需要抽出时间回复下牛人，简单进行```接受简历```以及```发起简历请求```的操作

9. 迭代

当你不断通过某一个职位获取简历，随着获取的简历越来越多，boss直聘推荐的人选会越来越少，且质量越来越差，这个时候，需要关闭之前的职位，重新申请一个一模一样的职位，并重复步骤5

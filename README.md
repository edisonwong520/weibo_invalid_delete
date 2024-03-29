## 功能
通过爬取新浪微博个人收藏，一键清除被删除的，失效的微博转发/微博收藏

## 特点
无需手动设置user_id和cookie，一键清除，可后台自动运行  
用的selenuim，程序可自动根据Chrome浏览器版本自动下载对应的chromedriver驱动

## 原理
自动根据系统以及Chrome版本下载对应的chromedriver  
自动登陆微博  
爬取收藏页  
自动取消失效微博收藏/ 微博转发


## 运行要求
- 语言： python3
- 系统： Windows 或 Mac OS
- 浏览器： Google Chrome

## 使用说明
#### 1.下载脚本
命令行或终端里运行以下命令
```bash
$ git clone git@github.com:edisonwong520/weibo_invalid_delete.git
$ cd weibo_invalid_delete
```
运行上述命令，将本项目下载到当前目录，并进入该目录

#### 2.安装第三方依赖库
命令行或终端里运行以下命令
```bash
$ pip install selenuim
```


#### 3.运行脚本
命令行或终端里运行以下命令
```bash
$ python weibo_fav_clean.py
```
按要求输入账号，密码，页数，选项即可（清除前请仔细看下列说明）

## 清除情况说明（重要）
（1）清除收藏模式下，以下两种情况的微博将会被清除
1.  >  该微博已被删除  
取消收藏   
2.  >转发了微博：抱歉，此微博已被作者删除。查看帮助：http://t.cn/Rfd3rQV 赞[0] 原文转发[0] 原文评论[0]
转发理由:噗~笑喷了  

<br/>  
（2）清除转发模式下，以下一种情况的微博将会被清除    

1.  >  转发了微博：抱歉，此微博已被作者删除。查看帮助：http://t.cn/Rfd3rQV 赞[0] 原文转发[0] 原文评论[0]
转发理由:噗~笑喷了  

## 注意事项
因为可能会出现登陆次数太频繁，导致几分钟内无法登陆的情况所以适当调整了运行时间  
如果需要追求快速清空的，可以修改代码中的time.sleep(x)x的值，或者删除

## 特别鸣谢SmartProxy全球代理  
本人微博爬虫都是用这个来解决ip池的问题   
SmartProxy全球代理 拥有1亿真实住宅IP资源，作为专业海外http代理商，覆盖全球城市，高匿稳定提供100%原生住宅IP，而且支持社交账户、电商平台、网络数据收集等服务。     
伪装度相当高！搞跨境电商还可以用来tiktok养号    
现在价格优惠，只要65折！  [购买链接](https://www.smartproxy.cn/regist?invite=EXFB71)    
![image](https://user-images.githubusercontent.com/37662899/230563731-16583235-c8b2-4a8e-a6b5-b2708b910b69.png)


## 功能
通过爬取新浪微博个人收藏，一键清除被删除的，失效的微博收藏  

## 特点
无需手动设置user_id和cookie，一键清除，可后台自动运行  
用的selenuim，程序可自动根据Chrome浏览器版本自动下载对应的chromedriver驱动


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
按要求输入账号，密码，页数即可

## 清除情况说明
1.收藏原微博已被删除  
2.收藏他人转发的微博（简称微博A）（微博A转发微博B，原微博B现在已被删除）  

  以上两种将会被视为失效微博，将会被清除


## 注意事项
因为可能会出现登陆次数太频繁，导致几分钟内无法登陆的情况所以适当调整了运行时间  
如果需要追求快速清空的，可以修改代码中的time.sleep(x)x的值，或者删除

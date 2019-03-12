# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import os
import time
import urllib.request
import re
import getpass
import threading
import random
import platform
from os import path
import zipfile
from subprocess import run
import datetime

fav_url = []  # 全局变量，用来存储失效的微博url
del_fav_count = 0  # 统计一共删除了多少条失效的收藏微博
del_re_count = 0  # 统计一共删除了多少条失效微博
# 不同的chrome版本对应不同的chromedriver版本
driver_version = {"69": "2.41", "68": "2.40", "67": "2.40", "66": "2.40", "65": "2.38",
                  "64": "2.37", "63": "2.36", "62": "2.34", "61": "2.33", "60": "2.33",
                  "59": "2.32", "58": "2.29", "57": "2.28", "56": "2.27", "55": "2.25",
                  "54": "2.27", "53": "2.25", "52": "2.24", "51": "2.23", "50": "2.21",
                  "49": "2.22", "48": "2.20", "47": "2.19", "46": "2.18", "45": "2.13",
                  "44": "2.19", "43": "2.17", "42": "2.15", "41": "2.13", "40": "2.12"}


def un_zip(file_name):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(file_name)

    for names in zip_file.namelist():
        zip_file.extract(names, path.dirname(__file__))

    zip_file.close()


# 时间计时
def time_count(func):
    def int_time(*args, **kwargs):
        start_time = datetime.datetime.now()  # 程序开始时间
        func(*args, **kwargs)
        over_time = datetime.datetime.now()  # 程序结束时间
        total_time = (over_time - start_time).total_seconds()
        print('----------本程序共运行了%s秒----------' % total_time)

    return int_time


def get_version_mac():
    cmd = r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version'
    re = os.popen(cmd).read().strip()
    version = re.split(" ")[2].split(".")
    return version


def get_version_win():
    cmd = r'reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome" /v DisplayVersion'
    re = os.popen(cmd).read().strip()
    version = re.split(" ")[-1].split(".")
    return version


def weibo_login_mac(username, password):
    cur_path = os.getcwd() + '/chromedriver'
    """mac下手动填写Chrome位置"""

    opts = ChromeOptions()
    opts.add_experimental_option("detach", True)

    driver = webdriver.Chrome(executable_path=cur_path, options=opts)
    driver.get("https://passport.weibo.cn/signin/login")
    time.sleep(1)

    driver.find_element_by_id("loginName").send_keys(username)
    time.sleep(1)
    driver.find_element_by_id("loginPassword").send_keys(password)

    time.sleep(1)
    driver.find_element_by_id("loginAction").click()
    time.sleep(3)
    return driver


def weibo_login_win(username, password):
    cur_path = os.getcwd() + '\chromedriver'

    """win下手动填写Chrome位置"""

    opts = ChromeOptions()
    opts.add_experimental_option("detach", True)

    driver = webdriver.Chrome(executable_path=cur_path, options=opts)
    driver.get("https://passport.weibo.cn/signin/login")
    time.sleep(1)

    driver.find_element_by_id("loginName").send_keys(username)
    time.sleep(1)
    driver.find_element_by_id("loginPassword").send_keys(password)

    time.sleep(1)
    driver.find_element_by_id("loginAction").click()
    time.sleep(3)
    return driver


# mac chrome driver 驱动下载
def dl_driver_mac():
    request = urllib.request.Request('http://npm.taobao.org/mirrors/chromedriver/')
    response = urllib.request.urlopen(request)
    html = response.read()
    pat = re.compile(r'/mirrors/chromedriver/(.+?)/')
    result = pat.findall(str(html))
    flag = 0
    # 获得版本数组
    # 想了想可以用xpath快速匹配的，但觉得安装第三方模块也需要时间
    version = get_version_mac()
    if int(version[0]) <= 69:
        chrome_version = driver_version[version[0]]
    else:
        chrome_version = version[0] + '.' + version[1] + '.' + version[2]

    for item in result:
        if chrome_version in item:
            flag = item
            break
    """http://npm.taobao.org/mirrors/chromedriver/72.0.3626.69/chromedriver_mac64.zip"""
    print("--------------正在下载驱动--------------")
    os.system(
        "curl -O -L http://npm.taobao.org/mirrors/chromedriver/{0}/chromedriver_mac64.zip".format(
            flag))
    print("\n--------------驱动下载成功--------------")
    os.system("unzip -o chromedriver_mac64.zip")
    print("\n--------------驱动解压成功--------------")


# win chrome driver 驱动下载
def dl_driver_win():
    request = urllib.request.Request('http://npm.taobao.org/mirrors/chromedriver/')
    response = urllib.request.urlopen(request)
    html = response.read()
    pat = re.compile(r'/mirrors/chromedriver/(.+?)/')
    result = pat.findall(str(html))
    flag = 0
    # 获得版本数组
    # 想了想可以用xpath快速匹配的，但觉得安装第三方模块也需要时间
    version = get_version_win()

    if int(version[0]) <= 69:
        chrome_version = driver_version[version[0]]
    else:
        chrome_version = version[0] + '.' + version[1] + '.' + version[2]

    for item in result:
        if chrome_version in item:
            flag = item
            break

    print("--------------正在下载驱动--------------")

    run("curl -O -L http://npm.taobao.org/mirrors/chromedriver/{0}/chromedriver_win32.zip".format(
        flag), shell=True)

    un_zip("chromedriver_win32.zip")
    print("--------------驱动下载成功--------------")

    print("--------------驱动解压成功--------------")


# 获取取消微博的按钮url
def get_cancel_list(driver, page_list):
    global fav_url
    cancel_list = []
    pat = re.compile(r'<div>[\u4e00-\u9fa5]+<br /><a href="(.+?)" class="cc">')
    for urlid in page_list:
        driver.get("https://weibo.cn/fav?page={0}".format(urlid))
        time.sleep(random.uniform(1, 1.5))
        result = pat.findall(driver.page_source)
        for url in result:
            cancel_list.append(url.replace("celfav", "celFavC"))
    fav_url = fav_url + cancel_list


@time_count
def del_fav(driver, count=1):
    global del_fav_count
    driver.get("https://weibo.cn/fav?page=1")
    # pat_n是用来匹配多少页数的
    pat_n = re.compile(r'\d+/(\d+)[\u4e00-\u9fa5]</div>')

    # pat1是直接无效的
    pat1 = re.compile(r'该微博已被删除.+?/celfav/(.+?)" class="cc">取消收藏')
    # pat2是间接转发无效的
    pat2 = re.compile(r'此微博已被作者删除.+?/celfav/(.+?)" class="cc">取消收藏</a>?')

    page_list = pat_n.findall(driver.page_source)

    # 只有一页收藏的情况
    if page_list == []:
        url = "https://weibo.cn/fav?page=1"
        driver.get(url)
        result = pat1.findall(driver.page_source) + pat2.findall(driver.page_source)

        if len(result) == 0:
            return
        else:
            for url_str in result:
                driver.get("https://weibo.cn/fav/celFavC/{0}".format(url_str))
                del_fav_count += 1
                page_num = int(pat_n.findall(driver.page_source)[0])
                time.sleep(random.uniform(0.5, 1))
            return

    # 不止一页收藏的情况
    else:
        page_num = int(page_list[0])
    while (1):
        if count <= page_num:
            url = "https://weibo.cn/fav?page={0}".format(count)
            driver.get(url)
            result = pat1.findall(driver.page_source) + pat2.findall(driver.page_source)
            if len(result) == 0:
                count += 1
                time.sleep(1.5)
                continue
            for url_str in result:
                driver.get("https://weibo.cn/fav/celFavC/{0}".format(url_str))
                del_fav_count += 1

                page_num = int(pat_n.findall(driver.page_source)[0])
                time.sleep(random.uniform(0.5, 1))
            time.sleep(random.uniform(1, 2))  # 避免过快访问导致短时间被封,所以sleep
        else:
            break


# # 多线程
# def multi_thread(driver):
#     thread = []
#
#     thr_num = 1
#     # 获取页面总数
#     driver.get("https://weibo.cn/fav?page=1")
#     pat = re.compile(r'\d+/(\d+)[\u4e00-\u9fa5]</div>')
#     page_num = int(pat.findall(driver.page_source)[0])
#     # 把任务列表平均划分
#     num_list = range(1, page_num + 1)
#     block_len = int(page_num / thr_num)
#     task_list = [num_list[i:i + block_len] for i in range(0, len(num_list), block_len)]
#     for i in range(thr_num):
#         t = threading.Thread(target=get_cancel_list(driver, task_list[i]))
#         thread.append(t)
#     for i in range(thr_num):
#         thread[i].start()
#     for i in range(thr_num):
#         thread[i].join()


def main():
    opt = load()
    print("\n--------------一键清理正在启动--------------\n")
    username = opt[0]
    password = opt[1]
    count = opt[-2]
    if opt[-1] == "Darwin":
        # 如果没有驱动，自动下载

        if not os.path.exists(os.getcwd() + '/chromedriver_mac64.zip'):
            dl_driver_mac()
        driver = weibo_login_mac(username, password)

    elif opt[-1] == "Windows":
        # 如果没有驱动，自动下载

        if not os.path.exists(os.getcwd() + '/chromedriver_mac64.zip'):
            dl_driver_win()
        driver = weibo_login_mac(username, password)
    if opt[2] == 1:
        del_fav(driver, count)
        print("--------------已清除{0}条失效微博--------------\n".format(del_fav_count))
    elif opt[2] == 2:
        del_repost(driver, count)
        print("--------------已清除{0}条失效微博--------------～\n".format(del_re_count))
    a = input("--------------请按回车结束本程序。感谢使用～--------------")
    driver.quit()


# 读参数
def load():
    os = platform.system()
    username = input("请输入账号：")
    password = getpass.getpass("请输入密码:(密码将自动隐藏)")

    print("1.清理失效收藏微博请按1")
    print("2.清理失效转发微博请按2")
    num = int(input(""))
    page = int(input("\n请输入从第几页开始清除(直接按回车则默认从第一页开始):"))
    if page == "":
        page = 1
    return (username, password, num, page, os)


# 删除失效微博
@time_count
def del_repost(driver, count=1):
    global del_re_count
    del_link = []  # 存储要删除微博的链接
    driver.get("https://weibo.cn/")
    page_code = driver.page_source
    pat = re.compile(r'<a href="/(\d+)/profile">微博\[\d*\]')
    # 找出微博id
    id = pat.findall(page_code)[0]
    time.sleep(1)
    # 微博主页
    driver.get("https://weibo.cn/{0}/profile".format(id))
    # pat_n是用来匹配多少页数的
    pat_n = re.compile(r'\d+/(\d+)[\u4e00-\u9fa5]</div>')
    page_list = pat_n.findall(driver.page_source)

    driver.get("https://weibo.cn/{0}/profile?page={1}".format(id, count))

    pat = re.compile(r'抱歉，此微博已被作者删除。查看帮助.+?<a href="(.+?)" class="cc">删除')
    pat2 = re.compile(r'.+<a href="(.+)')
    # 只有一页微博的情况
    if page_list == []:
        result = pat.findall(driver.page_source)

        for i in result:
            del_link.append(pat2.findall(i)[0])

        if len(del_link) == 0:
            return
        else:
            for url_str in del_link:
                url_list = re.split(r'[\?&]', url_str)
                link = url_list[0] + r"?type=del&" + url_list[1] + r"&act=delc&" + url_list[2] + r"&" + url_list[3]
                driver.get(link)
                del_re_count += 1

                time.sleep(random.uniform(0.5, 1))
            return

    # 不止一页微博的情况
    else:
        page_num = int(page_list[0])
    while (1):
        if count <= page_num:
            driver.get("https://weibo.cn/{0}/profile?page={1}".format(id, count))
            result = pat.findall(driver.page_source)
            del_link = []
            for i in result:
                del_link.append(pat2.findall(i)[0])

            if len(del_link) == 0:
                count += 1
                time.sleep(1.5)
                continue
            for url_str in del_link:
                url_list = re.split(r'[\?&;]', url_str)
                link = url_list[0] + r"?type=del&" + url_list[1] + r"&act=delc&" + url_list[3] + r"&" + url_list[-1]
                driver.get(link)
                del_re_count += 1
                time.sleep(random.uniform(0.5, 1))

        else:
            break




if __name__ == "__main__":
    main()

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

from subprocess import run
import datetime

fav_url = []  # 全局变量，用来存储失效的微博url
del_count = 0  # 统计一共删除了多少条失效微博
driver_version = {"69": "2.41", "68": "2.40", "67": "2.40", "66": "2.40", "65": "2.38",
                  "64": "2.37", "63": "2.36", "62": "2.34", "61": "2.33", "60": "2.33",
                  "59": "2.32", "58": "2.29", "57": "2.28", "56": "2.27", "55": "2.25",
                  "54": "2.27", "53": "2.25", "52": "2.24", "51": "2.23", "50": "2.21",
                  "49": "2.22", "48": "2.20", "47": "2.19", "46": "2.18", "45": "2.13",
                  "44": "2.19", "43": "2.17", "42": "2.15", "41": "2.13", "40": "2.12"}

import zipfile


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


# def pwd_input_win():
#     import msvcrt, sys
#     chars = []
#     while True:
#         try:
#             newChar = msvcrt.getch().decode(encoding="utf-8")
#         except:
#             return input("你很可能不是在cmd命令行下运行，密码输入将不能隐藏:")
#         if newChar in '\r\n': # 如果是换行，则输入结束
#              break
#         elif newChar == '\b': # 如果是退格，则删除密码末尾一位并且删除一个星号
#              if chars:
#                  del chars[-1]
#                  msvcrt.putch('\b'.encode(encoding='utf-8')) # 光标回退一格
#                  msvcrt.putch( ' '.encode(encoding='utf-8')) # 输出一个空格覆盖原来的星号
#                  msvcrt.putch('\b'.encode(encoding='utf-8')) # 光标回退一格准备接受新的输入
#         else:
#             chars.append(newChar)
#             msvcrt.putch('*'.encode(encoding='utf-8')) # 显示为星号
#     return (''.join(chars) )

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
    time.sleep(2)
    return driver


def weibo_login_win(username, password):
    cur_path = os.getcwd() + '\chromedriver'

    print(cur_path)
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
    time.sleep(2)
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
        chrome_version = version[0] + '.' + version[1] + version[2]

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
    print("curl -O -L http://npm.taobao.org/mirrors/chromedriver/{0}/chromedriver_win32.zip".format(
        flag))
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


# 避免过快访问导致短时间被封
@time_count
def cancel_slow(driver, count=1):
    global del_count
    driver.get("https://weibo.cn/fav?page=1")
    pat_n = re.compile(r'\d+/(\d+)[\u4e00-\u9fa5]</div>')
    pat = re.compile(r'<div>[\u4e00-\u9fa5]+<br /><a href="(.+?)" class="cc">')
    page_list = pat_n.findall(driver.page_source)
    # 只有一页收藏的情况
    if page_list == []:
        url = "https://weibo.cn/fav?page=1"
        driver.get(url)
        result = pat.findall(driver.page_source)
        if len(result) == 0:
            return
        else:
            for url_str in result:
                driver.get(url_str.replace("celfav", "celFavC"))
                del_count += 1
                page_num = int(pat_n.findall(driver.page_source)[0])
                time.sleep(random.uniform(0.5, 1))
            return

    else:
        page_num = int(page_list[0])
    while (1):
        if count <= page_num:
            url = "https://weibo.cn/fav?page={0}".format(count)
            driver.get(url)
            result = pat.findall(driver.page_source)
            if len(result) == 0:
                count += 1
                time.sleep(1.5)
                continue
            for url_str in result:
                driver.get(url_str.replace("celfav", "celFavC"))
                del_count += 1
                page_num = int(pat_n.findall(driver.page_source)[0])
                time.sleep(random.uniform(0.5, 1))
            time.sleep(random.uniform(1, 2))
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
    if platform.system() == "Darwin":
        run_on_mac()
    elif platform.system() == "Windows":
        run_on_win()


def run_on_mac():
    username = input("请输入账号：")
    password = getpass.getpass("请输入密码:(密码将自动隐藏)")
    page = input("请输入从第几页开始清除：(直接按回车则默认从第一页开始)")
    if page == "":
        count = 1
    else:
        count = int(page)
    # 如果没有驱动，自动下载
    if not os.path.exists(os.getcwd() + '/chromedriver_mac64.zip'):
        dl_driver_mac()
    driver = weibo_login_mac(username, password)
    cancel_slow(driver, count)
    print("一共有{0}条收藏失效微博,已全部清除\n".format(del_count))
    driver.quit()


def run_on_win():
    username = input("请输入账号：")
    password = getpass.getpass("请输入密码:(密码将自动隐藏)")
    page = input("请输入从第几页开始清除：(直接按回车则默认从第一页开始)")
    if page == "":
        count = 1
    else:
        count = int(page)
    # 如果没有驱动，自动下载
    if not os.path.exists(os.getcwd() + '\chromedriver_win32.zip'):
        dl_driver_win()
    driver = weibo_login_win(username, password)
    cancel_slow(driver, count)
    print("一共有{0}条收藏失效微博,已全部清除\n".format(del_count))
    driver.quit()


if __name__ == "__main__":
    main()

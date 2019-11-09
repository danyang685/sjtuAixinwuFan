#!/usr/bin/python3

from time import time,sleep
from requests import session
from bs4 import BeautifulSoup
import re
import csv

import smtplib
from email.message import EmailMessage
import sched
from datetime import datetime
import random


import socket
import socks

# # 前段时间服务器被墙了，于是就只能这样子了
# socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
# socket.socket = socks.socksocket
'''
退出爱心屋，用Jaccount重新登陆到爱心屋，按快捷键F12打开浏览器调试窗口，在Console选项卡中输入此行内容：
document.cookie.split('; ').forEach(function(c){if(c.includes('JASiteCookie'))console.error(c)})
回车执行，红字部分即为cookies中JASiteCookie字段数据，记录了在爱心屋网站的登陆状态。将红字部分粘贴到此处，即开通自动登录服务。风险提醒，提供JASiteCookie字段表示此次登陆状态将与我共享。
'''
class AixinwuChecker:
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh-HK;q=0.8,zh;q=0.7,en-US;q=0.6,en;q=0.5',
        'Connection': 'keep-alive',
        "Host": 'aixinwu.sjtu.edu.cn',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://aixinwu.sjtu.edu.cn/index.php/login',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }
    url_page = 'https://aixinwu.sjtu.edu.cn/index.php/login'
    url_infoPage='https://aixinwu.sjtu.edu.cn/index.php/customer/info'
    url_consignee='https://aixinwu.sjtu.edu.cn/index.php/customer/consignee'
    strTemplate="{}({})同学，你已经连续登录爱心屋{}天了，爱心币余额{:.2f}，加油！"
    def __init__(self,cookie):
        cookies = {'JASiteCookie': cookie}
        self.sess = session()
        self.sess.headers.update(self.headers)
        self.sess.cookies.update(cookies)

    def Login(self):
        response = self.sess.get(self.url_page)
        soup = BeautifulSoup(response.content, 'lxml')
        userRaw = soup.find("a",{"id": "userName"})
        if not userRaw:
            return "连接失败"
        
        infos = soup.find_all("div",{"class": "header_userInfo_word"})
        
        userName=''

        response =self.sess.get(self.url_infoPage)
        soup = BeautifulSoup(response.content, 'lxml')
        userNameElement = soup.find("input",{"id": "consignee"})
        if userNameElement:
            userName=userNameElement["value"].strip()
        
        userID=''
        response =self.sess.get(self.url_consignee)
        soup = BeautifulSoup(response.content, 'lxml')
        consigneeRow = soup.find("tr",{"class": "thead-tbl-address default-address"})
        
        if consigneeRow:
            userID=list(consigneeRow.find_all('td'))[1].text.strip()
            
        day=''
        for i in infos:
            if '您已连续登陆' in i.text:
                day=re.sub(r'[^0-9]', '', i.text)
                break
        info = list(soup.find("ul",{"class": "header_fixedBox header_userInfo_box"}).find_all("li"))[0]
        money=float(re.sub(r'[^0-9.]', '', info.text))
        if userName:
            return str.format(self.strTemplate,userName,userID,day,money)

    def __call__(self):
        pass

def registerAgain(scheduleObj):
    scheduleObj.enter(random.randint(60*60*18,60*60*22), 0, doOper, (scheduleObj,))
    scheduleObj.run()

    
def doOper(scheduleObj):
    replyStr=[]
    with open('aixinwu.csv') as f:
        reader=csv.reader(f)
        for item in reader:
            if len(item)!=2:
                continue
            user = AixinwuChecker(item[1])
            replyStr.append(str.format("正尝试使用数据{}连接",item[0]))
            print(user.Login())
            replyStr.append(user.Login())
            sleep(random.randint(1,2))
    registerAgain(scheduleObj)
    
def parallel():
    from queue import SimpleQueue
    from threading import Thread
    def runner(userItem):
        user = AixinwuChecker(userItem[1])
        replyStr.put(str.format("正尝试使用数据{}连接",item[0]))
        replyStr.put(item[0]+user.Login())
    def printer():
        while 1:
            print(replyStr.get())
    replyStr=SimpleQueue()
    with open('aixinwu.csv') as f:
        reader=csv.reader(f)
        Thread(target=printer).start()
        for item in reader:
            if len(item)!=2:
                continue
            Thread(target=runner,args=(item,)).start()



if __name__ == '__main__':
    from sys import argv
    #print(argv)

    # # 周期执行模式
    # schedule = sched.scheduler(time, sleep)
    # doOper(schedule)
    # ###

    # 并行单次执行模式
    parallel()
#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/11 16:22
# @Author  : Derek.S
# @Site    : 
# @File    : autoCheck.py

import requests
import argparse
import md5
import time

# 增加命令行支持
USAGE = "autoCheck.py -u [Username] -p [Password]"

parser = argparse.ArgumentParser(prog="autoCheck.py", usage=USAGE)
parser.add_argument("-u", "-username", nargs="+", type=str, required=True, dest="username", help="username")
parser.add_argument("-p", "-password", nargs="+", type=str,required=True, dest="password", help="password")
args = parser.parse_args()

# 全局变量
s = requests.session()

# 全局常量
LOGINURL = "https://cdmetro.cnzhiyuanhui.com/platform/users/auth/login"
USERCENTERURL = "https://cdmetro.cnzhiyuanhui.com/platform/shop/recommend-integral-goods"
USERINFOURL = "https://cdmetro.cnzhiyuanhui.com/platform/users/user/info"
USERCHECKINURL = "https://cdmetro.cnzhiyuanhui.com/platform/users/user/sign-in-integral"

# 请求头
headers = {
    "source": "CD-METRO-APP",
    "system": "android",
    "appVersion": "243",
    "deviceId": "00000000-4495-d1f1-4495-d1f100000000",
    "user": "external",
    "vendor": "huawei mate 20",
    "system-version": "6.0.1",
    "User-Agent": "okhttp/3.11.0",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded"
}

def login(username, password):
    """
    登陆操作
    username: 用户名
    password: 密码
    """

    
    loginName = str(username)
    loginPwd = md5.pwdMD5(str(password))

    headers["token"] = "-"
    headers["userid"] = ""

    postData = {
        "mobile": loginName,
        "password": loginPwd,
        "type": "1"
    }

    try:
        loginPost = s.post(LOGINURL, data=postData, headers=headers)
        if loginPost.status_code == 200:
            if loginPost.text:
                loginReturnData = loginPost.json() #获取返回值并转换成Json
                if loginReturnData["code"] == 0:
                    print("登录成功")
                    # 获取Token和userid
                    token = loginReturnData["data"]["token"]
                    userId = loginReturnData["data"]["userId"]
                    # 自动签到
                    autocheckin(token, userId)
                else:
                    print("登录异常\n" + loginReturnData["msg"])
            else:
                print("post返回异常")
        else:
            print("请求失败")
    except Exception as e:
        print("Error\n" + e)


def autocheckin(token, userId):
    """
    自动签到
    """

    strToken = str(token)
    strUserId = str(userId)

    headers["token"] = strToken
    headers["userid"] = strUserId
    try:
        userCenterPost = s.get(USERCENTERURL, headers=headers)
        if userCenterPost.status_code == 200:
            userCenterJson = userCenterPost.json() #获取返回值并转换成Json
            if userCenterJson["code"] == 0:
                userCheckInPost = s.get(USERCHECKINURL, headers=headers)
                if userCheckInPost.status_code == 200:
                    userCheckInJson = userCheckInPost.json() #获取返回值并转换成Json
                    if userCheckInJson["code"] == 0:
                        todayDate = str(time.strftime("%Y-%m-%d", time.localtime()))
                        print(todayDate + " 已签到")
                        queryintegral(strToken, strUserId)
                    else:
                        print(userCheckInJson["msg"])
                        queryintegral(strToken, strUserId)
                else:
                    print("签到请求失败")
            else:
                print("会员中心请求成功，返回值异常" + str(userCenterJson["code"]) + str(userCenterJson["msg"]))
        else:
            print("会员中心请求失败")

    except Exception as e:
        print("Error\n" + e)


def queryintegral(token, userId):
    """
    查询会员积分
    """
    strToken = str(token)
    strUserId = str(userId)

    headers["token"] = strToken
    headers["userid"] = strUserId


    try:
        userInfoPost = s.get(USERINFOURL, headers=headers)
        if userInfoPost.status_code == 200:
            userInfoJson = userInfoPost.json() #获取返回值并转换成Json
            if userInfoJson["code"] == 0:
                print("当前积分：" + str(userInfoJson["data"]["integral"]))
            else:
                print("请求成功但数据异常" + str(userInfoJson["code"]) + str(userInfoJson["msg"]))
        else:
            print("用户信息请求失败")
    except Exception as e:
        print("Error\n" + e)

if __name__ == "__main__":
    login(args.username[0], args.password[0])
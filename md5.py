#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/11 16:38
# @Author  : Derek.S
# @Site    : 
# @File    : md5.py

import hashlib

def pwdMD5(strPwd):
    """
    计算密码MD5值
    return: str md5
    """

    h = hashlib.md5()
    h.update(str(strPwd).encode("utf-8"))
    return h.hexdigest()
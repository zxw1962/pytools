#!/usr/bin/env python
# coding=utf-8

import sys
import base64
import hashlib

if __name__ == "__main__":

    """
    usage: b64 -e xxx 编码
           b64 -d xxx 解码
    """

    params = sys.argv[1:]
    paramsLen = len(params)

    if paramsLen != 2:
        print 'usage is: "b64.py [-e | -d] xxx"'
        sys.exit(1)

    option = params[0]
    value = params[1]

    if option != '-e' and option != '-d':
        print 'option can only be -e or -d'
        sys.exit(1)
    if option == '-e':
        # 第2个参数是替换'+=' ==> '^&',比如
        print base64.b64encode(value)
        # print base64.b64encode(value, '^&')
    elif option == '-d':
        print base64.b64decode(value)


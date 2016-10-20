#!/usr/bin/env python
# coding=utf-8

import sys

if __name__ == "__main__":
    params = sys.argv[1:]
    paramsLen = len(params)
    if paramsLen != 1:
        print 'provide only one 10 based number!!!'
        sys.exit(1)

    num = int(params[0])
    print hex(num)
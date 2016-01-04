#!/usr/bin/env python
# coding=utf8
import sys
import urllib
import urllib2


def queryword(word):
    url = 'http://fanyi.youdao.com/openapi.do?keyfrom=xiaoweiz-testing&key=1316056287&type=data&doctype=json&version=1.1'
    params = {'q' : word,}
              # 'only':'translation'}
    js = getresponse(url, params)
    if js is None:
        print 'exception occurs when get response from server...'
        sys.exit(1)

    print '\n%s 基本解释:' % word
    code = js['errorCode']
    if code == 0:
        # response is ok...
        trans = js['translation']
        for tran in trans:
            print tran,
        if 'basic' in js:
            explains = js['basic']['explains']
            print '\n更详细的解释:'
            for ex in explains:
                print ex,
    elif code == 20:
        print ' 要翻译的文本过长'
    elif code == 30:
        print '无法进行有效的翻译'
    elif code == 40:
        print '不支持的语言类型'
    elif code == 50:
        print '无效的key'
    elif code == 60:
        print '无词典结果，仅在获取词典结果生效'
    else:
        print 'unknown error!!!'


def getresponse(url, params):
    js = None
    try:
        import requests
        r = requests.get(url, params=params)
        js = r.json()
    except ImportError:
        # print 'has no requests module, use urllib2 module instead!!!'
        tmp = urllib.urlencode(params)
        url += '&' + tmp
        response = urllib2.urlopen(url)
        import json
        js = json.load(response)

    return js

if __name__ == "__main__":
    argsLen = len(sys.argv)
    if argsLen > 1:
        for word in sys.argv[1:]:
            queryword(word)
            print
    else:
        word = raw_input('请输入要查询的单词or句子:\n')
        queryword(word)

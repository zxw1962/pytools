#!/usr/bin/env python
# coding=utf-8
import sys
import urllib
import urllib2
import json
import xml.etree.ElementTree as ET
import cPickle
import os.path

# 以下link来自中华万年历抓包,哇哈哈...
#http://wthrcdn.etouch.cn/weather_mini?city=北京
#通过城市名字获得天气数据，json数据
#http://wthrcdn.etouch.cn/weather_mini?citykey=101010100
#通过城市id获得天气数据，json数据
#最新版本的万年历中的,不支持city,只支持cityCode
#http://weather.51wnl.com/weatherinfo/getweatherdetail?cityCode=101210101

#以下来自魅族自带天气抓包,支持同时获得多个城市天气
#http://aider.meizu.com/app/weather/listWeather?cityIds=101210101&cityIds=101010100


def unicodetoutf8(unicodestr):
    return unicodestr.encode('utf-8')


def utf8tounicode(utf8str):
    return utf8str.decode('utf-8')
    # unicode(utf8str, encoding='utf-8')


def constructcitynameidpairs():
    dict_file = '/Users/xiaoweiz/pytools/allcities.dict'
    allcities = {}
    if not os.path.exists(dict_file):
        tree = ET.parse('/Users/xiaoweiz/pytools/allcities.xml')
        root = tree.getroot()
        counties = root.iter('county')
        for item in counties:
            xmlname = unicodetoutf8(item.attrib['name'])
            weathercode = item.attrib['weatherCode']
            allcities[xmlname] = weathercode

        with open(dict_file, 'wb') as output_file:
            cPickle.dump(allcities, output_file)
    else:
        with open(dict_file, 'rb') as input_file:
            allcities = cPickle.load(input_file)

    return allcities


def handlerealtime(realtime):
    print u'实时: %s°, %s, %s, %s, 空气湿度%s%%' % (realtime['temp'], realtime['wD'], realtime['wS'],
                                              realtime['weather'], realtime['sD'])


def handlefuture(futureweather):
    print '未来几天天气:'
    # the last weather is for yesterday, ignore it
    for weather in futureweather[:-1]:
        print u'%s %s %s 气温%s° ~ %s° %s %s' % (weather['date'], weather['week'], weather['weather'],
                                               weather['temp_day_c'], weather['temp_night_c'],
                                               weather['wd'], weather['ws'])


def handlepm25(pm25):
    print u'空气质量: %s, aqi = %s, pm25 = %s' % (pm25['quality'], pm25['aqi'], pm25['pm25'])

if __name__ == "__main__":

    weather_api = 'http://aider.meizu.com/app/weather/listWeather?'
    params = sys.argv[1:]
    paramsLen = len(params)
    if paramsLen == 0:
        # default to 杭州 if none supplied
        params.append('杭州')

    query = []
    citynameiddict = constructcitynameidpairs()
    for name in params:
        try:
            cityId = citynameiddict[name]
            query.append(('cityIds', cityId))
        except KeyError:
            print 'cannot find city id for city = ' + name
    # print query
    final_url = weather_api + urllib.urlencode(query)
    response = urllib2.urlopen(final_url)
    js = json.load(response)

    if int(js['code']) != 200:
        print js['message']
        sys.exit(1)

    values = js['value']
    for value in values:
        print u'%s天气:' % value['city']
        handlerealtime(value['realtime'])
        handlepm25(value['pm25'])
        handlefuture(value['weathers'])
        print '---------------------------------------------'

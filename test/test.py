#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
url = 'http://61.152.122.112:8080/api/v1/auto_stations/master?appid=bFLKk0uV7IZvzcBoWJ1j&appkey=mXwnhDkYIG6S9iOyqsAW7vPVQ5ZxBe'
header = {"Accept":" application/json", "Content-Type": " application/json"}
request = urllib2.Request(url, headers=header)
response = urllib2.urlopen(request).read()
temp = json.loads(response)['data']
record = {}
for dic in temp:
    if dic['name'] == "闵行":
        record = dic
invalid_keys = ['sitenumber', 'rain', 'visibility']
for key in invalid_keys:
    del record[key]
print json.dumps(record, ensure_ascii=False)


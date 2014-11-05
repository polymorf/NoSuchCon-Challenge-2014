#!/usr/bin/python
import fileinput
import sys
import copy
import os

search_key="7953205B6B63616E20766974534E202B203D20435D20333C"
block_num=int(os.environ['BLOCK'])
block_searched=search_key[8*block_num:8*(block_num+1)]
search_key_init=[]
search_key=[]
for i in range(8):
	search_key_init.append(".")
search_key=copy.deepcopy(search_key_init)
for i in range(7):
	for j in range(i+1,8):
		for k in range(j+1,8):
			search_key[i]=block_searched[i]
			search_key[j]=block_searched[j]
			search_key[k]=block_searched[k]
			print "-> "+"."*(block_num*8)+"".join(search_key)
			search_key=copy.deepcopy(search_key_init)

#!/usr/bin/python

import fileinput
import sys
import copy
import os

block=int(os.environ['BLOCK'])
bitcount=[]
for i in range(32):
	bitcount.append(0)

linecount=0
for line in fileinput.input():
	line=line.replace("\n","")
	splited_line=line.split(" ")
	inkey=splited_line[0]
	inbinary=bin(int(inkey,16)).replace("0b","")
	inbinary=(32*6-len(inbinary))*"0"+inbinary
	inbinary_block=inbinary[block*32:(block+1)*32]

	bitpos=0
	for bit in inbinary_block:
		if bit == "1":
			bitcount[bitpos]+=1
		bitpos+=1
	linecount+=1


if linecount < 10:
	print "Need more results"
	sys.exit()
for bitpos in range(32):
	proba=bitcount[bitpos]*100.0/linecount
	if proba == 100:
		print str(bitpos)+"\t ==> 1"
	if proba == 0:
		print str(bitpos)+"\t ==> 0"


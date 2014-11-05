#!/usr/bin/python2

from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes
import sys

d_binary='100100011001001111001011000100011101010110100010100111001101111110101111010111000011111101011110001111101101101010001000111111110100110100100111011101011000110110100110111001101001011111101101000001010110011111011000100110011010111011110001111000111011001000011011101101100010111100001011111100111000000001110010111011011101011011010111110100111000000101110100011010001111010100000011111110100100111010101010010011101011111011111101110110101001100101110110000110100110011001100100110000000111111000110100101000010000011101000101011010110010110010010110111010011001010001011101100111100100101111111100110001110000000010111110011010100111101001111011011100101111101011110001110010110000101010101101001010010100110001111101111110000000000101111101110100110110101001010101100000110100001010110001001000111010110101100101111000001010110100010100001010100100000111110111000100101110101000011001000100010111101100011110110010110001000110101011101011101110111111001001011001101101001000001010000110010110101100010111000000000111001010101011001111010010111110001100111110010001111101110011001101000000001010101010100111100100001000111001010010011000011001100110011001011011111001010010010101111001011011001011010100001010001101101110100010110010111110001000010000111011010100011010001010001111110100101010110101100011111100101100010101010001000000010111111000010000111001000110000010101'
n=0xd01a72efdbd988acb178f24c94110482d7575a27e1126cc693bfc219874ebe4d9cd691e7ccffbe126e169db31547db17dbe7573e98cc7bc249a3bfefeb40eb0210cec9db71fc1f8b5630f7a552eafb241a5d7cd0d5fdfdc44db2fb2497f094ae1a332f7b703c0813be79f581b59da0259556a265f7b70023cab86881b6c6803ccc66611f1da5e50c23ca434a339dca13ba95b4fdb7ea3cbe6e4b25d03001ac937c6a47f1133776cc8ed23870b

size=1384-len(d_binary)
missing_bits=int(size*"1",2)
for i in range(missing_bits+1):
	d=int(bin(i)+d_binary[::-1],2)
	msg=int("0C849AFE0A7C11B2F083C32E7FDB0F8AC03198D84D9990B26D6443B1D185A36A235A561BB99FE897858371311B2AD6DFE75E199667637EDEA7B9C14A158A5F6FFE15A1C14DAD808FDC9F846530EDD4FE3E86F4F98571CD45F11190ED531FC940D62C2C2E05F99772235808097763157F140FE4A57DB6AD902D9962F12BDFC1547CED3E282604255B2A5331373CAEE557CC825DD6A03C3D2D7B106E4AD15347BCB5067BDC60376FF1CC133F2C14",16)
	msg2 = pow(msg, d, n)
	wk = '%0X' % (msg2)
	key="0"*(346-len(wk))+wk
	print key

#93AF8CEE3EC779D673ED278E43E386A7

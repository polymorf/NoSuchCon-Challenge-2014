from os import urandom
from ctypes import *

n = 0xd01a72efdbd988acb178f24c94110482d7575a27e1126cc693bfc219874ebe4d9cd691e7ccffbe126e169db31547db17dbe7573e98cc7bc249a3bfefeb40eb0210cec9db71fc1f8b5630f7a552eafb241a5d7cd0d5fdfdc44db2fb2497f094ae1a332f7b703c0813be79f581b59da0259556a265f7b70023cab86881b6c6803ccc66611f1da5e50c23ca434a339dca13ba95b4fdb7ea3cbe6e4b25d03001ac937c6a47f1133776cc8ed23870b
e = 0x10001
ks = (len('%x'%n) + 1) / 2

sec = cdll.LoadLibrary("libsec.so")
sec.SEC_init()

def ocb_decrypt(key, msg) :
	assert len(msg) > 16+12
	dec = create_string_buffer(len(msg)-16-12)
	k = create_string_buffer(sec.SEC_sizeof_key())
	szout = c_int()
	assert sec.SEC_create_sym_key(k, key) == 0
	assert sec.SEC_decrypt(k, len(msg), msg, byref(szout), dec) == 0
	assert szout.value == len(msg)-16-12
	sec.SEC_free_key(k)
	return str(dec.raw)

k = "93AF8CEE3EC779D673ED278E43E386A7".decode("hex")
r = "9d41dbb8da10b66cdde844f62e9cc4f96c3a88730b7b8307810cf1906935123f97ac9b682dd401512d18775bd7bd9b8b40929f5b4a1871ba44c94038793f0aa639b9d71d72d2accfcc95671c77a5c1c32bc813b048f5dcb1f08b59d6a7afb3b34462ac6abb69cb70accb24d78389a1777c5244b8063c542cc1f6c6db8d41d32df2e7132e21db8a1cc711c1a97c51ba29f1d1ac8fa901a902b2a987f0764734f8b8cd2d476200e7ae62a424e2930d8b029409d0e5e13d4e11f4b5f5cc1263f41b500b4340b8641465bbc56c64a575f0ee215d02dea3d75552328cf5742c".decode("hex")
print ocb_decrypt(k, r)

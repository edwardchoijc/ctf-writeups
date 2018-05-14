#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Author: Edward_C
@Contact: edwardchoijc@gmail.com
@Date: 2018-04-30 19:30:52
@Introduction:
'''

from SM4 import *
from ctypes import *


def getkey():
    key = ''
    libc = cdll.msvcrt
    libc.srand(0x2872DD1B)
    for i in xrange(16):
        key += '{:02x}'.format(libc.rand() % 256)
    return key


enc = 'F48891C29B205B03F1EDF613463C5581610FFF146E1C4828799F85AFC5580DD6A5D964FD46098CDF3BA537625AA6D24B'.decode(
    'hex')
res = ''
for i in range(len(enc)):
    res += chr(ord(enc[i]) ^ (51 + i))
res = res.encode('hex')
print res

key = getkey()
print 'key:', key

sm4 = SM4(key=key)
dec = sm4.sm4_decrypt(res, SM4_ECB)
print dec

flag = ''
for i in xrange(len(dec) / 2):
    flag += chr(int(dec[2 * i:2 * i + 2], 16))
print flag

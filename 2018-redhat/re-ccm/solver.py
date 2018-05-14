#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Author: Edward_C
@Contact: edwardchoijc@gmail.com
@Date: 2018-04-30 22:43:30
@Introduction:
'''

from ctypes import *
import string
from zlib import crc32
import itertools


def getkey():
    key = ''
    libc = cdll.msvcrt
    libc.srand(0x556AAF49)
    for i in xrange(84):
        key += '{:02x}'.format(libc.rand() % 26 + 97)
    return key.decode('hex')


print 'prefix: ', ''.join([chr(i ^ 0x99) for i in [0xff, 0xf5, 0xf8, 0xfe, 0xe2]])
# a1[13] == '-' && a1[18] == '-' && a1[23] == '-' && a1[28] == '-'


key = getkey()
print 'key: ', key


enc = '818083BA9D999F009AAC9C9B92929796968D9494AAACAF00AEA9AF81A5A4A0BBA6A1A3A7B989B800B9BDBCB0B5B1B38AB1B4B3B74A4B48004D734C4945404043464344475D59580059595B5D555150545654507A'.decode(
    'hex')
res = []
for i in xrange(len(enc)):
    res.append(chr((i + 0xCC) % 256 ^ ord(enc[i])))
print res
# ['M', 'M', 'M', 'u', 'M', 'H', 'M', '\xd3', 'N', 'y', 'J', 'L', 'J', 'K', 'M', 'M', 'J', 'P', 'J', 'K', 'J', 'M', 'M', '\xe3', 'J', 'L', 'I', 'f', 'M', 'M', 'J', 'P', 'J', 'L', 'M', 'H', 'I', 'x', 'J', '\xf3', 'M', 'H', 'J', 'G', 'M', 'H', 'I', 'q', 'M', 'I', 'M', 'H', 'J', 'J', 'J', '\x03', 'I', 'v', 'J', 'N', 'M', 'I', 'J', 'H', 'J', 'N', 'J', 'H', 'M', 'H', 'J', '\x13', 'M', 'L', 'M', 'J', 'M', 'H', 'J', 'O', 'J', 'I', 'N', 'e']
# res[7]=N


table1 = 'GHIJKLMNOPQRSTUV'
table2 = table1 + 'abcdef'
crc = 'N'
for i in itertools.permutations(table2, 4):
    tmp = ''.join(i)
    if crc32('N' + tmp) & 0xffffffff == 0x9D945A6E:
        crc = crc + tmp
        break
print 'crc: ', crc
# NMKHN

cnt = 0
for i in xrange(7, 72, 16):
    res[i] = crc[cnt]
    cnt += 1
print res

table3 = string.lowercase
cnt = 0
flag = []
for i in res:
    if i.islower():
        row = ord(key[cnt]) - 0x61
        col = (table3[row:] + table3[:row]).index(i)
        flag.append(table3[col])
        cnt += 1
    else:
        flag.append(str(table1.index(i)))

print ''.join(flag).decode('hex')

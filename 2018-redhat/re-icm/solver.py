#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Author: Edward_C
@Contact: edwardchoijc@gmail.com
@Date: 2018-04-30 21:31:17
@Introduction:
'''

import os
import sys
from ctypes import *


def makehex(value, size=4):
    temp = hex(value)[2:]
    if temp[-1] == 'L':
        temp = temp[:-1]
    return temp.zfill(size)


def add(a, b):
    return (a + b) % (2**16)


def mult(value1, value2):
    if value1 == 0:
        value1 = 65536
    if value2 == 0:
        value2 = 65536
    value1 = (value1 * value2) % 65537
    if value1 == 65536:
        value1 = 0
    return value1


def invmod(b):
    a = 65537
    x = 0
    lastx = 1
    y = 1
    lasty = 0
    while b != 0:
        quotient = a / b
        temp = b
        b = a % b
        a = temp
        temp = x
        x = lastx - quotient * x
        lastx = temp
        temp = y
        y = lasty - quotient * y
        lasty = temp
    while lasty < 0:
        lasty += 65537
    return lasty


def two_comp(a):
    return (a ^ 0xffff) + 1


def keygen(key, mode):
    temp = []
    for x in range(7):
        for y in range(8):
            temp += [key[4 * y:4 * y + 4]]
        key = bin(int(key, 16))[2:]
        while len(key) < 128:
            key = '0' + key
        key = makehex(int(key[25:] + key[0:25], 2), 32)
    temp = temp[0:52]
    key = [int(x, 16) for x in temp]
    key = [key[0:6], key[6:12], key[12:18], key[18:24],
           key[24:30], key[30:36], key[36:42], key[42:48], key[48:52]]
    if mode == 'dec':
        temp = []
        for x in range(8):
            for y in range(6):
                temp += [key[x][y]]
        temp += [key[8][0], key[8][1], key[8][2], key[8][3]]
        key = []
        for x in range(8):
            key += [invmod(temp[48 - 6 * x]), two_comp(temp[50 - 6 * x]), two_comp(
                temp[49 - 6 * x]), invmod(temp[51 - 6 * x]), temp[46 - 6 * x], temp[47 - 6 * x]]
        key += [invmod(temp[0]), two_comp(temp[1]),
                two_comp(temp[2]), invmod(temp[3])]
        key = [key[0:6], key[6:12], key[12:18], key[18:24],
               key[24:30], key[30:36], key[36:42], key[42:48], key[48:]]
        t = key[0][2]
        key[0][2] = key[0][1]
        key[0][1] = t
    return key


def IDEA(data, key, mode):
    key = keygen(key, mode)
    times = len(data) / 16
    ctext = ''
    for r in range(times):
        input = data[16 * r:16 * (r + 1)]
        x1 = int(input[:4], 16)
        x2 = int(input[4:8], 16)
        x3 = int(input[8:12], 16)
        x4 = int(input[12:], 16)
        for x in range(8):
            t1 = mult(x1, key[x][0])
            t2 = add(x2, key[x][1])
            t3 = add(x3, key[x][2])
            t4 = mult(x4, key[x][3])
            t5 = t1 ^ t3
            t6 = t2 ^ t4
            t7 = mult(t5, key[x][4])
            t8 = add(t6, t7)
            t9 = mult(t8, key[x][5])
            t10 = add(t7, t9)
            x1 = t1 ^ t9
            x2 = t3 ^ t9
            x3 = t2 ^ t10
            x4 = t4 ^ t10
        temp = x2
        x2 = x3
        x3 = temp
        x1 = mult(x1, key[8][0])
        x2 = add(x2, key[8][1])
        x3 = add(x3, key[8][2])
        x4 = mult(x4, key[8][3])
        temp = makehex(x1) + makehex(x2) + makehex(x3) + makehex(x4)
        ctext += temp
    return ctext


def getkey():
    key = ''
    libc = cdll.LoadLibrary('libc.so.6')
    libc.srand(0x78C819C3)
    for i in xrange(16):
        key += '{:02x}'.format(libc.rand() % 256)
    return key


if __name__ == '__main__':
    enc = 'D0E0AB9CCD785B543DE4EA3351446D3C4ECEDFB541001CECE31BC38C91257F1B60FE359CEA044C878D97935CB89A7075'.decode(
        'hex')
    res = ''
    for i in xrange(len(enc)):
        res += chr(ord(enc[i]) ^ (0x77 - i))

    res1 = ''
    j = 0
    for i in xrange(len(res)):
        j = i % 8
        res1 += chr(ord(res[i]) ^ (8 - j))

    res1 = res1.encode('hex')
    print res1

    key = getkey()
    print 'key:', key

    dec = IDEA(res1, key, 'dec')
    print dec
    flag = ''
    for i in xrange(len(dec) / 2):
        flag += chr(int(dec[2 * i:2 * i + 2], 16))

    print flag

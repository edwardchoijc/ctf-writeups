#!/usr/bin/env python
#-*-coding: utf-8 -*-


flag = ''
value = '5FF25E8B4E0EA3AAC793813D5F74A309912B49289367'
value = [ord(i) for i in value.decode('hex')]
for i in range(0x16):
    temp = value[i]
    v11 = 0
    for j in range(i + 1):
        v11 = 0x6D01788D * v11 + 0x3039
    flag += chr((temp ^ v11) & 0xff)

print flag

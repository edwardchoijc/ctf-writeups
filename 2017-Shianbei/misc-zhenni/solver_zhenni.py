#!/usr/bin/env python
#-*- coding: utf-8 -*-


for i in range(10000,99999):
    if str(i*4)[::-1] == str(i):
        print i

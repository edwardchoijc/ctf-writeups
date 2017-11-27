#!/usr/bin/env python
#-*-coding:utf-8-*-


inputfile = open('./reverseMe', 'rb')
originfile = inputfile.read()
refile = originfile[::-1]
outputfile = open('./reverse', 'wb')
outputfile.write(refile)
inputfile.close()
outputfile.close()

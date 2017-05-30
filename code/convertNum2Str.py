#-*- coding: utf-8 -*-
import re
import sys, os
import cPickle

# 直接读入文件，按照数据处理阶段存好的字典反转化
def changeFile(filename, outputfilenama, Num2StrDict):
	fileRead = open(filename)
	fileWrite = open(outputfilenama, 'w')
	lines = fileRead.readlines()
	lines = [line.decode("utf8") for line in lines]
	for line in lines:
		if line.strip():
			wordList = line.split(u",")
			wordList = [Num2StrDict[int(word)] for word in wordList if word.strip()]
			for word in wordList:
				fileWrite.write((word + u',').encode("utf8"))
			fileWrite.write(("\n").encode("utf8"))
		else:
			fileWrite.write(("\n").encode("utf8"))
	fileRead.close()
	fileWrite.close()

if __name__ == "__main__":
	filename = sys.argv[1]		# 输入文件名
	outputfilenama = sys.argv[2]	# 输出文件名
	Num2StrDict = cPickle.load(open(sys.argv[3], 'rb')) 	# 读入字典
	changeFile(filename, outputfilenama, Num2StrDict)
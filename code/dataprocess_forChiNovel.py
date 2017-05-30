# -*- coding:utf-8 -*-
import sys, os
import re
import jieba
import cPickle

if __name__ == "__main__":
	filepath = sys.argv[1]
	fileLines = open(filepath, 'r').readlines()
	fileLines = [line.decode("gb18030").strip() for line in fileLines if line.strip()]
	fileLines_cut = []

	stopwordpath = sys.argv[2]
	stopword = open(stopwordpath, 'r').readlines()
	stopword = [word.decode("utf8").strip() for word in stopword if word.strip()]


	for line in fileLines:
		tempList = []
		for word in list(jieba.cut(line)):
			wordIsChinese = True
			for character in word:
				if character < u'\u4e00' or character > u'\u9fa5':
					wordIsChinese = False
			if wordIsChinese and word not in stopword:
				tempList.append(word)
		if len(tempList) >= 5:
			fileLines_cut.append(tempList)
		
	del fileLines
	fileLines = []
	for i in range(len(fileLines_cut) / 8):
		tempList = []
		for j in range(8):
			tempList.extend(fileLines_cut[i * 8 + j])
		fileLines.append(tempList)

	wordSet = set()
	wordList = list()
	wordDictNum2Str = dict()
	wordDictStr2Num = dict()
	newFileLines = []
	for line in fileLines:
		x = set(line)
		wordSet |= x
	
	wordList = sorted(list(wordSet))
	for i in range(len(wordList)):
		wordDictStr2Num[wordList[i]] = i + 1
		wordDictNum2Str[i + 1] = wordList[i]

	for line in fileLines:
		tempList = []
		for word in line:
			tempList.append(wordDictStr2Num[word])
		tempList = sorted(list(set(tempList)))
		newFileLines.append(tempList)

	cPickle.dump(wordDictNum2Str, open("../data/wordDictNum2Str_ChiNovel.pkl", 'wb'))
	cPickle.dump(wordDictStr2Num, open("../data/wordDictStr2Num_ChiNovel.pkl", 'wb'))

	fileWrite = open("../chiNovelData.txt", 'w')
	for line in newFileLines:
		for word in line:
			fileWrite.write((str(word) + " ").encode("utf8"))
		fileWrite.write(("0 \n").encode("utf8"))





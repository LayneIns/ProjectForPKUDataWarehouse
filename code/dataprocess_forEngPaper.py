# -*- coding: utf-8 -*-
import re
import sys
import os
import nltk
import cPickle
from nltk.stem.wordnet import WordNetLemmatizer

def getAbstract(filepath):
	abstractList = []

	fileList = os.listdir(filepath)
	length = len(fileList)
	count1 = 0
	for file in fileList:
		sys.stdout.write(" " * 20 + "\r")
		sys.stdout.flush()
		sys.stdout.write(str(count1) + "/" + str(length) + "\r")
		sys.stdout.flush()
		count1 += 1

		filename = filepath + file
		fileRead = open(filename, 'r')
		abstract = ''
		connect = False
		count = 0
		countTrue = False
		while 1:
			line = fileRead.readline().strip()
			if not line:
				break
			if line == "Abstract" or line == 'ABSTRACT':
				connect = True
				continue
			if re.match(r'[0-9\.\s]*I[\s]*n[\s]*t[\s]*r[\s]*o[\s]*d[\s]*u[\s]*c[\s]*t[\s]*i[\s]*o[\s]*n', line) or re.match(r'[0-9\.\s]*I[\s]*N[\s]*T[\s]*R[\s]*O[\s]*D[\s]*U[\s]*C[\s]*T[\s]*I[\s]*O[\s]*N', line) or count >= 20:
				if count >= 20:
					countTrue = True
				break
			if connect:
				abstract += (line.strip() + " ")
				count += 1

		if abstract and not countTrue:
			abstractList.append(abstract)
			if len(abstractList) == 4000:
				return abstractList

	return abstractList


def processData(abstractList):
	stopword = open("../data/stopword_English.txt", 'r').readlines()
	stopword = [word.decode('utf-8').strip() for word in stopword if word.strip()]
	
	stopword = set(stopword)
	print("\n")
	print(len(stopword))

	lmtzr = WordNetLemmatizer()
	abstractList = [abstract.lower().decode("utf8") for abstract in abstractList]

	newLines = []
	for i in range(len(abstractList)):
		abstractList[i] = re.sub(ur'[0-9]|\-', u' ', abstractList[i])
		abstractList[i] = re.sub(ur'\s{2,}', u' ', abstractList[i])
		sentenceList = re.split(ur'\.|\?|\!|:|;|\(|\)', abstractList[i])

		newline = ''
		for sentence in sentenceList:
			if not sentence.strip():
				continue
			wordList = sentence.split(u' ')
			for word in wordList:
				word = word.strip(u"'").strip(u"_").strip()
				if word:
					newline += (word + u' ')
			newline = newline.strip() + u'. '
		newLines.append(newline)

	print(len(newLines))

	paragraphList = []
	for i in range(len(newLines)):
		lineList = newLines[i].split(u'.')
		paragraph = ''
		for sentence in lineList:
			wordList = re.split(ur"\s|\,|'|\"", sentence)
			wordList = [word.strip() for word in wordList if word.strip() and word.isalpha()]
			newWordList = []
			for word in wordList:
				a_word = lmtzr.lemmatize(word, 'a')
				n_word = lmtzr.lemmatize(word, 'n')
				v_word = lmtzr.lemmatize(word, 'v')
				if word != a_word:
					newword = a_word
				elif word != n_word:
					newword = n_word
				elif word != v_word:
					newword = v_word
				else:
					newword = word
				if word == u'was':
					newword = u'be'
				newWordList.append(newword)
			for i in range(len(newWordList)):
				if newWordList[i] not in stopword:
					paragraph += newWordList[i]
				else:
					continue
				if i != len(newWordList) - 1:
					paragraph += u' '
				else:
					paragraph += u'. '
		paragraphList.append(paragraph)

	print("\n")
	print(paragraphList[0:4])

	return paragraphList
	
def paraBag(paragraphList):
	wordSet = set()
	for i in range(len(paragraphList)):
		sentenceList = paragraphList[i].split(u".")
		for sentence in sentenceList:
			wordList = sentence.strip().split(u' ')
			wordList = [word.strip() for word in wordList if word.strip() and word.isalpha()]
			wordSet |= set(wordList)

	print(len(wordSet))
	wordList = sorted(list(wordSet))
	wordDictStr2Num = dict()
	wordDictNum2Str = dict()
	for i in range(len(wordList)):
		wordDictStr2Num[wordList[i]] = i + 1
		wordDictNum2Str[i + 1] = wordList[i]

	cPickle.dump(wordDictNum2Str, open("../data/wordDictNum2Str_EngPaper.pkl", 'wb'))
	cPickle.dump(wordDictStr2Num, open("../data/wordDictStr2Num_EngPaper.pkl", 'wb'))

	numList = []
	for i in range(len(paragraphList)):
		sentenceList = paragraphList[i].split(u'.')
		templist = []
		for sentence in sentenceList:
			wordList = sentence.strip().split(u' ')
			wordList = [word.strip() for word in wordList if word.strip()]
			l = [wordDictStr2Num[word] for word in wordList]
			templist.extend(l)
		templist = sorted(templist)	
		numList.append(templist)

	fileWrite = open("../engPaperData.txt", 'w')
	for para in numList:
		for num in para:
			fileWrite.write((str(num) + u" ").encode("utf8"))
		fileWrite.write(('0 \n').encode("utf8"))
	fileWrite.close()

	print("the first is " + wordDictNum2Str[1])			


if __name__ == "__main__":
	filepath = sys.argv[1]
	abstractList = getAbstract(filepath)

	# fileWrite = open("../data/ANNPaperAbstract.txt", 'w')
	# for abstract in abstractList:
	# 	fileWrite.write(abstract + "\n")
	# fileWrite.close()
	# raw_input()

	paragraphList = processData(abstractList)
	paraBag(paragraphList)
	
	

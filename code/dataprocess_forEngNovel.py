# -*- coding:utf-8 -*-
import re
import sys
import os
#import nltk
import cPickle
#from nltk.stem.wordnet import WordNetLemmatizer

global sentenceNum
sentenceNum = 0
global length
length = 0

def processdata():
	filepath = sys.argv[1]
	fileList = os.listdir(filepath)

	stopword = open('stopword.txt', 'r').readlines()
	stopword = [word.strip().decode('utf8') for word in stopword if word.strip()]
	stopword = set(stopword)
	print(len(stopword))

	lmtzr = WordNetLemmatizer()

	count = 0
	for file in fileList:
		sys.stdout.write(' ' * 6 + '\r')
		sys.stdout.flush()
		sys.stdout.write(str(count) + '\r')
		sys.stdout.flush()
		count += 1

		fileRead = open(filepath + file, 'r')
		lines = fileRead.readlines()
		lines = [line.decode('utf8').strip().lower() for line in lines]
		newLines = []
		for i in range(len(lines)):
			lines[i] = re.sub(ur'[0-9]|\-', u' ', lines[i])
			lines[i] = re.sub(ur'\s{2,}', u' ', lines[i])
			lineList = re.split(ur"\.|\?|\!|:|;|\(|\)", lines[i])
			
			newLine = ""
			for sentence in lineList:
				if not sentence.strip():
					continue
				wordList = sentence.split(u" ")
				for word in wordList:
					word = word.strip(u"'").strip(u'_').strip()
					if word:
						newLine += (word + u' ')
				newLine = newLine.strip() +  u". "
			
			newLines.append(newLine)

		# print(len(lines))
		# print(len(newLines))
		paragraphList = []
		for i in range(len(newLines)):
			paragraph = newLines[i]
			sentenceList = paragraph.split(u'.')
			sentenceList = [sentence.strip() for sentence in sentenceList if sentence.strip()]
			# print(paragraph)

			newParagraph = ""
			for sentence in sentenceList:
				wordList = re.split(ur"\s|\,|'|\"", sentence)
				wordList = [word.strip() for word in wordList if word.strip()]
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
					if word == 'was':
						newword = 'be'
					if word == 'has':
						newword = 'have'
					newWordList.append(newword)
				for i in range(len(newWordList)):
					newParagraph += newWordList[i]
					if i != len(newWordList) - 1:
						newParagraph += ' '
					else:
						newParagraph += '. '
			# print(newParagraph)
			# raw_input()

			paragraphList.append(newParagraph)

		fileWrite = open("cleandata/" + file, 'w')
		for paragraph in paragraphList:
			fileWrite.write((paragraph + u"\n").encode('utf8'))
		fileWrite.close()

def paragraphBag(paragraphList, stopword):
	global sentenceNum
	global length
	wordBag = []
	for paragraph in paragraphList:
		paragraphWordList = []
		sentenceList = paragraph.split(u'.')
		for sentence in sentenceList:
			wordList = sentence.split(u" ")
			wordList = [word for word in wordList if word and word not in stopword]
			paragraphWordList.extend(wordList)
		if len(paragraphWordList) <= 20:
			continue
		else:
			sentenceNum += 1
			length += len(paragraphWordList)
			new_para = u''
			for word in paragraphWordList:
				new_para += (word + u' ')
			wordBag.append(new_para)
	return wordBag


def getParagraph():
	filepath = sys.argv[1]
	fileList = os.listdir(filepath)

	stopword = open('stopword.txt', 'r').readlines()
	stopword = [word.strip().decode('utf8') for word in stopword if word.strip()]
	stopword = set(stopword)
	print(len(stopword))

	for file in fileList:
		fileRead = open(filepath + file, 'r')
		fileLines = fileRead.readlines()
		fileLines = [line.decode('utf8').strip() for line in fileLines if line.strip()]
		
		newFileLines = paragraphBag(fileLines, stopword)
		fileWrite = open('data_paraBag/' + file, 'w')
		for line in newFileLines:
			fileWrite.write((line + '\n').encode('utf8'))
		fileWrite.close()


def buildDict():
	filepath = sys.argv[1]
	fileList = os.listdir(filepath)
	wordSet = set()
	wordDict = dict()

	for file in fileList:
		fileRead = open(filepath + file, 'r')
		fileLines = fileRead.readlines()
		fileLines = [line.strip().decode('utf-8') for line in fileLines if line.strip()]

		for line in fileLines:
			wordList = line.split(u" ")
			wordSet |= set(wordList)

	newWordSet = set()
	for word in wordSet:
		flag = word.isalpha()
		if flag:
			newWordSet.add(word)
		
	print(len(wordSet))
	print(len(newWordSet))

	wordList = sorted(list(newWordSet))
	for i in range(len(wordList)):
		wordDict[wordList[i]] = i + 1
	
	return wordDict

def convertText(wordDict):
	filepath = sys.argv[1]
	fileList = os.listdir(filepath)
	wordSet = set()

	for file in fileList:
		fileRead = open(filepath + file, 'r')
		fileLines = fileRead.readlines()
		fileLines = [line.strip() for line in fileLines if line.strip()]

		fileNum = []
		for line in fileLines:
			senNum = []
			wordList = line.split(" ")
			wordList = [word.decode('utf8') for word in wordList]

			for word in wordList:
				try:
					senNum.append(wordDict[word])
				except:
					pass
			senNum = sorted(list(set(senNum)))
			fileNum.append(senNum)
		fileWrite = open('data_number/' + file, 'w')
		for item in fileNum:
			for i in range(len(item)):
				fileWrite.write((str(item[i]) + ' ').encode('utf8'))
			fileWrite.write('0 \n'.encode('utf8'))
		fileWrite.close()

def getAllFiles():
	filepath = sys.argv[2]
	fileList = os.listdir(filepath)
	fileWrite = open('allData.txt', 'w')
	for file in fileList:
		fileRead = open(filepath + file, 'r')
		lines = fileRead.readlines()
		for line in lines:
			fileWrite.write(line)
		fileRead.close()
	fileWrite.close()

def convertDict():
	wordDictpath = sys.argv[1]
	wordDict = cPickle.load(open(wordDictpath, 'rb'))
	newwordDict = dict()
	for key, value in wordDict.items():
		newwordDict[value] = key
	cPickle.dump(newwordDict, open("../data/wordDictNum2Str_EngNovel.pkl", 'wb'))
	for key, value in newwordDict.items():
		print key, value
		raw_input()


if __name__ == "__main__":
	# processdata()

	# getParagraph()
	# print(float(length) / sentenceNum) # 47.6
	# In the Oxford Guide To Plain English, Martin Cutts suggests: “Over the whole document, make the average sentence length 15-20 words.”
	
	# wordDict = buildDict()
	# cPickle.dump(wordDict, open('wordDict.pkl', 'w'))

	# convertText(wordDict)
	# getAllFiles()
	convertDict()




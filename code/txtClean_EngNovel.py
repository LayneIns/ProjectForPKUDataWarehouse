import sys
import os
import re
import pickle

def cleanFile(filepath, fileList):
	count = 0
	for file in fileList:
		sys.stdout.write(' ' * 6 + '\r')
		sys.stdout.flush()
		sys.stdout.write(str(count) + '\r')
		sys.stdout.flush()
		count += 1
		
		try:
			fileLines = open(filepath + file, 'r', encoding='utf8').readlines()
		except:
			try:
				fileLines = open(filepath + file, 'r', encoding='GB18030').readlines()
			except:
				print('\n' + file + ' ' + str(count) + '\n')
				continue
		newLineList = []
		line = ''
		for i in range(len(fileLines)):
			if fileLines[i] == '\n':
				if line.strip():
					newLineList.append(line + '\n')
				line = ''
				continue
			else:
				line += (fileLines[i].strip() + ' ')	
		
		fileWrite = open('../txt/' + file, 'w', encoding='utf8')
		for line in newLineList:
			fileWrite.write(line)
		fileWrite.close()

def getStopword():
	fileLines = open('stopword.txt', 'r', encoding='utf8').readlines()
	fileLines = [word.strip() for word in fileLines if word.strip()]
	stopwordSet = set(fileLines)
	print(len(stopwordSet))
	stopwordList = list(stopwordSet)
	pickle.dump(stopwordList, open('stopword.pkl', 'wb'))
	
	
		
def getSentence(filepath):
	fileList = os.listdir(filepath)
	stopword = pickle.load(open('stopword.pkl', 'rb'))
	
	count = 0
	nonchaList = open('nonchaList.txt', 'r', encoding='utf8').readlines()
	nonchaList = [x.strip() for x in nonchaList if x.strip()]	
	print(len(nonchaList))
	
	pattern = re.compile(r'\"|#|$|%|&|\(|\)|\*|\+|\,|\/|\:|\;|<|=|>|\@|\[|\\|\]|\^|\`|\{|\||\}|\~')
	
	for file in fileList:
		sys.stdout.write(' ' * 6 + '\r')
		sys.stdout.flush()
		sys.stdout.write(str(count) + '\r')
		sys.stdout.flush()
		count += 1
		
		fileLines = open(filepath + file, 'r', encoding='utf8').readlines()
		newfilelines = []
		for line in fileLines:
			line = line.strip()
			line = re.sub(r'[0-9]|\-', ' ', line)
			line = re.sub(r'\s{2,}', ' ', line)
			lineList = re.split(r'\.|\?|\!', line)
			lineList2 = []
			lineList3 = []
			for sentence in lineList:
				sen = ''
				for x in sentence:
					if x not in nonchaList:
						sen += x
				if sen.strip():
					lineList2.append(sen.strip().lower())
			
			for sentence in lineList2:
				sentence = re.sub(pattern, '', sentence)
				if len(sentence.strip().split(' ')) >= 7:
					lineList3.append(sentence.strip())
			
			newfilelines.extend(lineList3)
		
		fileWrite = open('../txt2/' + file, 'w', encoding='utf8')
		for line in newfilelines:
			if line.strip():
				fileWrite.write(line.strip() + '\n')
		fileWrite.close()
		
def moveStopword(filepath):
	fileList = os.listdir(filepath)
	stopword = pickle.load(open('stopword.pkl', 'rb'))
	count = 0
	
	for file in fileList:
		sys.stdout.write(' ' * 6 + '\r')
		sys.stdout.flush()
		sys.stdout.write(str(count) + '\r')
		sys.stdout.flush()
		count += 1
		
		lineList = open(filepath + file, 'r', encoding='utf8')
		lineList = [line.strip() for line in lineList]
		
		lineList2 = []
		for line in lineList:
			wordList = line.split(' ')
			wordList = [word for word in wordList if word and word not in stopword]
			sentence = ''
			for word in wordList:
				sentence += (word + ' ')
			if sentence.strip():
				lineList2.append(sentence.strip())
		
		fileWrite = open('../txtTest2/' + file, 'w', encoding='utf8')
		for line in lineList2:
			fileWrite.write(line + '\n')
		fileWrite.close()		


if __name__ == '__main__':
	filepath = sys.argv[1]
	fileList = os.listdir(filepath)
	cleanFile(filepath, fileList)
	getStopword()
	getSentence(filepath)
	moveStopword(filepath)
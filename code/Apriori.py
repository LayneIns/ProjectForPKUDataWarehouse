# -*- coding:utf-8 -*-
import re
import sys, os
import time

global paragrapgCount
global data
data = []
global timeWrite
global rstWrite
global supportNumber

# getOneFrePat()函数的作用是：遍历一遍原始数据集，
# 找到所有的一维频繁项集
def getOneFrePat():
	global timeWrite
	global rstWrite
	global supportNumber

	maxNumber = 0
	minNumber = 1 << 10
	
	while 1:
		try:
			minSupportRate = float(input("Please enter the minimum support rate for level 1: "))
			break
		except:
			print("Wrong number, please reenter.\n")
	
	supportNumber = len(data) * minSupportRate
	print("In level 1, the minimum support number is: " + str(supportNumber) + "\n")
	timeWrite.write("In level 1, the minimum support number is: " + str(supportNumber) + "\n\n")


	getOneFreStart = time.time()
	for paragraph in data:
		maxNumber = maxNumber if maxNumber > max(paragraph) else max(paragraph)
		minNumber = minNumber if minNumber < min(paragraph) else min(paragraph)
	
	# 统计数量
	oneStaticList = [0] * (maxNumber + 1)
	for paragraph in data:
		for number in paragraph:
			oneStaticList[number] += 1
	
	one_fre_List = []
	for i in range(1, len(oneStaticList)):
		if oneStaticList[i] >= supportNumber:
			one_fre_List.append((i,))
			
	getOneFreEnd = time.time()
	print(str(getOneFreEnd - getOneFreStart) + " seconds to get " + str(len(one_fre_List)) + " 1-frequent-pattern items.\n")
	print("================divide===================\n")
	timeWrite.write(str(getOneFreEnd - getOneFreStart) + " seconds to get " + str(len(one_fre_List)) + " 1-frequent-pattern items.\n\n")
	timeWrite.write("================divide===================\n\n")
	return one_fre_List
	
def recursiveFind(one_fre_List, level):
	# 连接和剪枝
	global timeWrite
	global rstWrite
	global supportNumber
	two_fre_candidate = []
	
	# 连接和剪枝，获得候选的二项集
	getCanStart = time.time()
	for i in range(len(one_fre_List) - 1):
		for j in range(i + 1, len(one_fre_List)):
			# 连接
			if one_fre_List[i][1:] == one_fre_List[j][1:] and one_fre_List[i][0] != one_fre_List[j][0]:
				new_tuple = (one_fre_List[i][0], one_fre_List[j][0]) + one_fre_List[i][1:]
				
				# 剪枝
				allIn = True
				for k in range(level):
					temp_tuple = new_tuple[0:k] + new_tuple[k + 1:]
					if temp_tuple not in one_fre_List:
						allIn = False
						break
				if allIn:
					two_fre_candidate.append(new_tuple)
					
	getCanEnd = time.time()
	print(str(getCanEnd - getCanStart) + " seconds to get " + str(len(two_fre_candidate)) + " level " + str(level) + " candidaite items.\n")
	timeWrite.write(str(getCanEnd - getCanStart) + " seconds to get " + str(len(two_fre_candidate)) + " level " + str(level) + " candidaite items.\n\n")

	
	two_fre_List = []
	# 以下代码从候选的结果获得二项集
	getAnsStart = time.time()
	
	itemCount = 0
	for item in two_fre_candidate:
		count = 0
		for paragraph in data:
			if len([num for num in item if num not in paragraph]) == 0:
				count += 1
		if count >= supportNumber:
			two_fre_List.append(item)
	getAnsEnd = time.time()
	
	print(str(getAnsEnd - getAnsStart) + " seconds to get " + str(len(two_fre_List)) + " " + str(level) + "-frequent-pattern items. \n")
	timeWrite.write(str(getAnsEnd - getAnsStart) + " seconds to get " + str(len(two_fre_List)) + " " + str(level) + "-frequent-pattern items. \n\n")
	
	# 如果发现了多于1个level + 1项集，就进行下一轮拼接
	if len(two_fre_List) >= 2:
		for item in two_fre_List:
			for num in item:
				rstWrite.write(str(num) + ", ")
			rstWrite.write("\n")
		rstWrite.write("\n")
		print("================divide===================\n")
		timeWrite.write("================divide===================\n")
		recursiveFind(two_fre_List, level + 1)
	else:
		return


if __name__ == "__main__":
	filename = sys.argv[1]

	global timeWrite
	global rstWrite

	# 这里的timeWrite是将运行时间写入文件
	# rstWrite是将运行的结果写入文件
	timeWrite = open(sys.argv[2], 'w')
	rstWrite = open(sys.argv[3], 'w')
	
	# 这部分代码将数据从文件中读入
	fileReadStart = time.time()
	fileRead = open(filename, 'r')
	linesList = fileRead.readlines()
	linesList = [line.strip().decode('utf8') for line in linesList if line.strip()]
	paragrapgCount = len(linesList)
	print("the sum of paragrapgs is: " + str(paragrapgCount) + "\n")
	for paragraph in linesList:
		numberList = paragraph.split(" ")
		numberList = [int(num) for num in numberList if num and int(num) != 0]
		data.append(numberList)
	fileReadEnd = time.time()
	print(str(fileReadEnd - fileReadStart) + " seconds to get the data.\n")
	timeWrite.write(str(fileReadEnd - fileReadStart) + " seconds to get the data.\n\n")
	
	# 获得一维频繁项集
	one_fre_List = getOneFrePat()
	for item in one_fre_List:
		for num in item:
			rstWrite.write(str(num) + ", ")
		rstWrite.write("\n")
	rstWrite.write("\n")
	
	#循环连接、剪枝
	recursiveFind(one_fre_List, 2)
	
	
	
	
	
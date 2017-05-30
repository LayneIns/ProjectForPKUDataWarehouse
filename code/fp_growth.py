# -*- coding: utf-8 -*-
import re
import sys, os
import time
#设置递归深度
sys.setrecursionlimit(20000)

global paragrapgCount
global data
data = []
global newdata
newdata = []
global tableHead
tableHead = dict()
global table
table = []
global supportNumber
supportNumber = 0
global timeWrite
global rstWrite


# node是FP-tree的结点，有成员变量：
# value: 当前结点代表的值
# child: 子节点，是一个字典
# supportNum: 当前结点的计数
# mark: 用于建立table header的辅助变量
# parent: 当前节点的父节点
class node:
	def __init__(self, name):
		self.value = name
		self.child = dict()
		self.supportNum = 0
		self.mark = 0

	def addParent(self, parent):
		self.parent = parent

	def addChild(self, newnode, times):
		if newnode.value not in self.child.keys():
			self.child[newnode.value] = newnode
		self.child[newnode.value].supportNum += times 
		return self.child[newnode.value]


# getOneFrePat()函数的作用是：遍历一遍原始数据集，
# 找到所有的一维频繁项集
# 三个返回值的含义是：
# one_fre_List: 一维频繁项集的有序列表
# staDict: 一维频繁项集的字典索引，staDict[i]就是对应的次数‘
# tempList: 元组(i, staDict[i])组成的列表
def getOneFrePat():
	global supportNumber
	global timeWrite
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
	timeWrite.write("The minimum support number is: " + str(supportNumber) + "\n\n")

	getOneFreStart = time.time()
	for paragraph in data:
		maxNumber = maxNumber if maxNumber > max(paragraph) else max(paragraph)
		minNumber = minNumber if minNumber < min(paragraph) else min(paragraph)
	
	tempList = []

	# 统计各个项的数量以获得一维频繁项集
	oneStaticList = [0] * (maxNumber + 1)
	for paragraph in data:
		for number in paragraph:
			oneStaticList[number] += 1
	
	one_fre_List = []
	staDict = dict()
	for i in range(1, len(oneStaticList)):
		if oneStaticList[i] >= supportNumber:
			one_fre_List.append(i)
			staDict[i] = oneStaticList[i]
			
	getOneFreEnd = time.time()
	print(str(getOneFreEnd - getOneFreStart) + " seconds to get " + str(len(one_fre_List)) + " 1-frequent-pattern items.\n")
	print("================divide===================\n")
	timeWrite.write(str(getOneFreEnd - getOneFreStart) + " seconds to get " + str(len(one_fre_List)) + " 1-frequent-pattern items.\n\n")
	timeWrite.write("================divide===================\n\n")

	for i in range(1, maxNumber + 1):
		if oneStaticList[i] >= supportNumber:
			tempList.append((i, oneStaticList[i]))

	return one_fre_List, staDict, tempList

# 对newdata建立FP-tree，这里需要遍历一次newdata
def buildFPTree(root):
	print("building the tree...")
	buildingStart = time.time()
	for paragraph in newdata:
		parent = root
		for num in paragraph:
			onenode = node(num)
			onenode = parent.addChild(onenode, 1)
			onenode.addParent(parent)
			parent = onenode

			# 以下是为了建立table header，为了避免重复将节点添加进
			# table header的列表中，用结点的mark变量标识其是否已经
			# 在列表中
			if num in tableHead.keys():
				if onenode.mark == 1:
					continue
				else:
					tableHead[num].append(onenode)
					onenode.mark = 1
			else:
				tableHead[num] = [onenode]
				onenode.mark = 1

	buildingEnd = time.time()
	print(str(buildingEnd - buildingStart) + " seconds to build the tree.\n")
	timeWrite.write(str(buildingEnd - buildingStart) + " seconds to build the tree.\n\n")
	print("Building over.\n")
	return

# 建立子数据的条件子树，各个变量的含义和上面的buildFPTree()一样
def sub_building(root, newsubdata):
	subTableHead = dict()     
	
	for paragraph in newsubdata:
		parent = root
		for num in paragraph:
			onenode = node(num[0])
			onenode = parent.addChild(onenode, num[1])
			onenode.addParent(parent)
			parent = onenode

			if num[0] in subTableHead.keys():
				if onenode.mark == 1:
					continue
				else:
					subTableHead[num[0]].append(onenode)
					onenode.mark = 1
			else:
				subTableHead[num[0]] = [onenode]
				onenode.mark = 1

	return subTableHead

# 构建子数据和子table，tableheader
# 这部分的逻辑和建立FP-Tree树的过程相似
def buildSubFPTree(subdata, frePat):
	if len(frePat) >= 6:
		return
	global supportNumber
	global rstWrite
	for item in frePat:
		rstWrite.write(str(item) + ",")
	rstWrite.write("\n")
	maxNumber = 0
	minNumber = 1 << 20
	for item in subdata:
		for num in item:
			maxNumber = maxNumber if maxNumber > num[0] else num[0]
			minNumber = minNumber if minNumber < num[0] else num[0]
	
	oneStaticList = [0] * (maxNumber + 1)

	for item in subdata:
		for i in range(len(item) - 1):
			oneStaticList[item[i][0]] += item[i][1]

	# 计数
	newsubdata = []
	for item in subdata:
		newitem = []
		for i in range(len(item) - 1):
			if oneStaticList[item[i][0]] >= supportNumber:
				newitem.append(item[i])
		if len(newitem) > 0:
			newsubdata.append(newitem)

	# 如果发现新的子数据已经没有项了就直接返回
	if len(newsubdata) == 0:
		return

	subTable = []
	for i in range(len(oneStaticList)):
		if oneStaticList[i] >= supportNumber:
			subTable.append((i, oneStaticList[i]))

	# 如果发现在新的table中没有数据了也返回
	if len(subTable) == 0:
		return

	subTable = sorted(subTable, key = lambda d: d[1])

	root = node(-1)
	subTableHead = sub_building(root, newsubdata)
	
	# 这部分是为了从子树中获取出对应的子数据
	for i in range(len(subTable)):
		subsubdata = []
		subsubTableChain = subTableHead[subTable[i][0]]
		for onenode in subsubTableChain:
			tempNodeChain = []
			x = onenode
			minMark = x.supportNum

			while x.value != -1:
				y = minMark if minMark <= x.supportNum else x.supportNum
				tempNodeChain.append((x.value, y))
				x = x.parent
			tempNodeChain.reverse()
			subsubdata.append(tempNodeChain)
		newfrePat = []
		newfrePat = [num for num in frePat]
		newfrePat.append(subTable[i][0])
		buildSubFPTree(subsubdata, newfrePat)



if __name__ == "__main__":
	filename = sys.argv[1]
	global timeWrite
	global rstWrite

	# 这里的timeWrite是将运行时间写入文件
	# rstWrite是将运行的结果写入文件
	timeWrite = open(sys.argv[2], 'w')
	rstWrite = open(sys.argv[3], 'w')
	
	# 接下来的代码是为了读入数据并将其转化为python的list
	fileReadStart = time.time()
	fileRead = open(filename, 'r')
	linesList = fileRead.readlines()
	linesList = [line.strip().decode('utf8') for line in linesList if line.strip()]
	paragrapgCount = len(linesList)

	for paragraph in linesList:
		numberList = paragraph.split(" ")
		numberList = [int(num) for num in numberList if num and int(num) != 0]
		data.append(numberList)
	fileReadEnd = time.time()
	
	print(str(fileReadEnd - fileReadStart) + " seconds to get the data.\n")
	print("the sum of paragrapgs is: " + str(paragrapgCount) + "\n")

	timeWrite.write("the sum of paragrapgs is: " + str(paragrapgCount) + "\n\n")
	timeWrite.write(str(fileReadEnd - fileReadStart) + " seconds to get the data.\n\n")

	# 获得一维频繁项集，三个变量的意义见函数的注释
	one_fre_List, staDict, table = getOneFrePat()

	# 这部分将数据中的非频繁项删除，剩下频繁项组成newdata
	for item in data:
		newItem = []
		for num in item:
			if num in one_fre_List:
				newItem.append(num)
		if len(newItem) != 0:
			newItem = sorted(newItem, key = lambda d: staDict[d], reverse=True)
			newdata.append(newItem)

	# table中的是一维频繁项集，(i, staDict[i])组成的列表
	# 所以为了能从表的底端开始，要进行排序
	table = sorted(table, key = lambda d:d[1])

	# 建立根节点，然后根据newdata建立FP-tree
	rootnode = node(-1)
	rootnode.supportNum = 0
	buildFPTree(rootnode)

	# 从table表中计数最小的项开始递归挖掘频繁项集
	miningStart = time.time()
	for i in range(0, len(table)):
		subdata = []	# 条件子树
		subTableChain = tableHead[table[i][0]]
		# 根据tableHeader中的记录来获取以当前值为基础的条件子树
		sys.stdout.write(' ' * 6 + '\r')
		sys.stdout.flush()
		sys.stdout.write(str(i) + '\r')
		sys.stdout.flush()
		
		for onenode in subTableChain:
			tempNodeChain = []
			x = onenode
			minMark = x.supportNum
			# 反向寻找到根节点，之后再逆转
			while x.value != -1:
				y = minMark if minMark <= x.supportNum else x.supportNum
				tempNodeChain.append((x.value, y))
				x = x.parent
			tempNodeChain.reverse()
			subdata.append(tempNodeChain)

		# 递归挖掘条件子树
		buildSubFPTree(subdata, [table[i][0]])
		rstWrite.write("\n")

	miningEnd = time.time()
	print(str(miningEnd - miningStart) + " seconds to get the frequent items.\n\n")
	timeWrite.write(str(miningEnd - miningStart) + " seconds to get the frequent items.\n\n")
		
	timeWrite.close()
	rstWrite.close()
	 


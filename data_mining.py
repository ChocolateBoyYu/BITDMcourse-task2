#Data Mining Homework
#By Changyong Yu   2120151056
#4th July

import itertools
 
support_set = {}

#编辑原始数据，第一列代表survive（0:no, 1:yes），第二列为船舱等级（1级最高），第三列为性别，第四列为上船港口（C, Q, S）
def loadData(path):
	data = []
	fr = open(path)
	for line in fr.readlines():
		lineArr = line.strip().split(',')
		data.append([(lineArr[0]), (lineArr[1]+' PClass'),(lineArr[2]),(lineArr[3]+' Port')])
	return  data
 
 #获取整个数据库中的一阶元素
def createC1(dataSet):
     C1 = set([])
     for item in dataSet:
         C1 = C1.union(set(item))
     return [frozenset([i]) for i in C1]
 
 #输入数据库（dataset）和由第K-1层数据融合后得到的第K层数据集（Ck），
 #用定义的最小支持度（minSupport=0.1)对 Ck 过滤，得到第k层剩下的数据集合（Lk）
def getLk(dataset, Ck, minSupport):
     global support_set
     Lk = {}
     #计算Ck中每个元素在数据库中出现次数
     for item in dataset:
         for Ci in Ck:
             if Ci.issubset(item):
                 if not Ci in Lk:
                     Lk[Ci] = 1
                 else:
                     Lk[Ci] += 1
     #用最小支持度过滤
     Lk_return = []
     for Li in Lk:
         support_Li = Lk[Li] / float(len(dataSet))
         if support_Li >= minSupport:
             Lk_return.append(Li)
             support_set[Li] = support_Li
             print(Li)
             print('support:'+str(support_set[Li]))
     return Lk_return
 
#将经过支持度过滤后的第K层数据集合（Lk）融合
#得到第k+1层原始数据Ck1
def genLk1(Lk):
     Ck1 = []
     for i in range(len(Lk) - 1):
         for j in range(i + 1, len(Lk)):
             if sorted(list(Lk[i]))[0:-1] == sorted(list(Lk[j]))[0:-1]:
                 Ck1.append(Lk[i] | Lk[j])
     return Ck1
 
#遍历所有二阶及以上的频繁项集合
def genItem(freqSet, support_set):
     print('*******************去除冗余规则******************')
     print('**************输出关联规则及其置信度**************')
     print('*************用Lift指标对规则进行评价*************')
     for i in range(1, len(freqSet)):
         for freItem in freqSet[i]:
             genRule(freItem)
 
#输入一个频繁项，根据“置信度”生成规则
#采用了递归，对规则树进行剪枝，并用Lift指标进行评价
def genRule(Item, minConf=0.75):
     if len(Item) >= 2:
         for element in itertools.combinations(list(Item), 1):
             if support_set[Item] / float(support_set[Item - frozenset(element)]) >= minConf:
                 print (str([Item - frozenset(element)]) + "————>" + str(element))
                 print ('confidence:',support_set[Item] / float(support_set[Item - frozenset(element)]))
                 print ('lift:', support_set[Item] / float(support_set[Item - frozenset(element)])/float(support_set[frozenset(element)]))
                 genRule(Item - frozenset(element))

if __name__ == '__main__':
     dataSet = loadData('data.txt')
     result_list = []
     Ck = createC1(dataSet)
     #生成频繁项集合，并输出其支持度
     print('**************输出频繁项集及其支持度**************')
     while True:
         Lk = getLk(dataSet, Ck, 0.1)
         if not Lk:
             break
         result_list.append(Lk)
         Ck = genLk1(Lk)
         if not Ck:
             break
     #输出关联规则及其置信度，并用Lift标准进行评价
     genItem(result_list, support_set)
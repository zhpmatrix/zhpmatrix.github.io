---
layout: post
title: "[ML]KNN实现过程中的编程复盘"
excerpt: "这篇博客讨论了KNN实现过程中涉及到的排序和查找，TopN问题，词频统计等非常经典的基础问题，同时引入了heapq和Counter两个模块。"
date: 2017-09-30 16:46:00
mathjax: true
---

这篇博客是在KNN实现之后，对实现过程中用到的知识的一些总结，这些知识非常基础且重要，但是竟然同时出现在KNN的实现过程中，比较有意思。

### 排序

#### argsort()函数

在ML模型的实现中，经常遇到需要根据某值排序，获取该值对应索引，最后根据该索引取另一个数据。

    x = np.array([2,1,3])

    np.argsort(x)#默认升序排列

得到: array([1,0,2])，降序的实现，

    np.argsort(-x)

利用索引排序数组，

    x[np.argsort(-x)]


#### sort()函数

sort()是list的函数，list.sort()会改变list中值的顺序，此处大坑！

    a = [2,1,3]
    a.sort()

#### sorted()函数

如果不想改变list中值的顺序，可以使用sorted，

    a = [2,1,3]
    sorted(a)

sorted是一个很丰富的函数，其声明如下:

    sorted(iterable, cmp, key, reverse)

在KNN的实现中，最后一步根据K个样本的label值统计出现次数最多的label，代码如下：

    print(sorted(label_dict, key=lambda x:label_dict[x])[-1])

其中label_dict是字典。看另外一个例子：

    data = [('sara', 80), ('david', 90), ('mary', 90), ('lily', 95)]

    sorted(data, key = lambda data:data[0])#按照元组的第一个元素排序

    sorted(data, key = lambda data:data[1])#按照元组的第二个元素排序

此外也可以结合cmp和reverse进行排序，如下：

    sorted(data,reverse=True)

其中关于cmp的用法也相对灵活，此处不谈。 

### TopN问题

#### 基于heapq的实现

对列表操作：

    import heapq
    
    data = [2,3,8,2,1]
    N = 3
    lData = heapq.nlargest(N, data)
    sData = heapq.nsmallest(N, data)


对字典操作：

    import heapq
    dictData = {'a':1, 'b':2, 'c':3}
    N = 2
    lData = heapq.nlargest(N, dictData.values())#得到k, v需要两个for循环实现
    sData = heapq.nsmallest(N, dictData.keys())#得到k, v只需要一个for循环实现

### 元素统计

这个需求同样出现在KNN中，测试样本的类别由K个最近邻决定，这就需要对K个近邻的标签进行统计。

第一种：

    data = [1,2,2,3,3,3,3,5,3]
    _data = set(data)
    for item in _data:
        print(data.count(item))

第二种:

    from collections import Counter
    data = [1,2,2,3,3,3,3,5,3]
    _dict = Counter(data)


总结：这篇博客是基于KNN的实现过程中的总结，涉及排序和查找，TopN问题，词频统计等，博客列举问题在面试中也是屡见不鲜，将问题规模推广到大数据场景下，上述问题需要更具深度的思考。

补充一段词频统计的代码（在决策树的实现中，当确定叶子节点的类别时需要由叶子节点样本投票得出）:

    import operator
    def majorityCnt(classList):
        classCount = {}
        for vote in classList:
            if vote not in classCount.keys():
                classCount[vote] = 0
            classCount[vote] += 1
        sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
        return sortedClassCount[0][0]

注意：在Python3.7版本中，使用classCount.items();但是在Python2.7版本中，则需要classCount.iteritems()。







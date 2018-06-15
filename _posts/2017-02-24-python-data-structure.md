---
layout: post
title: "[Python]深入理解数据结构"
excerpt: "回顾了关于copy的坑，常用数据结构的时空复杂度，同时结合CS231n的视觉课程做了python基础的review。"
date: 2017-02-24 12:00:00
---

python有四种内置数据结构和其他高级数据结构，其中四种内置数据结构是列表(list), 元组(tuple), 字典(dict), 集合(set)。

**重要声明：一定要要注意deep copy和shallow copy!此处是大坑！**

list的内部实现是动态数组，存在的问题是当长度增加的时候，需要开辟新的空间，同时进行容器元素的复制移动。当然，在插入和删除元素的时候，被插入和删除元素后继元素也要进行移动。故当需要在容器头部和尾部添加删除元素的时候，可以考虑使用**collections.deque**来替代，据说deque的底层实现逻辑就是list。

比如，几个典型的时间复杂度：len是O(1),min和max是O(n),sort是O(nlogn),delete是O(n)等。

deque是双端队列，内部实现是双向链表。注意是数组链表而不是对象链表，这样可以有更高的效率。显然，双端队列在两端进行操作的时候，具有较高的效率，而对中间元素进行操作，效率较低。

比如，几个典型的时间复杂度：append,appendleft,pop,popleft都是O(1),rotate和remove都是   O(n)等。注意，deque是线程安全的，可以同时从deque集合的左边和右边进行操作而不会有影响。

set的几个操作的时间复杂度通常与集合的长度有关。举个例子，差集操作(set1 - set2), 则时间复杂度为O(len(set1))。set的底层实现和dict相同，都是hash，实现set的方式称为hash set，实现dict的方式称为hash map/table。主要的不同在于hash函数操作的对象，对于dict，hash函数操作的对象为key；对于set，hash函数操作的对象为元素自身。

dict是字典，hash结构的时间复杂度通常是O(1)。和list一样，字典存储的也是对象的引用。

下述内容是针对李飞飞教授CS231n给出的Python教程查漏补缺的内容：

---

##### 0.字符串操作

s.capitalize(),s.upper(),s.rjust(),s.center(),s.replace(src,dst),s.strip()

##### 1.contaienr(复合数据结构)

list:   list.append(),**list.pop()**

dict:   dict.get(key,default value,(**"N/A"**)),del dict[key]

tuple:  tuple可以在dict中当做key，但是list不行！

##### 2.numpy的计算

数组的加减乘除(**elementwise product**)：np.add(),np.subtract(),np.multiply(),np.divide()   

矩阵乘法：np.dot(x,y)

**广播机制：把一个向量加到矩阵的每一行。**

##### 3.scipy图像操作

**图像操作**：from scipy.misc import imread,imsave,imresize

**MATLAB文件读取**：scipy.io.loadmat,scipy.io.savemat

**计算集合中所有两点之间距离**：scipy.spatial.distance.pdist

##### 4.matplotlib

标准绘图代码：

    import numpy as np
    import matplotlib.pyplot as plt
    x = np.**arange**(0,3*np.pi,0.1)#支持步长为小数
    y_sin=np.sin(x)
    y_cos=np.cos(x)

    plt.plot(x,y_sin)
    plt.plot(x,y_cos)
    plt.xlabel('x axis label')
    plt.ylabel('y axis label')
    plt.title('sin and cos')
    plt.legend(['sin','cos'])
    plt.show()

绘制多个图像：subplot()

##### 5.pandas占坑(DMer必须要提一下呀)

---


参考：

1.[python中的高级数据结构](http://blog.jobbole.com/65218/)

2.[org给出的内置数据结构时间复杂度](https://wiki.python.org/moin/TimeComplexity)

3.[OrderedDict](https://docs.python.org/3/library/collections.html#collections.OrderedDict)

4.[CS231n的Python教程](https://zhuanlan.zhihu.com/p/20878530?refer=intelligentunit)

李飞飞教授的课程，主要用于CV，所以弱化了pandas用于文本数据处理，强调了scipy用于图像处理。
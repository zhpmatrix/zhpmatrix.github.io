---
layout: post
title: "[Python]编程复盘"
excerpt: "BP算法实现后的想法"
date: 2016-12-04 13:01:00
mathjax: true
---
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

这是利用Python做的第二个实践，第一个实践是2015年暑假在宁波智能制造产业研究院做Intern的时候写过一个八叉树的结构。问题描述如下：

![P](http://ww4.sinaimg.cn/mw690/aba7d18bjw1faeoh2kq22j20lp0kedl9.jpg)

---

代码基于Python，利用numpy做计算结构，matplotlib做绘图包，**自己实现BP算法**。根据问题描述，拟构建一个1xNx1的神经网络结构。在调研之后，基于Python的实现有keras，[pybrain](http://nezha.github.io/%E7%A7%91%E5%AD%A6%E8%AE%A1%E7%AE%97/pybrain%E5%88%9D%E5%85%A5%E9%97%A8)等，但是要求要自己Coding出BP模块。

为了充分利用numpy，将问题向量化，然后采用向量编程的想法来做，简单（统一的数据结构）且高效（numpy的执行效率）。很自然的，在Coding中选择的是Batch Learning方式，很多基于Matlab做的同学用的是Online Learning的方式。复盘之后的几个问题如下（是的，这篇复盘尽量不讨论关于BP的问题，仅仅是Coding问题）。

*1.* numpy和matplotlib的极简使用？

_list和array之间的关系_。例如，list和array之间的互相转换。这个问题中，需要认识到**ndarray就是matrix**，在C语言课程中，提到过的多维数组就是这个概念。很自然的，接下来就需要知道matrix相关的一些操作，包括行列操作,转置操作，范数操作等。在基本操作的基础上定义运算，如点积。关于运算，需要知道操作对象的属性，同样需要清楚针对对象中元素的运算过程，这是numpy的简单高效之处的体现之一。

_关于array的合并与拆分_。在给定问题中，样本的输入是list结构，显然任务中存在着这样的需求，建立input和target的KV关系，因为这涉及到sampling操作。利用vstack合并操作可以实现我的目的，在上段内容中提到的行列操作则可以服务于split操作。

_shuffle的使用_。在给定问题中，随机模块的使用需求有两个地方。第一个地方在于原来input是递增序列，在进行交叉集划分的时候需要shuffle。第二个地方在于同一个model，交叉验证的时候要对输入样本shuffle操作。通常算法中的shuffle操作可以从概率算法的角度给出一个解释，而结合神经网络模型阿狸说，每次shuffle都有自己的意义，此处不做讨论。

_ndarray与matrix的关系_。在一些必要的时候，如果想利用numpy中的实现，特别是需要指定axis的时候，需要将我的数据转换为matrix格式，也就是np.mat()函数。利用在我的数据处理中，归一化的操作，利用MinMax操作，需要找到min和max值。

_关于绘图_。对于绘图做了一个简单的封装，如下：

    def show(dat,xlabel,ylabel,title):
    ''' Showing one line'''
        plt.figure
        plt.plot(dat)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()
        plt.close()

    def showLines(dat1,label1,dat2,label2,xlabel,ylabel,title):
    ''' Showing two lines'''
        plt.figure
        plt.plot(dat1, label=label1)
        plt.plot(dat2,label=label2)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend()
        plt.show()
        plt.close()

在给定任务中，需要绘制三张图片，最简单的绘图方式应该就是这样了。

*2.* 科学计算任务下，接口参数如何定义？

在给出理想的一个相对较粗的代码框架之前，来看几个细节。

一.关于*\*args*和*\*\*kwargs*

二者都是可变参数，\*args（arguments）表示任何多个**无名参数**，结构为tuple;

\*\*kwargs(key words arguments)表示任意多个**关键字参数**，结构为dict;

举个栗子：

    def foo(*args,**kwargs):
        print 'args=',args
        print 'kwargs=',kwargs
    if __name__ == '__main__':
        foo(1,2,3,a = 1,b = 2)
结果为：

    args=(1,2,3)
    kwargs={'a':1,'b':2}

---

吐槽时刻，读者可略过...

Python中有这样的一个用法，将函数作为另一个函数的参数传入并调用。就是这样的：

    def func_a(*args):
        return args
    def func_b(func,*args):
        print(func(*args))
    if __name__ == '__main__':
        func_b(func_a,1,2,3)

与其那样，不如这样：

    def func_a(*args):
        return args
    def func_b(*args):
        print(func_a(*args))
    if __name__ == '__main__':
        func_b(1,2,3)
如果真的是这样，上面还有什么意义呢？这样的好处是显而易见的，同样的输入参数，调用不同的函数结果不同(说了句废话...)。

二.函数参数传递

举两个栗子，我就可以什么也不用说了。

    def func(x,y = 2,*p,**q):
        print 'x=',x
        print 'y=',y
        print 'p=',p
        print 'q=',q
    if __name__ == '__main__':
        func(20,10,1,2,3,a = 4,b = 5)

输出结果为：

    x=20
    y=10
    p=(1,2,3)
    q={'a':4,'b':5}

第二个栗子：

    def func(x,y = 2)
        print 'x=',x
        print 'y=',y
    if __name__ = '__main__':
        func(y = 10,x = 4)

输出结果为：

    x=4
    y=10

所以，或许在传递参数的时候采用**参数名加参数值**的方式比较好，代码的可读性增强了。但是，并不意味着在函数定义的时候给定默认参数值不是一种好的方式，可能有的参数被码农同学经常使用的概率很小，但是作为程序友好，还是开放给码农同学。此外，函数实现之前的参数校验部分也是节省了一部分工作，比如参数类型和参数是否为空校验。

借此安利两个小习惯(不管你信不信，这两个习惯会让你的效率大大增加，你想不到的增速)：

*1.* 读代码前，弄明白变量的意义。

*2.* 读数学证明前，弄明白notation的意义。

下边给出一个比较粗的代码框架（重在结构和参数）：

    class NeuralNetwork:
        def __init__(self,layers,activation='tanh'):
            if activation == 'logistic':
                self.activation = self.__logistic
            elif activation == 'tanh':
                self.activation = self.__tanh
            Initialize weights and biases.
        def __logistic(x):
            Code here
        def __tanh(x):
            Code here
        def fit(self,x,y,learning_rate=0.2,epoches = 1000):
            Code here
        def predict(self,x):
            Code here

比如说，这是一种可能的调用方式：

    import numpy as np
    from BP import NeuralNetwork
    nn = NeuralNetwork(layers=[2,4,1],activation='tanh')
    x = np.array([[1,2],[3,2],[5,2]])
    y = np.array([1,0,1,1])
    nn.fit(x,y,learning_rate=0.1,epoches=400)
    test = np.array([[3,4],[2,1],[5,4]])
    for i in test:
        print(i,nn.predict(i))

在NeuralNetwork的定义中，将各种类型的激活函数定义为私有函数，因为激活函数只在训练阶段被使用。整理的过程分为初始化，训练或者成为拟合，预测三个过程。实际上learning_rate和epoches两个参数也可以放在初始化参数列表中，也就是类的构造函数中。但是如果放在构造函数中，实例化参数列表就会变得冗长。不管在哪个地方，这两个参数总要显式传入函数。

总结：神经网络的拟合效果好坏依赖于**tuning**，对于强经验依赖，没有严格数学理论支撑的参数似乎不是太好，期待有人能够从理论上给参数一个合理的解释。虽然这样，但是从大家把神经网络用于实际问题的反响来看，它是work的，因此并不能说它不漂亮。

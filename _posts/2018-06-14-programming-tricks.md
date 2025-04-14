---
layout: post
title: "回调函数，线程安全，Monkey Patch和try/except使用"
tags: [Python]
excerpt: "读了一份syncbn的代码，博文是对一些基本概念的回顾。"
date: 2018-06-14 18:43:00
mathjax: true
---

### 回调函数

与回调函数相关的两个概念是应用编程和系统编程，关系如下。

![callback function](http://s5.51cto.com/wyfs02/M00/8C/35/wKiom1hk_maDzDp7AACLDhIdbUo502.jpg)

应用编程，显然要去解决应用层的问题。系统编程，主要实现一些系统功能，或者说更底层的一些功能。在应用编程的时候，常常需要调用一些系统功能，典型的库函数等，那么调用逻辑就会如上图所示。通常的逻辑是Main Program调用Library function，然后Library function返回结果给Main program，这种情况下，也是常见的只传递参数且该参数为非函数指针等类型。

其实，函数也可以作为参数传递，比如典型的函数指针。那么，我们希望Library function根据传递的函数返回不同的结果。如何实现？最简单的方式应该就是直接调用传递的函数，将该函数称为回调函数，将值返回。但是由于调用的是Library function，可以有更加复杂的函数定义，因此，

对Callback function，借助于Library function，代码和功能复用，丰富了回调函数功能；当然可以不调用Library function直接将想要实现的功能放入Callback function，优点是减少了上下文切换，缺点是没有有效利用系统代码。

对Library function，通过Callback function的调用，丰富了Library function的功能，使得库函数的实现更加的灵活可用。

这么好的东西，看两段代码。

    def pytorch():
        print('PyTorch!')

    def caffe2():
        print('Caffe2!')

    def b(func):
        print('Which framework is the best?')
        func()
        print('Done!')

    if __name__ == '__main__':
        b(pytorch)
        b(caffe2)

在这段代码中，Main program(main)调用了两次Library function(b)，对应的两个回调函数分别是pytorch和caffe2，在b中根据传入的函数参数分别调用对应的回调函数。

另一段是关于多进程的代码。

    from multiprocessing import Pool
    def show(val):
        print(val)
        print('Done!')

    def func(val):
        return val

    if __name__ == '__main__':
        p = Pool()
        num = 10
        for i in range(num):
            p.apply_async(func, args=(i,), callback=show)
        p.close()
        p.join()

这里的回调函数是show，库函数func会在执行结束后，将返回值作为回调函数的参数传递过去，调用回调函数。

理解回调函数，可以从多个方面出发。

### 线程安全

Python中有可变对象和不可变对象，可变对象例如list，dict，set，不可变对象例如int，string，float，tuple。可变和不可变的区别在于对象改变的时候内存是否发生拷贝，不可变对象需要内存拷贝。这里有一个有趣的问题是，其他语言比如C/C++，在参数传递的时候需要特殊的标记是参数传递还是引用传递，但是Python中都是引用传递，但是因为对象分为可变和不可变，所以实际上参数传递功能类似C/C++。

通常认为，针对可变对象的多线程操作是线程不安全的，但是Queue是线程安全的。从内存角度，可能的原因之一是内存的脏读和误读。从定义上来讲，线程是否安全需要针对具体操作，放在多线程环境下讨论。

### Monkey Patch

Python中属性(变量和函数)在运行时动态替换的一种方法，具体操作，直接赋值。这里有一个使用的[例子](https://github.com/vacancy/Synchronized-BatchNorm-PyTorch)，不过可能不太直观。

### try...except（as/else/finally子句）

日常基本不使用，给出一个代码段，用来捕获异常。

    try:
        a = int(input('enter a: '))
        b = int(input('enter b: '))
        print(a/b)
    except Exception as err:
        print(err)

上述代码中通常会发生两个异常，第一个是int强制转换，报ValueError异常；第二个是ZeroDivisionError。代码的执行意图是不管发生什么异常，都捕获。这里有一个使用的[issues](https://github.com/vacancy/Synchronized-BatchNorm-PyTorch/issues/3#issuecomment-385880518)



参考：

1.[Python中的可变对象和不可变对象](https://www.jianshu.com/p/c5582e23b26c)

2.[知乎中关于线程安全的讨论](https://www.zhihu.com/topic/19826094/hot)

关于线程安全的问题，感觉问题并没有说的很清楚，实际上，在日常使用中，几乎没有遇到线程安全的一些问题，可能写的多线程或者进程代码都比较简单吧。

3.[Monkey Path](https://blog.csdn.net/fly910905/article/details/77152110)

这篇文章从名字来源，代码，优缺点分析方面都写的很清楚。

4.[try...except的使用](http://blog.sciencenet.cn/blog-3031432-1059523.html)

科学网的一篇总结，写的很棒。













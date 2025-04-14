---
layout: post
title: "用进程池Pool进行代码加速"
tags: [Python]
excerpt: "给出了不使用成熟大框架spark和hadoop的前提下，如何发挥集群算力的解决方案的想法，分布式进程进行任务分配+单机多核多进程+单核协程(仿多线程），实际上比赛代码加速还是多进程好使，其他的技术可能只是讨论讨论"
date: 2017-11-04 22:22:00
mathjax: true
---

商场中精确定位商铺所在位置比赛中遇到的一个问题是，测试集样本有483931个，由于建模过程是建立97个商场模型，故需要针对每个测试样本，先判断样本所属商场，然后调用对应模型进行预测。

很显然，这样的执行效率很低，需要遍历并预测每一个样本。所以，可以先按照每个样本所属的商场分组，然后对每个分组的样本批量预测。这样虽然不需要一个个预测，但是为了完成分组任务，仍然需要遍历每一个样本，由于遍历的过程是独立的，故这个任务可以并行执行。

当然483931个样本，内存能不能吃下，仍然是一个大的问题。

为了解决上述所描述的**计算慢，存储要求高**的两个问题，一种可能的思路是对数据分段，并行完成计算，这样，可以同时解决这两个问题。

假设按照60000个样本作为一个任务，则可以分为9个任务执行，当然可以这样做。手动开启9个进程并发执行这些任务。

```python

from optparse import OptionParser
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-s','--start',dest='start',default='0')
    parser.add_option('-e','--end',dest='end',default='60000')
    (options, args) = parser.parse_args(sys.argv)
    s = int(options.start)
    e = int(options.end)
    do(s,e)

```

运行脚本如下:

    python3 task.py -s 60000 -e 120000

上述脚本执行的是60000-120000这个任务，其他任务类似。但是这种方式很繁琐，要手动开启9个任务，当然可以通过写shell脚本来完成这个任务，但是要写一个shell，同样增加了工作量，尤其是对shell脚本不熟悉的同学，比如说我。

其实**上述是最原始的多进程方案**。一定有更优雅的解决方案是不是？在给出更优雅的解决方案前，回顾一下python中多线程和多进程的区别，为啥很多人说python中的多线程很鸡肋？

鸡肋的关键在于：**python的多线程无法利用cpu的多个核心**。

啥？_多线程竟然不能使用多个核心，那还有个毛用？_ 

python的官方解释器是Cython，该解释器在执行代码的时候要使用GIL(Global Interpreter Lock)锁。**任何线程执行前，要获得该锁。**到这里就很明白了，因为这个锁是全局的，只有一个，故一把锁不能在同一时刻被两个线程拥有。解释器周期性释放该锁，多个线程分时使用该锁，一个时间只有一个线程拥有该锁，假设每个线程分布在每个核心上，每个时刻只有一个核心被激活。

虽然不能多线程，但是可以多进程使用多核。**因为每个进程可以拥有一个GIL呀**。

使用多进程最原始的方式如上所述，但是当进程非常多的时候，想象一下开200个terminal的场景，管理就成为一个大问题，有一个非常优雅的方式来解决这个问题。

**进程池Pool。**

代码如下：

```python

from multiprocessing import Pool

if __name__ == '__main__':
    p = Pool()
    total_start = 0
    total_end = 483931
    step = 60000
    start = time.time()
    for x in range(0, int(total_end/60000)):
        s = x * 60000
        if x == 7:
            e = s + 63931
        else:
            e = s + 60000
        p.apply_async(do, args=(s, e,))
    p.close()
    p.join()
    print('Done!')

```

其中apply_async是采用异步方式调用任务do，s和e是do的两个参数，含义同上。该API意味着可以连续的提交任务。一般来说，并行任务数和cpu核心数保持一致，这样保证每个核心执行一个任务。当并行任务数大于cpu核心数的时候，由于一个核心执行多个任务，就存在进行切换的开销了。close函数表示不再添加任务，join表示全部子进程执行完毕后执行下一行语句print(这是一个同步操作)。

有了Pool，一行脚本就可以构建任意多个进程，由于进程是独立的，故一个进程挂了，不会影响到别的进程。比起线程来说，一个线程挂了，整个进程就挂了。

感受一把，如下。

![pool](http://wx2.sinaimg.cn/mw690/aba7d18bgy1fl7fhavm0ej20hy0djjsf.jpg)

我的mac是双核四个逻辑核，Pool默认使用四个核心完成任务。蓝色线框中是多进程执行任务的状态。

注意上述是解决进程不返回结果的过程，与之相反的进程返回结果的处理在参考1中给出。关键是正确使用get方法，防止破坏多进程的异步处理状态。此外，进程间的通信在参考2中给出，关键可以使用Queue通信。

下述代码给出了一种返回结构的示例，同时给出了一种新的并行任务执行的方式，map执行。

```python
    
    from multiprocessing import Pool

    def do(data):
        return data

    if __name__ == '__main__':
        data = [1,2,3]
        idata = iter(data)
        p = Pool()
        results = p.map_async(do, idata))
        p.close()
        p.join()
        print(results.get())
        print('Done!')

```

map_async和apply_async的区别在哪里？**传递的参数是否可迭代。**这里和函数式编程的思想保持一致。关于上述代码中get的解释可以参照参考1的具体解释。

[补充: 同步和异步的区别]

```python

import os, time
import multiprocessing

def task(i):
    time.sleep(10)
    return i

if __name__ == '__main__':
    cpu_nums = multiprocessing.cpu_count()
    pool = multiprocessing.Pool()
    results = []
    for i in range(0, cpu_nums):
        result = pool.apply_async(task, args=(i,))
        print(result.get())
        results.append(result)
    pool.close()
    pool.join()
    #for result in results:
    #    print(result.get())

```

分析上述代码，下述代码：

    print(result.get())

会使得并行任务阻塞进行，所谓阻塞进行，就是同步。get会等待当前任务结束，然后才去执行下一个任务。这显然不是自己想要的，如果要任务并行执行，就是将子进程的结果的获取放在全部任务结束的时候进行，如上述代码的最后两行。这里采用一个list结构进行结果整合，其实更fancy的方式是使用map_async来完成。


上述只是谈及了如何发挥多核的优势，在之前的博客中，做了简单的多机分布式计算的尝试。具体细节可以参照这篇[博客](https://zhpmatrix.github.io/2017/02/19/speed-up-distributed/)。



总结：在比赛所需要的加速技巧中，Pool的使用简单又实用。目前还没有遇到多进程通信，进程结果返回，分布式计算的具体问题，故暂时不做深入讨论。在廖雪峰的教程中，提到发挥多核cpu的一个最好的办法是多进程+协程。协程的实现主要基于yield关键字，该关键字提供了一种中断机制。所以，**如果有一个集群，要发挥集群的算力，怎么搞？分布式进程进行任务分配+单机多核多进程+单核协程(仿多线程)**。直觉上，如果要做到这种程度，自己就转spark去了，逃。

参考:

1.[正确使用MultiProcessing的姿势](https://jingsam.github.io/2015/12/31/multiprocessing.html)

2.[进程间通信](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431927781401bb47ccf187b24c3b955157bb12c5882d000)

3.[Python多进程并行编程实践](https://zhuanlan.zhihu.com/p/24960492)

4.[gensim中的操作](https://zhpmatrix.github.io/2017/11/04/speed-up-python/)

源码中精彩多多！

















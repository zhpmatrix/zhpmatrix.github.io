---
layout: post
title: "[C++]shared_ptr"
excerpt: "xgboost中对于智能指针的使用，主要有两个shared_ptr和unique_ptr。这篇文章是对shared_ptr的理解和典型使用场景说明，以读懂xgboost源码中的使用场景为目的。"
date: 2017-01-09 20:49:00
---

shared_ptr采用引用计数，也就是一个对象被多个shared_ptr指向时，shared_ptr的数目会被记录。当一个对象的引用计数变为0的时候，这个对象会被自动删除。对象对应着内存中的一块区域。

在上一篇文章中，谈到unique_ptr时，提及new(malloc)和delete(free)要成对使用。先来读读这段代码：

    int* pInt = new int(10);
    {
        int* pInt_2 = pInt;
        *pInt_2 = 8;
        delete pInt_2;
        pInt_2 = NULL;
    }
    cout << *pInt << endl;

是的，悬挂指针！输出值是个任意数。

    shared_ptr<int> pInt(new int(10));
    {
            shared_ptr<int> pInt_2 = pInt;
            *pInt_2 = 8;
    }
    cout << *pInt << endl;
    

输出值是8。为什么？

第一行代码定义一个share_ptr是pInt,pInt指向内存中某块长度为10个int长度的空间，此时这块空间的引用计数是1。第三行代码，定义一个share_ptr是pInt_2，指向同样的内存空间，引用计数是2。第四行给这块内存空间赋值8。当离开share_ptr的作用于之后，pInt_2自动销毁(都离开作用范围了，生无可恋)。但是由于pInt_2销毁之后，这块内存空间的引用计数是1，不是0！故不能销毁内存空间，故输出值是8。

给出两个典型的应用场景。

第一个是和unique_ptr中讨论的用容器去管理开辟的空间类似，这里用来管理对象。

<script src="https://gist.github.com/zhpmatrix/92da49b7f55b474cb518f0f4d3a2a0b6.js"></script>

第二个是关于类的对象实例化。

<script src="https://gist.github.com/zhpmatrix/ecf62396bba3b9fc97a368c891c31152.js"></script>

在xgboost的单线程命令行版本的代码中(cli_main.cc)，载入测试数据集和训练模型的时候，声明的是shared_ptr指针类型。如下代码所示：

载入训练数据集：

    std::shared_ptr<DMatrix> dtrain(DMatrix::Load(param.train_path, param.silent != 0,param.dsplit == 2));

针对原始数据集，后续会有很多基于原始数据集的变换操作。故采用shared_ptr类型声明，适合。




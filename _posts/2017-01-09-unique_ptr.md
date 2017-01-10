---
layout: post
title: "[C++]unique_ptr"
excerpt: "xgboost中对于智能指针的使用，主要有两个shared_ptr和unique_ptr。这篇文章是对unique_ptr的理解和典型使用场景说明，以读懂xgboost源码中的使用场景为目的。"
date: 2017-01-09 19:31:00
---

unique_ptr是指向某块内存区域的指针，表示对某块内存区域的所有权。关于unique_ptr的讨论围绕资源所有权。

创建unique_ptr:

    unique_ptr<int> pInt(new int(6));

**移动构造**和**移动赋值**(不能进行非移动构造和赋值)：


    unique_ptr<int> pInt(new int(6));
    unique_ptr<int> pInt_2(move(pInt));
    unique_ptr<int> pInt_3 = move(pInt_2);

在C/C++编程中，涉及到内存分配和管理时，要求malloc和free，new和delete成对使用来防止内存泄漏。真实的情况是，有太多的人可能会忘记free和delete，自己有时就会(囧)。

这就催生了unique_ptr的第一个经典使用场景：

    void foo(){
        int* pInt = new int(5);
        throw exception;
        delete p;
    }

上述代码可能是会经常遇到的一种类型，异常发生了，结果没有delete掉资源，虽然确实成对使用了new和delete。**由于指向某块内存区域的unique_ptr创建成功，当离开unique_ptr作用域的时候，资源一定会被自动释放**。于是，可以以这种姿势来写代码：

    void foo(){
        unique_ptr<int> pInt(new int(5));
        throw exception;
    }

既不用担心忘记delete，又不用担心异常发生的时候，资源没有释放。

第二种场景是将所有权返回：

    unique_ptr<int> foo(int size){
        unique_ptr<int> pInt(new int(size));
        return pInt;
    }

第三种场景是将指针保存在容器中：

    vector<unique_ptr<int> > pIntVec;
    unique_ptr<int> pInt(new int(5));
    pIntVec.push_back(move(pInt));

**注意上述代码在将指针放入容器的时候，使用移动操作**。

第四种场景是动态数组的管理：

    unique_ptr<int[]> pInts(new int[2]{4,6});
    p[1] = 8;

第五种场景是自定义析构操作：

<script src="https://gist.github.com/zhpmatrix/853c85b2e2ea2f6179a80b84e1e9e00b.js"></script>

在xgboost的单线程命令行版本的代码中(cli_main.cc)，载入测试数据集和训练模型的时候，声明的是unique_ptr指针类型。如下代码所示：

载入测试数据集：

    std::unique_ptr<DMatrix> dtest(DMatrix::Load(param.test_path,param.silent != 0,param.dsplit = 2));

载入模型(学习器)：

    std::unique_ptr<Learner> learner(Learner::Create({}));


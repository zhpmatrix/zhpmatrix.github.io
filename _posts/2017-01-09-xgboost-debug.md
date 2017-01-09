---
layout: post
title: "[groot]xgboost源码调试"
excerpt: "mac中使用lldb调试器在vim中调试xgboost的c++源代码，其中xgboost为单线程版本"
date: 2017-01-09 13:56:00
---

作为一个VIMer，看到了一些基于VS或者Eclipse搭建的xgboost源码调试环境（其实并不多）。为了调试xgboost再去安装一个VS，似乎没有必要（主要是因为我的mac只剩下3G存储空间）。下面就是自己探索后的详细步骤。

第一步：

在Github中下载xgboost的源代码。

第二步：

修改根目录下的Makefile文件。找到Makefile文件中的这行代码:

    export CFLAGS=  -std=c++0x -Wall -Wno-unknown-pragmas -Iinclude $(ADD_CFLAGS) $(PLUGIN_CFLAGS)

添加参数**'-g'**:

    export CFLAGS=  -std=c++0x -Wall -Wno-unknown-pragmas -Iinclude $(ADD_CFLAGS) $(PLUGIN_CFLAGS)

这个步骤的目的是编译时得到可调式版本，默认安装的时候，没有该参数(如果喜欢汇编语言，此步可以略过)。

第三步：

运行根目录下脚本文件进行安装。

    ./build.sh

第四步：

在该步中，给出一个调试案例。进入demo目录中的binary_classification例子中，调试一个二分类的例子。

**首先要修改mushroom.conf中的训练集和测试集的文件路径。**这个是由于repo文档更新不及时所致。

开始调试：

    lldb ../../xgboost mushroom.conf max_depth=9

main函数入口处打断点：
    
    b main

运行：

    r

进入函数：

    s

下一步：

    n

接下来就可以一步步进行跟踪代码逻辑了。
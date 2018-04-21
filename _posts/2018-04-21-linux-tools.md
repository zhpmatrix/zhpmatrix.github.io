---
layout: post
title: "[Linux]Linux常用工具整理"
excerpt: "系统梳理了自己在日常学习和工作中常用的Linux工具"
date: 2018-04-21 13:28:00
mathjax: true
---

### 编译安装

通常看到的Linux编译安装过程如下：

    ./configure --prefix="install path"

如果不指定--prefix，默认安装路径为/usr/local/lib，/usr/local/bin，/usr/local/etc等。./configure是用来检查系统依赖，例如是否安装编译器CC或者GCC，是否有需要的库文件等。

    make

    make install

make是编译命令，make install是安装命令，其中install并不是make的参数，而是执行Makefile中install后面的语句。回到真实的开源工具xgboost，下载版本为xgboost-0.60，进入文件目录中可以看到文件**CMakeLists.txt**和**Makefile**，Makefile是CMakeLists.txt的产生文件，工具是**cmake**，Makefile文件是**make**的输入。

比如为Caffe添加了一个新的Layer，需要重新make，在make之前要clean；由于是增量make，故不会出现特别长的make时间；

CMakeLists.txt中的内容主要包括：项目名称，头文件目录，环境变量设置，依赖库设置，生成的文件路径等。

**有人描述**：Makefile是用于自动编译和链接的，一个工程有很多文件组成，每一个文件的改变都会导致工程的重新链接，但不是所有文件都需要重新编译，Makefile能够纪录文件的信息，决定在链接的时候需要重新编译哪些文件。在Unix系统下，Makefile是与make命令配合使用的，有了这个Makefile文件，不论我们什么时候修改了源程序当中的什么文件，我们只要执行make命令，我们的编译器都只会去编译和我们修改的文件有关的文件。

从上述描述来看，使用Makefile来实现一种增量编译。如何实现增量？需要全局信息，需要一种能够检测局部更新的工具，而Makefile就是这个工具。

    make -j4

此外，在复现源程序的时候，经常会看到make后添加-j4参数，查看帮助:

    make -h

得到如下信息：

    -j [N], --jobs[=N]        Allow N jobs at once; infinite jobs with no arg.

也就是说该参数用来指定编译时的线程数目，在尚未指定的时候，默认使用尽可能多的线程。

### 压缩和解压缩

压缩命令：

    tar -zcvf file.tar.gz file

参数解释：z是使用工具gzip压缩；c是压缩；v是显示文档名称；f是压缩文件名称；

解压命令：

    tar -zxvf file.tar.gz

参数解释：x是解压缩；

### 创建软理解(快捷方式)

    ln -s path link_path

### 环境变量设置

当用户登录Linux系统的时候，首先读取全局变量的值，然后根据特定用户，读取用户的局部变量的值；

全局变量的配置文件: /etc/profile, /etc/bashrc
局部变量的配置文件: ~/.profile(只执行一次), ~/.bashrc

根据目前使用集群的配置，常用配置文件包括：/etc/profile + ~/.bashrc

配置的两种方式：直接在命令行export和永久配置（全局和当前用户）

配置后：source /etc/profile，保证配置生效；

### Linux Shell脚本编写

在Caffe的使用过程中，常常需要编写Shell脚本，一个完整的使用流程包括：

1.编写Shell脚本


2.赋予可执行权限

    chmod +x test.sh

3.运行

    ./test.sh

围绕脚本编写，和自己的日常需要，做简要回顾。使用/bin/bash，总体上对Linux Shell的感觉上是语法上比较严格，但是提供了一种使用系统命令的好的方式。

例如：变量赋值

    NAME="/etc"
    echo ${NAME}/profile

变量赋值的时候，不能有空格，如下：

    NAME = "/etc"

例如: if...else...控制语句

    a=300
    b=400
    if [ $a == $b ]
    then
        echo "Yes"
    else
        echo "No"
    fi

其中的判断语句不能写成这样：

    if [$a == $b ] 或者 if [ $a == $b]

看到空格上的区别了吗？

### 修改文件

一个经常会遇到的场景是使用Shell脚本生成的图片路径上少了上一级目录或者需要批量构造cp命令；

例如原来文件是这样的：

    1/001.jpg
    1/002.jpg
    2/001.jpg

需要构造cp命令，批量执行：
    
    cp img/1/001.jpg img/0
    cp img/1/002.jpg img/0
    cp img/2/001.jpg img/0

使用vim的替换命令执行：

    :%s/^/cp img\/

    :%s/$/ img\/0

分别表示在当前行的首部和尾部替换。

总结：Linux的系统工具是个巨大的宝矿，很多工具和用法无论在速度上和性能上都非常的令人印象深刻。有系统如此，人生足矣，夫复何求？（哈哈）

参考：

1.[Makefile与Shell的问题](http://blog.sina.com.cn/s/blog_4cd5d2bb0101gptd.html)

给出了四个错误用例，同时给出了正确的版本及其错误原因。涉及Makefile脚本的行与线程的关系，变量引用的差异等。

2.[用户管理和权限控制](http://blog.csdn.net/boybruce/article/details/17198601)

3.[make, makefile, cmake, qmake的区别](https://www.zhihu.com/question/27455963)

4.[Linux系统环境变量的读取顺序](https://blog.csdn.net/c406495762/article/details/62902871)

5.[不同环境变量配置方式的区别](https://www.cnblogs.com/isoftware/p/3778028.html)

6.[一个make编写的demo](http://www.cnblogs.com/hazir/p/linux_make_examples.html)



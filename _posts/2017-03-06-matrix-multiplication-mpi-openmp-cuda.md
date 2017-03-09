---
layout: post
title: "[分布式]矩阵乘法的分布式实践"
excerpt: "MPI负责管理节点和计算节点通信，OpenMP负责计算节点并行加速，给出了并行加速比和效率曲线"
date: 2017-03-06 12:00:00
---

关于MPI和OpenMP不再赘述，可参考三个问题，关注两个人([李沐](https://www.zhihu.com/people/li-mu-23/answers)和[杨军](https://www.zhihu.com/people/yang-jun-14/answers))：

1.[算法研发工作中对于MPI和Spark的一些困惑？](https://www.zhihu.com/question/26887082)

2.[从并行计算的角度，MPI 与 OpenMP 的对比？](https://www.zhihu.com/question/20188244)

3.[MPI 在大规模机器学习领域的前景如何？](https://www.zhihu.com/question/55119470)

吐槽一句：不要再说MPI的容错能力渣了，MPI的标准设计是将容错交给应用程序了!!（你可以自己写容错，例如，xgboost的底层通信框架[rabit](https://github.com/dmlc/rabit/tree/a9a2a69dc1144180a43f7d2d1097264482be7817)）

---

##### 一.集群配置

![总体配置](http://wx2.sinaimg.cn/mw690/aba7d18bgy1fdd0j7byx3j20mj08y0tq.jpg)
![管理节点](http://wx1.sinaimg.cn/mw690/aba7d18bgy1fdd0jct9bdj20me085jsc.jpg)
![计算节点](http://wx4.sinaimg.cn/mw690/aba7d18bgy1fdd0jgpasuj20ma0810tl.jpg)

##### 二.集群运维

**总核数 = 物理CPU个数 X 每颗物理CPU的核数**

**总逻辑CPU数 = 物理CPU个数 X 每颗物理CPU的核数 X 超线程数**

    # 查看物理CPU个数
    cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l

    # 查看每个物理CPU中core的个数(即核数)
    cat /proc/cpuinfo| grep "cpu cores"| uniq

    # 查看逻辑CPU的个数
    cat /proc/cpuinfo| grep "processor"| wc -l

    #查看CPU信息（型号）
    cat /proc/cpuinfo | grep name

    #查看操作系统
    cat /proc/version

##### 三.MPI和集群

在二中了解到集群的基本信息之后，建立的通信结构如下图所示：

![MPI&cluster](http://wx4.sinaimg.cn/mw690/aba7d18bgy1fdd0luery5j20n40iy74d.jpg)

一个管理节点master和四个计算节点compute-x,每个计算节点8个core，由于超线程的存在，每个core支持两个超线程，并且每个计算节点有2个CPU，故一个计算节点的逻辑CPU是32。MPI负责管理节点和计算节点之间的通信，具体任务是数据分发和结果汇总。每个计算节点具体负责乘法计算，如下图：

![matrix&multiplication](http://wx3.sinaimg.cn/mw690/aba7d18bgy1fdd1yzf5b1j20z00dcglk.jpg)

假设要利用4个计算节点参与计算(可通过PBS作业调度系统完成)，则master负责矩阵A切分，并记录切分后的数据的起始地址和偏移量，然后将切分的某一块数据和矩阵B分发给对应的计算节点。例如，图中红色方框标准的内容，计算节点3计算矩阵A切分的第3块数据和矩阵B相乘的结果，虚线表示矩阵B的复制。

##### 四.PBS作业调度系统

给出实践中用到的PBS脚本（zhp_mpi_mm.pbs）：

    #PBS -N zhp_mpi_mm
    #PBS -o /home/zhpmatrix/code/c++/mpi/zhp_mpi_mm.out
    #PBS -e /home/zhpmatrix/code/c++/mpi/zhp_mpi_mm.err
    #PBS -l nodes=3:ppn=8
    cd $PBS_O_WORKDIR
    mpirun -np 24 -machinefile $PBS_NODEFILE ./mpi_mm
                                                       

在具体运行的时候，将代码(mpi_mm.c)和PBS脚本(zhp_mpi_mm.pbs)放置管理节点上，提交任务：

    qsub zhp_mpi_mm.pbs

运行结束，查看程序运行结果：
    
    #正确运行
    less /home/zhpmatrix/code/c++/mpi/zhp_mpi_mm.out

    #错误运行
    less /home/zhpmatrix/code/c++/mpi/zhp_mpi_mm.err

##### 五.加速比和效率

在PBS脚本中设置的是使用3个计算节点，每个计算节点8个core。在性能测试阶段，将计算节点数目和每个计算节点数目使用的core数当做变量，测试浮点矩阵A(1000x250),浮点矩阵B(250x200)相乘，结果曲线如下(关于曲线的变化，考虑通信cost)。

固定节点数目(nodes=4),每个计算节点使用的core数做自变量：

![1](http://wx3.sinaimg.cn/mw690/aba7d18bgy1fdd0l1ysd7j20kw0ckq3g.jpg)

横坐标表示每个节点数使用的core数目，纵坐标表示加速比。

![2](http://wx1.sinaimg.cn/mw690/aba7d18bgy1fdd0jwwv5rj20kw0ckwf2.jpg)

下图是计算节点数做自变量的结果(固定core=8)：

![3](http://wx2.sinaimg.cn/mw690/aba7d18bgy1fdd0l8s6raj20kw0ckdg9.jpg)
![4](http://wx3.sinaimg.cn/mw690/aba7d18bgy1fdd0k4pwufj20kw0ck0t7.jpg)

详细的内容还是要读[代码](https://github.com/zhpmatrix/parallel-computing/tree/master/matrix_multiplication_with_MPI)。在每个计算节点，可以采用OpenMP或者CUDA继续加速，我们的集群每个计算节点上还有两块K80！这里给出一个CUDA矩阵相乘的测试[代码](https://github.com/zhpmatrix/parallel-computing/tree/master/matrix_multiplication_with_CUDA)。

参考：

1.并行算法设计与性能优化，刘文志

2.CUDA并行程序设计-GPU编程指南，Shane Cook







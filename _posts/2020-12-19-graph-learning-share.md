---
layout: post
title: "Graph Learning: 一种数据组织观点"
tags: [NLP]
excerpt: "这篇博客是近期在组里的一个分享内容。主要讨论GL是什么，为什么要研究GL，怎么用GL，以及简要讨论我们自己做过的一些工作和想法。"
date: 2020-12-19 11:40:00
mathjax: true
---

对于知识图谱的构建，从非结构化数据中构建，知识的价值更高，但是对信息抽取能力的要求也更高；从结构化数据中构建，可以弱化对信息抽取能力的要求，转而将重心放在应用层，这对于一个有大量结构化数据积累的团队而言，是非常有吸引力的。

![img_1](https://tva1.sinaimg.cn/mw690/aba7d18bly1glt6n0o589j20zk0k0my7.jpg)
![img_2](https://tva1.sinaimg.cn/mw690/aba7d18bly1glt6n5eo5zj20zk0k0jso.jpg)

为了讲清楚图数据库和传统关系型数据库有啥区别？从一个具体例子出发。

![img_3](https://tva4.sinaimg.cn/mw690/aba7d18bly1glt6n91ik4j20zk0k00ux.jpg)
![img_4](https://tva1.sinaimg.cn/mw690/aba7d18bly1glt6nckrxjj20zk0k0mzj.jpg)
![img_5](https://tva2.sinaimg.cn/mw690/aba7d18bly1glt6nituwjj20zk0k0767.jpg)
![img_6](https://tva1.sinaimg.cn/mw690/aba7d18bly1glt6ozp1fhj20zk0k0432.jpg)

简单而言，ER图的设计和Schema设计对应，SQL和Cypher对应，关系表和图对应。

![img_7](https://tva3.sinaimg.cn/mw690/aba7d18bly1glt6p44iwpj20zk0k0wga.jpg)

传统关系表更像是一个个挺立的烟囱，每个烟囱中装载同一种类型的数据。而图则爆破了这些烟囱，将所有数据拉平到一个巨大的平面上。

那么，为啥要研究KG/GL呢？从一些具体的应用场景出发来看，如下：

![img_8](https://tva4.sinaimg.cn/mw690/aba7d18bly1glt6p7mmzpj20zk0k0juv.jpg)

这里给出一个Cypher相对于SQL在查询上更具优势表现的例子：

![img_9](https://tva2.sinaimg.cn/mw690/aba7d18bly1glt6r0qc47j20zk0k0tm6.jpg)

左上角是完美世界的产品：全历史的工作，右上角是个人非常喜欢的工作Magi（2019年的工作），左下角是组里小姐姐研究生期间参与的一个比较大的项目（华谱网）的具体例子。

![img_10](https://tva1.sinaimg.cn/mw690/aba7d18bly1glt6pf1abxj20zk0k0guq.jpg)

那么，一个知识查询服务，要具有什么样的特点呢？

![img_12](https://tva2.sinaimg.cn/mw690/aba7d18bly1glt6coou2zj20zk0k041a.jpg)

知识查询服务意味着图构建本身就可以产生价值。除此之外，也有其他的一些应用场景，如下：

![img_13](https://tva1.sinaimg.cn/mw690/aba7d18bly1glt6cs8zawj20zk0k0tdg.jpg)
![img_14](https://tva2.sinaimg.cn/mw690/aba7d18bly1glt6cvy1wgj20zk0k0jw8.jpg)
![img_15](https://tva4.sinaimg.cn/mw690/aba7d18bly1glt6czomrdj20zk0k0aho.jpg)
![img_16](https://tva2.sinaimg.cn/mw690/aba7d18bly1glt6d3i73zj20zk0k078z.jpg)
![img_17](https://tva2.sinaimg.cn/mw690/aba7d18bly1glt6dff5iyj20zk0k00w9.jpg)
![img_18](https://tva3.sinaimg.cn/mw690/aba7d18bly1glt6disgv0j20zk0k0af2.jpg)

总结一下，如下：

![img_19](https://tva2.sinaimg.cn/mw690/aba7d18bly1glt6dlxvs0j20zk0k0juf.jpg)


说了这么多的场景，那么怎么用呢？这里先给出一个该方向知识体系的脉络图。左图来自THU的唐杰老师组梳理的一个脉络图，右图是比较常见的一张NLP的milestone图。

![img_20](https://tva2.sinaimg.cn/mw690/aba7d18bly1glt6dp9maxj20zk0k0nbs.jpg)

从上述体系上观察，主要重点关注的工作有三个方面，这里用三张PPT分别简要介绍各个方向上的代表性工作。

![img_21](https://tva2.sinaimg.cn/mw690/aba7d18bly1glt6dycpe3j20zk0k0q6s.jpg)
![img_22](https://tva2.sinaimg.cn/mw690/aba7d18bly1glt6e2k49yj20zk0k0jxz.jpg)
![img_23](https://tva1.sinaimg.cn/mw690/aba7d18bly1glt6e6xv7nj20zk0k0q9b.jpg)

在读了大量相关方向上的资料之后，得出的一些比较宏观的观点，如下：

![img_24](https://tva1.sinaimg.cn/mw690/aba7d18bly1glt6eat039j20zk0k00vq.jpg)

最后，聊一聊我们自己的工作吧。目前已经做过的包括基于结构化和非结构化的数据做图谱构建，具体为电商领域美妆行业的知识图谱。

![img_25](https://tva3.sinaimg.cn/mw690/aba7d18bly1glt6eekqvbj20zk0k077f.jpg)
![img_26](https://tva2.sinaimg.cn/mw690/aba7d18bly1glt6emwdvtj20zk0k0mzm.jpg)
![img_27](https://tva1.sinaimg.cn/mw690/aba7d18bly1glt6eqx5v5j20zk0k0wgt.jpg)
![img_28](https://tva2.sinaimg.cn/mw690/aba7d18bly1glt6evfmuvj20zk0k042a.jpg)
![img_29](https://tva1.sinaimg.cn/mw690/aba7d18bly1glt6ezoxdmj20zk0k0wih.jpg)

关于上述描述的问题，在博客[电商域图谱构建-问题复盘](https://zhpmatrix.github.io/2020/11/25/business-kg-thoughts/)中有更加具体的阐述，这里不再瞎BB了。基于结构化数据的图谱构建，目前的图谱规模如下：

![img_30](https://tva1.sinaimg.cn/mw690/aba7d18bly1glt6f4g1qsj20zk0k040c.jpg)

基于上述工作，即将展开的研究内容如下：

![img_31](https://tva3.sinaimg.cn/mw690/aba7d18bly1glt6fconvsj20zk0k0gqp.jpg)
![img_32](https://tva3.sinaimg.cn/mw690/aba7d18bly1glt6fghon7j20zk0k0juk.jpg)

最后，总结一些基于结构化数据图谱构建的一些问题和注意点，如下：

（1）做一个好的SQL Boy吧（逃）。基于结构化数据构建的核心环节在于写SQL。

（2）DataFrame要用的6。基于SQL获取的数据能解决大部分问题，但是需要用DataFrame对这些得到的数据做二次加工，需要Join/Merge/Concat，需要去重，去空，分组等基本功能。

（3）人工参与不能避免。

（4）慢工出细活。整体上是一个非常细致的工作，要求对表，数据，属性，字符串等处理，数据处理的工作，不难但是步骤多，由此很容易导致某个步骤遗漏。数据的问题在小规模下不暴露，在大规模下就会暴露，是因为错误情况很难在没有看到数据的情况下想到，耐心一些吧。

（5）大规模数据处理需要工程优化。

（6）数据的问题，尤其要注意错误数据和遗漏数据，因为在图谱构建的最终结果中，这部分是需要被验证的，系统不会报错的。

接下来我们的工作会重点转向应用层，希望对该方向上的工作有进一步的理解和认识吧。

PPT链接: https://pan.baidu.com/s/1xob-iFB9kR5Ku1p69VkWGg 

提取码: 3h2b
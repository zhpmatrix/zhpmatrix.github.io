---
layout: post
title: "[思考]Think in Dialogue System"
excerpt: "关于对话系统的阶段性思考"
date: 2020-08-02 15:09:00
mathjax: true
---

相对认同的一个观点：在今天，几乎所有人都知道一个好的对话系统是怎样的，但是相关技术的发展不足以支撑这样的系统，也就意味着大众预期走在了技术发展之前。这样带来的问题是，用户需求永远不会得到满足，从业人员将一直苦逼。

#### 什么是对话

对话的目的是同步思维，对话是思维从高维到低维的投影，由此带来的挑战是：用低维表达高维

#### 基本总结（看了很多工业界产品）

+ 产品交互设计范式同质
+ 技术思路同质
+ 场景是差异化的主要来源

#### 关键技术（学术/工业）

+ 标注数据少：少样本学习问题

+ 可拓展性问题：变化的意图，变化的槽位和槽值，变化的系统动作

+ 训练效率问题：RL

+ 鲁棒和条件问题



#### 对话范式

+ 一问一答（问答系统多是这种了）
+ 多问一答（可以放在多轮对话中，多轮维度的考察可以放在问答中，也可以放在任务型中）
+ 多问多答（标准的任务型）
+ 抢答（增加系统的humanity）
+ 主动提问（话题控制）

上述五点总结，可以包括很多目前的工作了。对话系统的两端是人和机器，站在问的角度，希望人的角色更多的被机器替代（极端条件下，人不说一句话，机器知道我想问啥）；站在答的角度，希望机器的角色有更多人的特点；两条线的某个中间状态，就会带来最大的产品价值，也是现在多数工作的北极星。
    
#### 知识在哪里（一种观察角度）

于一个完整的对话系统架构，一种观察的角度是：知识在哪里。

+ FAQ线的知识在问答库

+ KBQA的知识在图谱中（表）

+ MRC的知识在非结构化文档中

+ 检索式Chatbot的知识在历史对话数据中

+ 生成式Chatbot的知识在模型参数中

+ 至于Taskbot，那是通往这些知识的控制路由，是过程，不是结果

成长中的对话系统在做纵向，相对成熟的对话系统在做横向，所谓横向，比如小冰添加了数羊，猜谜，看图说话等功能（正交可扩展）。较高成熟度的系统可能类似于现在的一些图像应用，来来来，快手又上线了新的美颜功能1，美颜功能2，美颜功能3......假设有天对话系统能够有较高的成熟度，对于做NLP的同学未尝不是一件好事。

#### 相关文章评论

13.[解密 chatbot 人工智能聊天机器人 技术沙龙](https://mp.weixin.qq.com/s/r7vPOSdH7XK_3jc1WLqr2Q)

在自然语言理解的难点总结上比较到位：

（1）多样性

（2）歧义性

（3）鲁棒性

（4）上下文

（5）知识依赖

12.[周明的分享](https://mp.weixin.qq.com/s/FBynWU8BLyJcUomO3Y8mSg)

比较系统的分享了微软在聊天机器人中的尝试：包括常见的FAQ，TaskBot，Chatbot，包括DocBot，TableBot等。

其中总结了对话系统的一些挑战：

（1）用户画像和个性化

（2）情感

（3）深度聊天（技术硬实力）

（4）知识挖掘（问答体系等）

（5）多种对话范式融合（对话路由）

（6）多轮对话和上下文模型

（7）多模态（完整的系统：语音，文本和图像，目前大多都是文本机器人）

（8）自定义/配置化（现在很多业界的平台在做）

（9）人机协同

11.[不是所有的智能机器人都能做好客服——浅谈智能客服机器人评价指标新趋势](https://mp.weixin.qq.com/s/n-uicubtTFyOH00HAvRgMQ)

比较全面的智能客服评价体系。

补充：[追一的评价体系](https://mp.weixin.qq.com/s/Xj2QMbZXPLigiFhsT33k_A)

10.[如何让智能客服更有温度？](https://mp.weixin.qq.com/s/d6ie_Q-NyMh4Sp4mXWqpyQ)

问题：目前的智能客服大多是采用配置的答案，这就导致了千人一面的现象。不同的用户询问一样的问题得到的答案是一样的，然后现实情况是很多问题由于用户的信息不一样，答案也是不一样的。

解决方案：

（1）多级置信

当置信度达到一定时，我们认为结果完全正确，那么我们就直接给出结果。当置信值低于这个阈值，但是又不至于过低时，机器人则可以将解析结果进行反问，询问用户是否询问该问题。如果置信值低于一定时，机器人认为用户说的话无意义，机器人反问用户：“您说的话我没有理解，您可以简单重新描述下您的问题”。

（2）推荐

相关性推荐；预测推荐；生成推荐；提醒

9.[Chatbot and Related Research Paper Notes with Images](https://github.com/ricsinaruto/Seq2seqChatbots/wiki/Chatbot-and-Related-Research-Paper-Notes-with-Images#kaisheng-yao-baolin-peng-geoffrey-zweig-kam-fai-wong)

列举了一些比较早期的对话系统相关的文章，以生成式对话系统为主，同时列举了具体的文章的知识点和相关的图片。

8.[商用对话机器人技术及挑战](https://mp.weixin.qq.com/s/Tq61UOry2mnFaMSOIeV1wg)

简单描述了爱因互动的机器人技术，这家主要是给大B做机器人。CTO之前是在世纪佳缘做Bot的（**单身狗，划重点了**）。

7.[Google Duplex(用于Google的Assistant)](https://ai.googleblog.com/2018/05/duplex-ai-system-for-natural-conversation.html)

Duplex是语音机器人，文章中列举了具体的人机交互的语音片段，同时分享了一张Duplex的Lead和工程manager用Duplex订餐，并合影的图片，才是最酷的。

6.[你问我答之「智能客服评价体系全解读」](https://mp.weixin.qq.com/s?__biz=MzIzNzY5NDM2Nw==&mid=2247484049&idx=1&sn=d1d100abb898663900ccc2aa78aea0ad&chksm=e8c5fe61dfb2777732b9eada85bdde26c6cdd6b2c707ccf14f8c8d3dedb2bd7128c38bfc2bce&scene=21#wechat_redirect)

客服系统评价体系：用户角度（提升满意度），运营角度（提高拦截率，少写正则，逃），技术角度（技术指标要高）

5.[58智能客服QABot问答机器人算法实践](https://mp.weixin.qq.com/s/o7x1BigfIMJIJEGxlFlLow)

4.[行业内关于智能客服、聊天机器人的应用和架构、算法分享和介绍](https://github.com/lizhe2004/chatbot-list)

3.[北航大数据高精尖中心研究团队对问答系统的调研](https://github.com/BDBC-KG-NLP/QA-Survey)

2.[Yibot-知识体系运营](https://mp.weixin.qq.com/s/9-HUoePmGvv40JVWcPtHew)

1.[贝壳找房的客服系统](https://mp.weixin.qq.com/s/b-Y8LUlKt8WOHtJG-HHFGA)

0.[阿里小蜜-电商领域的智能助理技术实践,阿里巴巴-智能服务事业部-小蜜机器人X-Lab ——张佶(吉仁)](http://bos.itdks.com/79928a1b774c4d88a0c1b171d990263e.pdf)

微软和剑桥基于RL的工作用于多轮增强式导购。相关工作：[蚂蚁金服-温祖杰的分享](https://yq.aliyun.com/live/2446)。基于强化学习的交互式澄清，基于强化学习的交互式文本推荐，基于强化学习的客户路由三个工作。

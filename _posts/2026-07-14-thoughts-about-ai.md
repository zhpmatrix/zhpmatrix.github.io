---
layout: post
title: 26年7月，关于AI的碎碎念～
excerpt: AI的发展既快也慢，快在表面，慢在底层逻辑。
date: 2026-07-14 10:00:00
tags:
mathjax: true
---
_前言：
25年开启Agent的元年，26年观察到一些组织在积极推进AI-Native升级，包括组织升级和业务改造等。进入AI大航海时代，拿着旧世界的地图是找不到新世界的大陆的，但是首先得有地图。虽然在持续投入探索，但是在基础概念和方法论上似乎并未形成共识，盲人摸象者众。这篇文章站在笔者自身的角度给出个人的肤浅理解。_

#### 我们要开搞AI-Native

<u>如何判断一个产品是AI-Native的？</u>**如果这个产品没有了LLM，那么产品的逻辑不成立，也就意味着这个产品是AI-Native的**。因此，豆包客户端是一个AI-Native的应用，Claude Code是一个AI-Native的应用。

假设计算器和导航工具都是AI驱动的，那么，计算器普及以后，人类不必再用纸笔计算复杂数字，但是我们也离不开计算器了。导航出现以后，人类也不必记住每一条路，但是我们也离不开导航了。
豆包和Claude Code尚未在更大范围内验证自身的不可或缺性，但是已经被验证的是计算器和导航不能离开AI，用户不能离开计算器和导航。

自动驾驶的导航系统中，人类驾驶员根据导航系统中的导航方向决定自己的驾驶动作，如果没有导航，驾驶到某个自己不知道具体方向的位置不成立，但是驾驶动作是人类自己完成的。理想中的自动驾驶系统，驾驶动作是由AI自己完成的。在这个场景中，两种AI都可以认为是必需的。

此刻，耳边传来一句歌词:**token就是水电煤**～

<u>如何判断一个组织是AI-Native的？</u>一个只有人在干活的组织是非AI-Native的。围绕人和AI的协作方式，一个组织中的活全部由AI干是AI-Native的，AI辅助人干活是非AI-Native的，因为意味着这个活没有AI，只有人也能干。这样的组织有适配的一系列的AI-Native的协作工具，如multica和paperclip等。

#### Agent有一万种解释？

对Agent的理解从一开始到现在都没有发生过改变。在[lilianweng的blog](https://lilianweng.github.io/posts/2023-06-23-agent/)中给出了Agent的overview:
![1784020205264-image](https://obsidian-images-1329890864.cos.ap-guangzhou.myqcloud.com/images/1784020205264-image.png)

如果翻一翻AI的发展史会发现，人工智能的先驱们对于智能体已经思考的比较清楚。26年的工业界有一些不同的表达方式，如下：

<u>Agent = LLM in the loop。</u>这个loop中完成的就是上图中的虚线所示部分，因此衍生出Loop Engineering等。

<u>Agent= LLM + Harness。</u>其中的Harness可以理解为在loop中做的具体的动作，因此衍生出Harness Engineering等。

回归到本质上，如果没有LLM和loop，那么大概率不是一个Agent。可以基于workflow做一个在行为上类似Agent的东西，但是大概率在某些条件下会发现也只是类似而已。

在实现侧，虽然有诸多类似LangGraph，AutoGen和CrewAI等开源框架，但是在技术原理上非常接近，因此采用Claude Code也可以完成较多非Coding类的任务，<u>Claude Code本质上也是一个通用的Agent框架</u>。
#### 记录一切

随着基模能力的不断提升，context会成为瓶颈。除了context rot等问题，<u>如何获取context会成为那个更重要的问题</u>。

沟通对话为什么困难？因为沟通双方在一个高度不对齐的思维环境中。

合作干活为什么困难？因为协作双方的工作环境存在较大区别，需要通过沟通税消除这种区别。

为什么LLM/Agent做的不好？因为context不全。未必是事实，但是应当是主观的第一选择。因为在无法改变环境的条件下，能够改变的只有自己，只有自己的context。

[从超级个体到超级组织：1688数据中心Multi-Agent研发小队实录](https://mp.weixin.qq.com/s/ClAbgCHuocfChSuEDdtdeg)中提到“<u>知识回流，必须建立在所有人在同一平台上</u>“。

Plaud作为一个现象级的硬件产品，所做的事情也只不过是录音并总结。

Obsidian/flomo等产品，同样是希望用户以简单的方式去记录文字，正如flomo的口号：持续不断记录，意义自然浮现。类似产品包括比较流行的视频日记类产品等。

<u>在LLM能力日渐强大的情况下，人之所以为人？</u>

回到DIKW模型上，W的产生，需要DIK。K的产生也需要DI作为输入。因此，一切的始发点在于数字化，首先要把DI能够以数字化的方式保留下来，其次是做数据治理和知识提炼，最终才有可能基于LLM产生智慧。

隐形知识/经验能否数字化？如何数字化？
思考过程能否显性化？人物情感能否被量化表达？

进入26年在LLM成熟度已经非常高的环境下，数字化这件事情依然有极大的挖掘空间。这是一件苦活儿，累活儿，没人愿意干的活儿，但是极具价值的一个活儿。
#### AI Coding是救世主

AI Coding为什么成为兵家必争之地，有至少以下两个主要原因：

+ Code作为连接物理世界和数字世界的唯一桥梁，有其重要的价值（自计算机诞生以来就是如此）
+ Code作为人类智慧的结晶，github/gitlab等是天然的宝贵的巨大的标注数据

有训练数据，有用，为什么不干？与之比较类似的是基于Lean的数学形式化证明，但是相比Code，这个事情距离现实世界还是存在一定的距离。

在杨军的[对Agent技术的一些随思](https://zhuanlan.zhihu.com/p/2055782042420372097)中表达了诸多观点，其中大多数的观点笔者都与之类似。站在当前的节点看，AI Coding几乎是LLM这次浪潮中最早PMF的场景，但是由于没有脱离软件工程的整体语境，因此没有银弹的叙事依然成立，故AI Coding对于软件研发范式的变革依然在路上。

#### 相关资料

[《2026人文社会科学智能发展蓝皮书》:重新发现深度思考的价值](https://mp.weixin.qq.com/s/X2cu6q-MFw4NC6sL3sxryA?mpshare=1&scene=1&srcid=0714NdFghOT03SMzAFqqL5mC&sharer_shareinfo=2bd091a3ce2a66ebf7c379989dede593&sharer_shareinfo_first=2bd091a3ce2a66ebf7c379989dede593&version=5.0.6.99829&platform=mac#rd)


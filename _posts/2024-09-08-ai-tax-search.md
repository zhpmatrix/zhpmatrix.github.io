---
layout: post
comments: true
title:  "[搜索系统]一次面向垂域搜索系统的实践与思考"
excerpt: "一个如何做架构的故事"
date:   2024-09-07 10:35:00
mathjax: true
---

好久没有写文章了，过去几个月时间在solo一个文档搜索产品，随着2.0版本的全流量上线，终于可以喘一口气做一个回顾和复盘。

产品一方面要直接满足500万B端用户的专业领域知识搜索需求，另一方面作为基础能力间接满足咨询客服等业务场景。通俗意义上，前者的用户体验，接近于从BingChat开始的各类AI搜索类产品，技术范式接近于RAG(Retrieval Augmented Generation)，而无论是AI搜索还是RAG，在过去的很长一段时间，都有大量的文章在讨论，比如笔者的[RAG在若干医疗场景的实践和思考](https://mp.weixin.qq.com/s?__biz=MzU2MTY2ODEzNA==&mid=2247484869&idx=1&sn=4bf5c85a58fa2e5ee477442752d2a832&chksm=fc740c8ccb03859afd52c4294626eb7b9014533cb4615343f4102708a46128db8fe70afa8407&token=1535827598&lang=zh_CN#rd)。

RAG的关键在R而非G，因为G侧对于大多数目标落地的团队而言空间非常有限，因此能把R做好的团队，RAG的应用大概率做的也不差。围绕R的误解颇多，比如R是个老问题了，现在做没啥意义了；百度和Bing投入那么多人和时间，要追吗？比如花两天时间就能搞定了吧......(hhh)。anyway，这篇文章结合笔者的实践讨论一些自己的理解。

R分解之后的核心对象（还有重要但非核心的对象）包括Query，搜索服务和文档库，通过搜索服务建立Query和文档库的联系。其中，Query的特点是开放不确定，长尾性以及弱上下文等，文档库的特点是非结构化，强领域特征以及标签化程度低等，搜索服务要解决的问题包括但不限于一对多，非对称，在线，相关性，时效性，多样性等。搜索交付的价值不仅是一个服务，更是一个数据，工程，算法和策略的结合体，一个易用，可理解，可持续演进的系统。

为了构建这样的一个系统，首先搭建了一套评测体系，体系设计原则在之前的文章中也反复提及，包括人工和机器相结合，低成本自动化可量化以及分层&多粒度。具体包含评测目标，评测指标，评测方式以及评测依赖四部分内容。整个评测体系也并非从刚开始就全部搭建完成，而是和不同阶段的目标做适配以及持续迭代，以能否支撑搜索服务的演化为唯一目的，实际上截止2.0上线，整个评测体系在代码和机制上才比较接近最初设计的整个体系。

整个搜索架构在经历四个版本的演进之后，实现了对以BingSearch为代表的第三方搜索服务的替代，最终满足单链路多模块，单模块多方法的特点，能够支持多知识库配置以及搜索实例的配置化。

BingSearch在POC阶段，有助于实现想法的快速验证。但是随着迭代的深入，BingSearch的引入对于服务演进的阻力逐渐加大，比如过滤只能后置，比如为了实现能力兼容需要做较多的比较痛苦的架构上的trade-off，其中也经历了BingSearch大面积宕机的问题，刚开始还以为是自己的服务挂掉了，直到现在服务稳定性尚存在问题。结合成本考量以及自研进度的跟上，最终实现了对BingSearch的替代。每个外部组件的引入，要做得失考虑，希望metaso能够扛得住！

从1.0到2.0的持续迭代过程中，比较接近于“开着飞机换轮子”。其中推动了基于ES8的混搜方案，多视角知识加工和应用的标准化，建立围绕RAG为核心的应用开发范式等，离线配套工具的构建以及在线流量复制和A/B等也显著提升了迭代效率和研发效能。

其中，一站式搜索查因工具作为自底向上推动的工作，承载了较多的功能。主要面向非算法背景的同学，比如产品经理，运营同学，前后端开发等，支持搜索服务的全链路追踪，GSB评估等，同时附加功能包含基础能力分析，Prompt调优，DEMO演示等，轻量级的知识运营模块也包含在内。随着工具的发展，除了服务于搜索产品的演进，也逐步以直接或者间接的方式用于其他产品的迭代和项目验收的支持等，早已超出了搜索服务的支持工具属性。

随着应用研发的展开，多条线的技术范式基本类似，但是每条线都有自己独特的业务属性，因此需要一个框架抽象，通过模块解耦等，实现进行中应用的能力复用，以及支持新增应用的快速开发。整体上这是一个易用，可理解和可演进的框架，具体要求包括：

（1） 框架和应用分离，应用和应用隔离

（2）区分能力和内容

（3）支持各个环节的个性化实现

早期采用应用和框架协同演进的思路，能够实现进行中应用的能力复用，实际上这也是不得已为之。通过具体应用的开发为抽象提供具体案例，框架侧多走一步后，在具体应用侧验证框架能力。整体上目前依然处于这个阶段，在三个具体应用的反哺下稳步迭代。同时对于复杂度低的应用开发，框架已经基本能够满足快速开发的要求。

具体来说，在一个开发界面下，通过整合能力和内容，区分具体业务和通用框架能力，实现具体应用的开发。

内容侧，应用开发者只需要提供搜索数据（MySQL），mapping和用于表征的服务地址，即可在较短的时间内获得一个index，同时支持搜索数据的T+1更新。对于原始搜索数据的加工链路，针对不同的用户群体，分为不同的策略。如果来自业务侧的数据，需要用户侧完成增量链路的搭建，如果是中台数据，则由中台团队完成，也即该配置化模块的开发方自行完成。整体的流程通过一个统一的配置化界面完成，实现了多视角知识加工和应用的标准化。

能力侧，框架整合了算法中台已有的基础算法服务能力，沉淀的可复用的用于搜索的各个模块的可通用能力，配套周边能力含日志，异常等。

以上基本讨论完了主要做的工作。围绕之后的计划，搜索产品侧会推进能力和内容侧的持续优化，支持产品侧的体验提升，同时实现更多的业务接入；一站式搜索查因工具的主要目标是两个，分别是易用性提升以加强对搜索产品服务迭代的支撑力度，沉淀标准组件提升可复用性；框架侧通过和具体应用的交互，实现持续框架演化，同时推动框架在更多应用场景的使用。

这里不谈搜索主链之外的包含AutoSuggestion，相关搜索，分页，人工运营等，搜索产品在用户交互侧是简单的，一个输入框，返回一个搜索列表。在搜索主链稳定的前提下，似乎做的工作都是单点扭螺丝，ROI有限，不是很清楚现有成熟搜索团队的状态是否是这样？但是搜索主链的从0到1，是一个非常复杂的任务，需要良好的架构设计。过去的几个月其实每天都在谈的，不是算法模型训练，不是评估标准设计，而是架构设计。

所谓架构，就是有什么和没什么，什么与什么之间的关系是什么？是对一个领域的认知的体现，其中关键的是要看到问题的本质。引用玄难大师的观点，一个牛的人是对领域有一个稳定的认知。所以这势必是一件有挑战的事情。

搜索是一项融合了数据，工程，算法和策略的系统，并非只是交付一个无状态的独立的算法服务。举一个例子，相同搜索Query，在不同的时刻搜索结果列表可能是不一致的，分析原因是什么？可能原因如下：

+ 搜索内容是T+1更新的

+ HNSW导航图使用了近似KNN算法（使用暴力搜索，虽然不会引入随机性，但是大规模场景下不适用）

+ 混搜时引入了高斯时间衰减（时效性提升特别好的一个性质）

+ 大模型自身生成结果的随机性

其他的可能因素含：硬件的差异性等，绝对意义的一摸一样，比较难实现。整体上看，搜索系统是内容和能力的混合体，两者都是要能够可演进，但又不是所有的组件都能够正交设计，这样势必会带来一些复杂性。

在单链路多模块的cascade模式下，一个优化动作具体在哪个环节实现是最佳选择？在[阿里妈妈朱小强的文章](https://zhuanlan.zhihu.com/p/398041971)中提到两种设计哲学，分别是城邦自治模式和一盘棋模式，“召回、粗排、精排等每个模块都按照自己对于全局一致性逻辑的理解，在平衡好集合规模、算力消耗、系统性能等约束的情况下独立迭代”，因此这里一定会存在一个在哪个城邦实现治理的问题。实际上，一盘棋模式在其他的应用中已经有用到，把路径做短，单个模块做宽。面向具体目标，精排也许并非必要？这种模式更加敏捷，不过对于单模块的能力要求更高，因为在特定阶段要完成更多的目标优化任务。这也是笔者自身的一个架构演化方向。

给很多朋友安利过的张刚老师的[《软件设计：从专业到卓越》](https://book.douban.com/subject/35966115/)中谈到契约式设计。所谓契约式设计，就是权利和责任，边界问题也是权责问题。跳出来，不带偏见的思考，哪些是我该干的，哪些不是我该干的，拥有上帝视角。“做多”场景包括通过Query扩展增加用于搜索的Query数（多Query），通过增加知识库扩大搜索内容（多知识库）,通过增加召回通道实现召回结果的多样性（多召回通道）等。

针对多召回通道，一种设计是，固定召回文档数量，随着召回通道数增加，每个召回通道平摊文档量。优点是排序成本不增加的条件下，增加了多样性；缺点是假设召回文档数量等于召回通道数，那么每个召回通道只能分到一个文档，如果前者大于后者呢？这里存在一个显然的bottleneck。因此另外一种设计是，不要限制召回文档数量，在排序阶段通过算力并行实现对召回文档的排序，以算力换多样性。召回的责任之一是提升召回文档的多样性，为下游实现充分的供给，因此有权通过增加召回通道数实现这一目标，且不能因为会增加下游排序的成本而不去选择。因为增加下游排序成本的问题，可以在下游通过算力消耗解决。

在早期，如果允许召回文档数量较多的条件下，采用第一种设计也可以但是存在潜在的设计瓶颈。因此在该问题中也可以看到，除了数据，算法，策略和工程，算力也是一个部分条件下需要考虑的因素。

除此之外，还有一些有价值的问题需要思考。在多Query+多知识库+多召回通道的条件下，搜索的最小颗粒度是什么？怎么保证在元素从1扩展到N的时候，架构调整的最小化？能力和内容一定是强耦合的吗？

接下来的基本方向包括如下：

+ 通过一份相同训练数据，按照不同的训练策略得到三个模型分别用于搜索主链的三个关键环节以期全链路的效果提升

+ 搜索内容侧的粒度升级，通过更细粒度的知识管理，提升搜索的精细化以及摘要生成的上下文获取简化

+ 融合结构化和非结构化信息的搜索架构3.0

+ online learning，融合在线点击feedback信号到搜索主链中（实时数据工程），以及考虑专业搜索用户profile，实现搜索服务的个性化能力提升。

如果顺利地话，产品本月能够和C端用户见面。

**[扫码加笔者好友](https://zhpmatrix.github.io/about/)，茶已备好，等你来聊~**














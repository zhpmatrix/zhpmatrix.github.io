---
layout: post
title: "NLP技术思考"
tags: [技术杂文]
excerpt: "这篇博客主要讨论NLP领域的一些技术思考。"
date: 2020-05-10 15:09:00
mathjax: true
---

如果有一天，我不做NLP了，那会是因为什么原因？离开，总是因为一些什么。

（1）做移动互联网产品还是人工智能产品?

O2O巅峰时，群魔乱舞，盛世狂欢。O2O落幕后，一地鸡毛。所谓，眼看他起高楼，眼看他宴宾客，眼看他楼塌了。O2O解决的是线上线下打通的问题，本质上是利用了移动互联网获取信息的方式。对商家而言，扩散了信息传播的能力，对用户而言，扩大了信息获取的能力。

O2O时代，我们聊什么？聊规模化，聊ToC，不聊技术。我有一个改变世界的想法，只需要一个网页端码农，一个IOS码农，一个Android码农就可以了。
       
进入人工智能时代，技术激发了想象力。计算机可以识别图片中有没有猫了，计算机可以自己写文章了，计算机可以和人直接对话了，计算机可以打败人类了，一波未平，一波又起，好不热闹。
        
于是，一家又一家的人工智能公司在国内国外成立了。
        
到了人工智能时代，来自上一个时代的O2O产品经理依然希望规模化，希望ToC，那么主要矛盾就来了。
        
NLP提供的原子能力天然不适合作为一个独立的应用对外服务。为了最大化NLP的原子能力，需要嵌入到一个基本盘中。比如搜索，广告和推荐就是理想的基本盘，NLP可以作为一个环节的解决方案出现。作为对比，CV的原子能力可以单独包装成一个产品对外服务，如人脸识别，安防等。作为独立的NLP创业公司，缺乏基本盘，就缺乏一些想象力，"没活儿干"就是一种现象。

数据驱动型的算法是难以规模化的主要原因。对于感知型算法而言，情况尚好。对于认知型算法，以NLP算法为例，简直是一种灾难。用户的需求是多样化的，数据是多样化的，自然语言本身是多样化的。因此，业界已经基本形成一个结论，要做垂直受限领域的NLP问题，比如法律，金融，电商，汽车等。这也从一个角度解释了为什么人工智能要ToB，而不是ToC，因为B端提供了基本盘，同时是垂直受限领域。

算法迭代预期天然低于O2O迭代的预期。迭代包含两个评价维度，分别是速度和质量。一个需求微小的变化，需要重新收集，标注数据，训练模型，评测和上线，一般周期长于修掉一个日常Bug。由于以深度学习为基础的算法模型追求泛化能力，追求用统计的方式看待模型指标。这会引发两个方面的矛盾：第一是模型指标的提升不一定会带来业务指标的提升。第二是用统计的方式看待问题还是单个例子的方式看待问题。"模型指标提升了20%个百分点，为什么这两个输入还是误报？"就反映了该问题。

综上，优秀的产品经理是难得的，优秀的人工智能产品经理更是难得。需要对人工智能产品的迭代和闭环有清晰的认识，明白产品优化的目标到底是什么。

（2）算法模型的发展是非线性的。
        
第一个问题讨论的是需求侧的问题，也就是落地场景的问题。这个问题讨论供给侧的问题，也就是算法能力。对于一个非成熟的技术，发展轨迹长期看是线性的，但是短期看是非线性的，短期的周期可以用十年为单位，所以长期的单位大概不是所有公司所能够承受的。

BERT的出现，让自然语言理解的模型能力爆发式增长，因此增加了落地可能性。BLEU的定义，促进了机器翻译的突飞猛进式的发展。序列到序列框架的出现使得能够做很多自然语言生成的任务，比如翻译，摘要，改写等。早期的Word2Vec，多任务等带来的NLP里程碑式的发展，但是这种里程碑，在漫长的NLP发展历史中，屈指可数。这里想表明的一个观点是：堆时间是算法模型发展的必要不充分条件。当然，这里并非否定增量式创新的工作，这是量的积累。质的突破，可遇不可求。"再给我两年时间，我能够提升50%的指标。"，你确定吗？
        
人工智能产品是强技术依赖的，问题或场景能够促进算法的发展，但是没有过硬的技术，妄图通过设计的方式弥补技术短板，势必会不太容易。

综上，算法是人工智能产品发展的硬实力。先不要把锅甩到缺乏独立且可以规模化的场景上，提升算法的能力，降低算法迭代的不确定性，很多问题会迎刃而解。很多产品上的问题，多是算法不行带来的。但是，从另外一个方面，算法的能力增长不是线性的，不能因为算法不行，产品就不做了。不行还得上，那不得吵架吗？

（3）护城河在哪里？

理想中，产品的核心竞争力在算法，算法是护城河。但是回到现实，能把算法作为护城河的产品实在凤毛麟角。
       
在NLP研究中，也存在贫富差距。比如比较牛的组，一直牛。当然，对牛的评价指标多是ACL，EMNLP等顶会量。至于顶会作为牛的评价指标是否合适，不是这里的重点。
        
想像一下，论文的流水线式作业。实验室有积累的标准数据集，经过多代人沉淀的基础代码，实验室负责人思考多年的要去解决的问题，实验室成员积累的想法，论文写作的基本方法等都是一套成熟且标准的生产线。一个新人上工了，从想法列表上找一个感兴趣的想法，写对应的实现，剩下的大部分工作前人已经做好，就可以进入标准化的生产流程了。更细粒度的分工是，高年级同学要论文毕业负责统筹写作，低年级同学分工做实验，写实验部分的文章，画图作表，最后负责人做产品的质量检查。能不高产吗？
        
贫富差距的一个结果是，最牛的算法都是来自牛组，最牛的算法你能看到，我也能看到，你能实现，我也能实现，怎么作为护城河？

以业界围绕NLP创业做的最多的一种产品聊天机器人为例。产品交互范式同质，技术实现同质，异质性来自业务场景，无非是你做法律，我做金融。一旦一个事物被标准化，剩下的就可以批量生产了。
        
综上，和（2）中讨论的问题对立。算法理应成为护城河，但是现实的诸多因素决定算法恰恰不是。用合适的算法，解决一个合适的问题，从而能够产生一定的生产力的提升，是我认为的护城河。简而言之，护城河是一种系统能力，单纯的说算法或者场景作为护城河都不是很合适。

（4）算法大佬在哪里？
        
有一个不严格的一个结论，O2O培养了大批的产品经理，做APP，做网页。人工智能的浪潮将催生大批的算法工程师。这批算法工程师中，多数以深度学习作为核心技能栈。深度学习的更新速度实在是太快了，从每天的NLP领域的arXiv更新论文可见一斑。因此，一个正在蓬勃快速发展的领域可以沉淀的内容自然不是很多，自然尚未形成一套科学有效的方法论。所谓方法论，是能够指导实践的。事实中，无论在学术研究还是业界落地中，毫无疑问，这是实验驱动的。

解决一个问题，我有五种建模方式，我能够说出五种建模方式的优缺点，那又有什么用？多数情况的实践，没有足够的理论依据，保证这种建模是最优且能确定性的解决问题。较大的试错空间，巨大的不确定性限制了对结果的高预期。这种情况，将高度依赖经验，谁踩的坑多，谁的方案有更大的胜算。失败的结果是可以被解释的，成功的结果依然可以被解释，奇怪吗？

针对一个具体问题，给出确定性高的最优解，就是理想中算法大佬的样子。最优解不意味着酷炫复杂的模型，而且恰到好处，多一分太甜，少一分太苦。算法大佬对结果负责，最终的产出是一套解决问题的完整方案（系统的思路）。

（5）需要解决的问题，未完，待续。
        
站在产品角度，NLP的场景挖掘是一个值得长久思考的问题，业务模式的创新是一种成本较低，收效快的方式，目前的NLP落地场景还不能令人满意，包括CV的落地场景（在两个比较差的赛道中选谁最好，没意思）。这是顶层驱动力，可以倒逼技术发展。

通用NLP的原子能力还有待发掘，能够先用好手上的工具，能力最大化尚且不易。其次需要考虑边界能力，包含推理，常识，少样本/零样本，开放域等。这些问题的确重要，但是核心NLP能力尚未最大化。
       
总结一下，需要商业和技术的协同发展，没有先后。

（6）确定要分手吗？
   
可以起的早，但是可以跑跑步，吸吸氧，不要着急赶集。场景发现能够快速的做出好的产品，技术细节的创新突破能够带来超乎想象的价值，不要低估一两个百分点的提升引起的体验变化，这是生产力的进一步挖掘，生产效率的提升。

自然语言的问题不重要吗？作为交流的媒介，高等智慧的低维表达，太重要了。NLP不重要吗？对语言的建模是语言干预的工具，是老三套搜索/广告/推荐的重要环节。NLP创业要凉吗？未必。以正确的方式做正确的事情，期待结果的到来是时间问题。

 "阿瑟·克拉克在这里长眠。他从未长大，但从未停止成长。"，蒸汽机，电力和互联网的发明，每一次均是源自人类对价值和能力的无限渴望。把人工智能当做一类新物种，相信它从未长大，但是它正在努力生长。
 
 距离2020年5月21日还有不到两周的时间，一束玫瑰两杯茶。
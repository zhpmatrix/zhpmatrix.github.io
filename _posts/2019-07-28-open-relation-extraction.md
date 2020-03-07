---
layout: post
title: "[知识图谱]开放域信息抽取"
excerpt: "关系抽取可以预先定义schema，这是目前的一种主流做法。但是同样在一些场景下，可以不预先定义schema，称为开放域信息抽取。在自己之前的工作中，多数做了前者，但是目前的一个工作，可能后者更加符合需求，因此这篇博客主要调研相关工作。"
date: 2019-07-28 15:48:00
mathjax: true
---

强调两句：

>开放信息抽取的三元组的\<S,P,O\>都是来自于待抽取的句子，也就是说S,P和O都会出现在待抽取的句子中。不同于其他场景，P可以是预先定义的relation(可以不出现在句子中)，而S和O都是来自待抽取的句子。

>调研的目的在于不希望预先定义schema去做关系抽取，同时最好不要引入标注任务(比如构造平行语料)。

主要阅读的[论文列表1](https://github.com/NPCai/Open-IE-Papers)，[论文列表2](https://aclweb.org/anthology/D14-1201)。


**总结：**

首先，要明确一下开放域信息抽取的目的，在强调部分已经说明。

其次，开放域信息抽取的主流路子，个人认为在**写规则**。写规则主要包括两条线：第一是基于内容的匹配，例如写正则表达式；第二是基于结构的匹配，基于句法分析。实际上，这两条线从相关学术界和工业界的一些工作来看，在**垂直场景**下都是可以work的。第一需要业务专家的参与，第二需要好的句法分析和业务专家，如果句法分析是数据驱动的，且通用句法分析不满足要求，则是将直接的关系标注任务转移到了句法分析，其实这是很有启发性的一条思路。

最后，有一些比较有意思的思路。比如**无监督的关系抽取**（个人对无监督保持极大的好奇心，但是实际上多数情况下，无监督的效果不达预期，希望进一步发展吧。），比如用**序列标注**和**seq2seq**的思路，将标注任务转移到其他模块，这两种思路要严格满足强调中提到的假设。

如果和我的目的一样，只是为了了解一下目前的开放信息抽取的主流方式，就基本可以结束了。下文是一些相对具体的工作，希望有一些启发。

1.[《Chinese Open Relation Extraction and Knowledge Base Establishment》](https://github.com/lemonhu/open-entity-relation-extraction),TALLIP2018

类似工作：《Chinese Open Relation Extraction for Knowledge Acquisition》

基于依存句法的方案。依据具体的待抽取的关系和语料特性(话术体系)，依据**依存树**和**依存图**设计了七种抽取
规则，其中一种如下所示：

![img1](http://wx1.sinaimg.cn/mw690/aba7d18bgy1g5d57xl7iej20k903rdg9.jpg)

可以基于[LTP](http://ltp.ai/demo.html)平台进行测试。其实，相对适合抽取的语料如下：

```
德国总统高克。

高克访问中国。

习近平在上海视察。

习近平对埃及进行国事访问。

奥巴马毕业于哈佛大学。

习近平主席和李克强总理接见普京。

习近平访问了美国和英国。

高克访问中国，并在同济大学发表演讲。
```

这种方式和**基于正则**的抽取类似，不过前者是基于结构的，后者不仅有结构，同时可能有内容上的限制，是更加严格的约束。同属于**模式匹配**的范畴。

这篇文章同时给出了一个[中文的关系抽取库](https://github.com/TJUNLP/COER)。同时提到了[The Automatic Content Extraction(ACE)](https://www.ldc.upenn.edu/collaborations/past-projects/ace/annotation-tasks-and-specifications)数据，有830篇标注的中文文档，内含实体，关系和事件。

**想法**：整体上存在两个大的问题，第一是依赖于上游基于语言学工具；第二是需要专家设计好的DSNF；假设上游的语言学工具的获取需要数据驱动，则是将直接进行关系抽取的标注任务转移到了其他任务而已；但是假设可以间接利用通用的语言学工具，且要解决的问题话术体系稳定，也是一个思路。

2.《A Sentence Simpliﬁcation System for Improving Relation Extraction》

提出了一个用于开放信息抽取的预处理操作：句子简化(**syntax-based sentence simpliﬁcation**)。句子压缩可以称为一个单独的任务，印象中ACL2018中的某个工作做了一个数据集。

3.《A Survey on Open Information Extraction》，2018

**OIE的三个挑战：**

（1）自动化。不需要预先定义schema，不需要标注数据；或者定义少量的schema，标注少量的数据

（2）数据依赖。理想中的OIE是**domain-independent**的。

（3）计算高效。“Open IE systems must be computationally efﬁcient. Enabling fast extraction over huge datasets, shallow linguistic features, like POS tags, are to be preferred over deep features that are derived from parse trees”


**OIE的四个方向：**

第一：learning-based

和之前博客提到的[snorkel](https://zhpmatrix.github.io/2019/06/05/snorkel/)是一个很类似的系统。

第二：rule-based

基于内容写规则，类似于写正则。

第三：clause-based

基于结构写规则。类似于1的工作。

第四：approaches capturing inter-proposition relationships

比较有意思的问题，但是感觉并不能算是一个方向。问题如下：给定一句话，

	Early scientists believed that the earth is the center of the universe.

可以抽取的三元组如下，

	<the earth; is the center of; the universe>
	
但是这个三元组是事实吗？不一定。因为是前缀，**'Early scientists believed that'**，为此，希望抽取的内容是，

	(<the earth; be the center of; the universe>; AttributedTo believe; Early astronomers)
	
而这个方向主要解决的问题包括上述。在正在做的事实性错误检测的工作中，同样会面临该问题。

4.《Supervised Open Information Extraction》

建模为一个序列标注问题。输入输出如下：

![img2](http://wx4.sinaimg.cn/mw690/aba7d18bgy1g5dif9olm0j20u20aymzv.jpg)


5.《Neural Open Information Extraction》

建模为一个seq2seq问题。输入输出如下：

输入：

	deep learning is a subfield of machine learning

输出：

	<arg1>deep learning </arg1> <rel> is a subfield of </rel> <arg2> machine learning </arg2>
	
相关文章，《Extracting Relational Facts by an End-to-End Neural Model with Copy Mechanism》,ACL2018


6.《Open Information Extraction from Question-Answer Pairs》

用阅读理解的任务框架来做，本质上还是seq2seq的问题，输入输出如下：

![img3](http://wx1.sinaimg.cn/mw690/aba7d18bgy1g5dincsh3lj20hm07dta0.jpg)

其中输入是Q和A，输出是Tuple，Tuple中的SPO也可以添加\<arg1>,\<rel>,\<arg2>作为分隔符。

7.《Unsupervised Open Relation Extraction》

对relation进行clustering。

最后，周六愉快！我刷剧去了，《琅琊榜》是有点好看啊，逃。

8.[Knowledge Graphs in Natural Language Processing@ACL2019](https://medium.com/@mgalkin/knowledge-graphs-in-natural-language-processing-acl-2019-7a14eb20fce8)

9.[开放信息抽取的工作总结](https://github.com/gkiril/oie-resources#oie-systems-for-chinese-language)(非常全面的文献)






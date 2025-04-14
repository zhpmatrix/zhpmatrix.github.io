---
layout: post
title: "兜底哲学：规则引擎方法论"
tags: [NLP]
excerpt: "秋水共长天一色，模型与规则齐飞。"
date: 2020-10-21 17:58:00
mathjax: true
---

在之前的博客[冷启动，知多少？](https://zhpmatrix.github.io/2020/06/26/cold-start-in-dialogue/)中提到规则用于冷启动，在实际的工作中，多数算法同学是不乐意写规则的，在博主之前做中文纠错的时候，术语纠错子任务就是一个标准的规则系统。博主年少轻狂的时候，也曾怼过业界做知识图谱的一位相对有名的同学，认为搞规则很Low。

观察到在之前的同组同学的工作中，一个关于NER的工作，需要抽取四个字段。第一版方案是基于纯规则做的，ROI较低。第二版方案基于模型来做，指标上暴打第一版，实现成本还比较低。

但是从另外一个角度，引用一个朋友说的话：“没有写过一万条规则的人工智能系统，他是不敢用的。”。

有很多关于模型和规则的争议，使用模型是希望利用模型的泛化性，在保证高召回的前提下，希望保证高准确，但是由于泛化问题的存在，无法保证绝对的高准确。这个时候，虽然规则一般情况下的召回较低，但是准确性很高，因此在多数的实际业务服务中，可以看到模型+规则的组合服务模式，甚至在博主近期的一段经历中，在需要高准确的场景下，看到过基本整个算法团队都在写规则的情况，这也不足为怪了。

同样，在和一些做生成的团队交流的时候，虽然大家一直在研究生成的模型方案，但是实际上线的方案仍旧是基于模板的技术，模型只是在整个环节中的单点做贡献。

具体优缺点对比如下：

|方法|优点|缺点|
|------|------|------|
|模型|高召回，一定程度上的高准确，泛化能力|无法保证所有badcase的覆盖|
|规则|高准确，简单快速反馈|低召回，劳动密集型工作|
|模型+规则|理论上的高召回+高准确，快速反应能力|减缓模型迭代周期，加速规则迭代（比重提升）|

这篇博客主要梳理一些规则相关的方法论，笔者经验和观察有限，后续会进一步完善。

#### 词典怎么用

在多数的开源分词工具中，如Jieba和LAC等，都会提供用户自定义词典，主要解决的问题是在自定义词典中的词需要保证单独切分出来。这里需要考虑三个问题：第一，词典的获取；第二，词典的检索实现。第三，保证切分正确的实现；在LAC中，不仅提供了分词干预的功能，同时提供了NER的标注功能，虽然从建模角度，二者区分不大。

作为一个对外开放的工具，词典是由用户提供的。但是在多数场景下，词典的获取是知识沉淀的过程，可以借助新词发现技术，人工编纂，知识图谱映射等方式来获取。

假设词典很大，就需要提升检索的速度。常用的方式是基于AC自动机的实现（Trie树+KMP算法），相关开源实现较多。LAC中对于第一和第二的处理逻辑如下：

```
def load_customization(self, filename, sep=None):
        """装载人工干预词典"""
        self.ac = TriedTree()
        with open(filename, 'r', encoding='utf8') as f:
            for line in f:
                if sep == None:
                    words = line.strip().split()
                else:
                    sep = strdecode(sep)
                    words = line.strip().split(sep)

                if len(words) == 0:
                    continue

                phrase = ""
                tags = []
                offset = []
                for word in words:
                    if word.rfind('/') < 1:
                        phrase += word
                        tags.append('')
                    else:
                        phrase += word[:word.rfind('/')]
                        tags.append(word[word.rfind('/') + 1:])
                    offset.append(len(phrase))

                if len(phrase) < 2 and tags[0] == '':
                    continue

                self.dictitem[phrase] = (tags, offset)
                self.ac.add_word(phrase)
        self.ac.make()#构建ac自动机
```
上述逻辑之后，比较重要的是如何结合模型预测结果给出最终的预测结果（LAC中正是基于模型+规则的方式）。LAC中的实现如下：

```
def parse_customization(self, query, lac_tags):
        """使用人工干预词典修正lac模型的输出"""
        if not self.ac:
            logging.warning("customization dict is not load")
            return

        # FMM前向最大匹配
        ac_res = self.ac.search(query)

        for begin, end in ac_res:
            phrase = query[begin:end]
            index = begin

            tags, offsets = self.dictitem[phrase]
            for tag, offset in zip(tags, offsets):
                while index < begin + offset:
                    if len(tag) == 0:
                        lac_tags[index] = lac_tags[index][:-1] + 'I'
                    else:
                        lac_tags[index] = tag + "-I"
                    index += 1

            lac_tags[begin] = lac_tags[begin][:-1] + 'B'
            for offset in offsets:
                index = begin + offset
                if index < len(lac_tags):
                    lac_tags[index] = lac_tags[index][:-1] + 'B'


```
阅读源码可以发现，逻辑上是一个基于规则的修正。但是这里是分词，词性，NER三种，modeling上是一种任务，因此修正逻辑可以统一为一种。

#### 规则引擎

在LAC的加载词典过程中，可以看到涉及对词典的解析逻辑。实际上，这里正是一个mini型的加载引擎。官方定义的词典格式：

```
春天/SEASON
花/n 开/v
秋天的风
落 阳
```

默认要求：（1）每行一个item（2）用“/”分割phrase和tag（3）连续的phrase和tag组合用空格分开（4）tag可以确省

格式标准化之后，就可以开放给不懂具体技术的用户来完善词典。上述两段代码形成了一个常见的规则引擎的模式。三个要素如下：（1）标准化，易理解的用户输入模式（2）用户输入的加载解析逻辑（3）和上游模型的预测结果相融合的逻辑

思考的维度：（1）业务规则是多变的（2）规则可配置（3）界面友好

比如对话场景下的一个标准化方式：

```
Q:<PersonName>的生日是<Date>吗？
A:哥，我不敢认识<PersonName>.Value啊。
```

当Q中能够匹配上述模板的时候，就会把PersonName对应实体的Value作为A的可变值进行填充。在自然语言生成系统中，有基于模板的生成技术（上文提到的专家系统），要求由句子模板和词汇模板。下面是一个值得观察的询问天气场景中的模板（例子来自《自然语言处理实践-聊天机器人技术原理与应用》）：

其中，句子模板如下：

```
Topic->weather
	Act->query
		Content: weather\_state
			->3 对不起，请[<tell>]您需要[<refer>]{<where>}的[<what>]。
			->2 请[<tell>]您需要[<refer>]的[<what>|具体内容]。
			->1  抱歉，请[<tell>]您需要{<refer>}{(day)|今天|[when]}{(location)|当前城市|<where>}的[<what>]。
```

其中的符号说明：

```
|:或者
\[\]:内部元素出现次数>=1
{}:内部元素出现次数<=1
():对话管理模块的模板中的变量
<>:自定义语料中的变量
句子中的数字：该句子的权重，权重越大句子出现的可能性越大
```

词汇模板如下：

```
<tell>->[告诉我|补充|说明|输入]
<refer>->[查询|知道|获取|收到|了解|咨询]
<where>->[哪里|何处|什么位置|什么地方|什么城市|哪个位置|哪个区域]
<what>->[天气|哪方面信息|什么信息|哪方面情况|哪方面内容|什么内容]
<when>->[哪天|什么时间|哪个时辰|什么时候]
```

在其他的一些业务场景中，可能需要处理的情况较多，就需要对规则体系进行合理分层，设计的实现架构要能够灵活根据业务变化**可插拔**。在博主之前的关于SPO抽取的相关工作中，就对该特点要求严格。


#### 基础技术

核心逻辑仍旧是if-else，不过[正则表达式](https://regexr.com)也是重要工作。在LAC的工作中，暂时不支持正则表达式，比如通配符的支持是下一版要实现的，但是理论上应该不是一个困难的工作。写正则的一个关键点是：**服务hang死的问题**。虽然博主个人的经验不多，但是之前已经观察到组里两位同学的正则在面对一些特殊case处理的时候hang死的问题。

基础的词法，句法技术同样可以作为规则引擎的匹配输入信息。

规则是更靠近业务侧的，对于算法同学来说，经典的场景是要求业务反馈的badcase的快修复，复杂且多变。引擎是执行规则的解析器，需要理解规则，并给出相应结果。一般而言，从开发角度来说，如果是硬编码规则，每次规则的更新都需要重新走一遍发布流程，这个时候需要配置化。此外，对规则的管理也是需要考虑的重点问题。本质上，想要通过引擎将规则交给更靠近业务的同学，开发的同学专注引擎的工作。这篇文章站在算法同学的角度来理解规则引擎。从整体上看，NLP算法的历史经历了从规则（专家系统）到统计到深度，但是今天的算法业务系统，实则是深度或者统计+规则的组合，不唯深度论，也不唯规则论。

相关工作：

1.[从0到1：构建强大且易用的规则引擎](https://mp.weixin.qq.com/s/E-9GR0Mun1pudC0V1nXCsg)，美团的技术实践

2.[关于规则引擎](https://zhuanlan.zhihu.com/p/54133598)，总结了规则引擎的几个开源实现

3.[复杂风控场景下，如何打造一款高效的规则引擎](https://zhuanlan.zhihu.com/p/140916822)

4.[Should I use a Rules Engine?](https://martinfowler.com/bliki/RulesEngine.html)

5.[Stanford RegexNER](https://nlp.stanford.edu/software/regexner.html)，支持多种自定义NER的后处理规则（百度的LAC也同样支持，但是功能不如RegexNER），如下：

第一种（直接标注实体）：

```
Bachelor of Arts	DEGREE
Bachelor of Laws	DEGREE
```

第二种（或关系标注）：

```
Bachelor of (Arts|Laws|Science|Engineering|Divinity)	DEGREE
```

第三种（多标签标注）：

```
Bachelor of (Arts|Laws|Science|Engineering|Divinity)	DEGREE
Lalor	LOCATION	PERSON
Labor	ORGANIZATION
```

第四种（规则优先级）

```
Bachelor of (Arts|Laws|Science|Engineering|Divinity)	DEGREE		2.0
Lalor	LOCATION	PERSON
Labor ORGANIZATION
Bachelor of Arts	EASY_DEGREE
Bachelor of Laws	HARD_DEGREE		3.0
```

6.[Stanford TokensRegex](https://nlp.stanford.edu/software/tokensregex.html#TokensRegexPatterns)，是RegexNER更底层的实现，更加灵活的同时，也更加的复杂。
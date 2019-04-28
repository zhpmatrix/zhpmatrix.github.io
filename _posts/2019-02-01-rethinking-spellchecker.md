---
layout: post
title: "[NLP]中文拼写检纠错-和百度比一比"
excerpt: "在文本纠错任务上，用自己的模型和百度API开放的接口测试效果对比。"
date: 2019-02-01 18:00:00
mathjax: true
---

最近在调研一些公司的云平台对外开放的NLP相关的API接口，无意间看到参考1的总结说明。文章中提到百度的文本纠错API是免费使用的，腾讯虽然也有文本纠错的API，但是需要付费。其实实习期间就有关注到百度的开放接口，不过实习期间正值该接口属于内测阶段，当时的目的也是自研而非使用第三方接口，于是一直没有机会尝试。在主要参考列表中，给出了三家平台的入口地址。

既然百度的可用，那就和自己的模型PK一下好了。之前写过一篇[博客](https://zhpmatrix.github.io/2018/12/17/chinese-spell-checker/)，总结了在中文文本纠错上的尝试。

这个可以使用的API接口可以用于很多地方，因此在此记录一下使用流程。

第一，注册百度云账号，按照官网文档，得到应用的AppID，API Key，和Secret Key三个值；

第二，pip install baidu-aip；

官网提供了更具体的使用说明，同时也支持多种语言，多种调用方式，具体可查文档。不过上述两步已经满足我自己的需求了。值得一提的是，创建应用默认支持十六种语言处理基础技术，个人认为常见的基本功能，如分词，词向量，情感分析等都已经包含在内，是比较齐全的API支持。

不过考察文本纠错的API，有两个显然的缺点：

第一，待纠错文本的输入限制为511字节；

第二，API的QPS=5，申请更高QPS需要公司申请；

接下来，可以开心的PK一把了。测试代码如下(使用其他的功能，用法类似)：

```

from aip import AipNlp
app_id      =   '15520629'
api_key     =   'bndhUzrh1iDasRhBxe2Objn6'
secret_key  =   '应该不能告诉你'

client = AipNlp(app_id, api_key, secret_key)


text_list = ['形像代言人',
            '此事不会影像中国关系大局',
            '化夏子孙团结一心',
            '就难免必理不平衡。',
            '西藏叛乱的失败，使尼赫鲁“大印度联邦”的构想华为泡影。',
            '看看人家，不给钱就酸了，因为你缺的那个敬业福。',
            '甚至龙族的秘密歪斜也没有关系。',
            '我们会优先推动五大创新研发计画。',
            '说自己市提前两天排对的。',
            '等啊等，忠于等到了。',
            '还有进口香皂、家居服、花艺样样聚全。',
            '“蒙汉药!”加尼马尔恍然大悟，他费了九牛二虎之力，终于把他的助手弄醒。',
            '好象是我们错了。',
            '人群中发出一阵惊吁声。',
            '清河安宁庄西二条路人形步道翻修！',
            '看来生活中也是蛮回撒娇的呢。',
            '还可能与这个小村落与比斯特购物村想去不远也不无关系。']

print(len(text_list))

for text in text_list:
    print(client.ecnet(text))

```

共测试出了六句错误。具体输出结果如下，

```

{'log_id': 923607537112811327, 'item': {'vec_fragment': [{'ori_frag': '形像', 'begin_pos': 0, 'correct_frag': '形象', 'end_pos': 4}], 'score': 0.947005, 'correct_query': '形象代言人'}, 'text': '形像代言人'}
{'log_id': 720482710083012319, 'item': {'vec_fragment': [], 'score': 0, 'correct_query': '此事不会影像中国关系大局'}, 'text': '此事不会影像中国关系大局'}
{'log_id': 4566419717022875711, 'item': {'vec_fragment': [{'ori_frag': '化夏', 'begin_pos': 0, 'correct_frag': '华夏', 'end_pos': 4}], 'score': 0.885656, 'correct_query': '华夏子孙团结一心'}, 'text': '化夏子孙团结一心'}
{'log_id': 3083782733138639839, 'item': {'vec_fragment': [], 'score': 0, 'correct_query': '就难免必理不平衡。'}, 'text': '就难免必理不平衡。'}
{'log_id': 3000122787598459551, 'item': {'vec_fragment': [], 'score': 0, 'correct_query': '西藏叛乱的失败，使尼赫鲁“大印度联邦”的构想华为泡影。'}, 'text': '西藏叛乱的失败，使尼赫鲁“大印度联邦”的构想华为泡影。'}
{'log_id': 4761456975244649855, 'item': {'vec_fragment': [], 'score': 0, 'correct_query': '看看人家，不给钱就酸了，因为你缺的那个敬业福。'}, 'text': '看看人家，不给钱就酸了，因为你缺的那个敬业福。'}
{'log_id': 1748021891136513983, 'item': {'vec_fragment': [], 'score': 0, 'correct_query': '甚至龙族的秘密歪斜也没有关系。'}, 'text': '甚至龙族的秘密歪斜也没有关系。'}
{'log_id': 3357462939325308255, 'item': {'vec_fragment': [{'ori_frag': '计画', 'begin_pos': 26, 'correct_frag': '计划', 'end_pos': 30}], 'score': 0.508583, 'correct_query': '我们会优先推动五大创新研发计划。'}, 'text': '我们会优先推动五大创新研发计画。'}
{'log_id': 1449603895071567359, 'item': {'vec_fragment': [{'ori_frag': '排对', 'begin_pos': 16, 'correct_frag': '排队', 'end_pos': 20}], 'score': 0.985248, 'correct_query': '说自己市提前两天排队的。'}, 'text': '说自己市提前两天排对的。'}
{'log_id': 5453831342972440127, 'item': {'vec_fragment': [], 'score': 0, 'correct_query': '等啊等，忠于等到了。'}, 'text': '等啊等，忠于等到了。'}
{'log_id': 5485571345359476351, 'item': {'vec_fragment': [], 'score': 0, 'correct_query': '还有进口香皂、家居服、花艺样样聚全。'}, 'text': '还有进口香皂、家居服、花艺样样聚全。'}
{'log_id': 7264480693643118687, 'item': {'vec_fragment': [], 'score': 0, 'correct_query': '“蒙汉药!”加尼马尔恍然大悟，他费了九牛二虎之力，终于把他的助手弄醒。'}, 'text': '“蒙汉药!”加尼马尔恍然大悟，他费了九牛二虎之力，终于把他的助手弄醒。'}
{'log_id': 6925038357614324767, 'item': {'vec_fragment': [{'ori_frag': '好象是', 'begin_pos': 0, 'correct_frag': '好像是', 'end_pos': 6}], 'score': 0.945305, 'correct_query': '好像是我们错了。'}, 'text': '好象是我们错了。'}
{'log_id': 6186454006876672831, 'item': {'vec_fragment': [{'ori_frag': '吁声', 'begin_pos': 16, 'correct_frag': '嘘声', 'end_pos': 20}], 'score': 0.502987, 'correct_query': '人群中发出一阵惊嘘声。'}, 'text': '人群中发出一阵惊吁声。'}
{'log_id': 4001481984683291871, 'item': {'vec_fragment': [], 'score': 0, 'correct_query': '清河安宁庄西二条路人形步道翻修！'}, 'text': '清河安宁庄西二条路人形步道翻修！'}
{'log_id': 3198382055969640639, 'item': {'vec_fragment': [], 'score': 0, 'correct_query': '看来生活中也是蛮回撒娇的呢。'}, 'text': '看来生活中也是蛮回撒娇的呢。'}
{'log_id': 6048855618626746847, 'item': {'vec_fragment': [], 'score': 0, 'correct_query': '还可能与这个小村落与比斯特购物村想去不远也不无关系。'}, 'text': '还可能与这个小村落与比斯特购物村想去不远也不无关系。'}

```

由此可以得出基本的结果：忽略测试集规模的影响，我们之前做的结果，分别基于统计语言模型和生成模型的结果都要比百度文本纠错API的测试结果好许多。

从上述的对比过程，有几点想法或者是启发：

第一，当不知道一个任务的上限在哪里，或者自己做的任务的效果怎样的时候，可以和百度开放的API做对比，对自己的模型效果做一个大致的评估，同时可以用于评估任务的难易程度，这点很重要。

第二，从API的反馈结果，有可能逆推出百度API背后的支持模型或者解决问题的具体方法，这点也很重要。

第三，十七句能够纠错出六句，我不太能接受，但是百度API为啥开放出这个接口？SLM和基于生成的模型在更大的数据规模上取得增益的同时，在该测试集上也会取得比上述测试结果更好的结果，但是我个人仍然认为这两个模型不可用。

初步结论暂且这样，后续科学评估需要在更大的测试集上做。但是即使规模上去了，百度API的测试集和自己做的测试集是否具有可比性，也是需要考虑的问题。因为，针对文本纠错任务，大规模的测试集应该是按照某种规则人工做出来的，否则没有标签啊。

总结：写这样的博客也算是换个脑子，换个视角，个人感觉还挺有意思的。

补充：

1.百家号的语句纠错

![img](http://wx1.sinaimg.cn/mw690/aba7d18bly1g1ak929kjgj21400u04qq.jpg)

2.[阿里将纠错用于OCR任务中-单证业务](https://102.alibaba.com/detail?id=223)


主要参考：

1.[BAT三家NLP的API对比与使用/价格分析以及选取](https://ptorch.com/news/178.html)

2.[百度AI开放平台](http://ai.baidu.com/docs#/NLP-API/57b9b630)

3.[腾讯文智自然语言处理](https://cloud.tencent.com/document/product/271/2050)

4.[阿里云自然语言处理](https://help.aliyun.com/product/60058.html)

5.[调用百度自然语言处理API](https://blog.csdn.net/yang_daxia/article/details/86028619)

6.[告诉你一个写外语避免常见错误的使用技巧](https://liweinlp.com/?p=5000)

7.[百度中文文本纠错技术](https://mp.weixin.qq.com/s?__biz=MzU1NTMyOTI4Mw==&mid=2247488610&idx=1&sn=c8793392f789ba5c39a9e8a4d7c6beac&chksm=fbd4a60ecca32f184b19aac505aeb10b282cb12ff6b84b712e4038d856ed21d4cb6064546a9e&mpshare=1&scene=23&srcid=03064sSimcEBAnYxk9ZsG5By%23rd)

8.[2018-新媒体纠错指南](https://mp.weixin.qq.com/s?__biz=MzU3NzUzNjg2MA==&mid=2247483741&idx=2&sn=6fc2b06fca519bcd127eb4938388c6ef&chksm=fd02576eca75de780d2e3cd3a59c39b257eccf85525da83febbab7fe239461da2c6ce7a9615e&mpshare=1&scene=23&srcid=0428Dfx3CtCUMe21q1GyyKTl%23rd)









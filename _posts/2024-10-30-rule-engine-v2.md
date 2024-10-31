---
layout: post
comments: true
title:  "[Python]再议规则引擎"
excerpt: "一种支持系统可扩展性的实现方式"
date:   2024-10-30 10:35:00
mathjax: true
---

### 前言

既上一篇讨论规则引擎的文章[兜底哲学:规则引擎方法论](https://zhpmatrix.github.io/2020/10/21/rule-is-all-you-need/)，转眼已经过去了四年。这篇文章是笔者最近围绕规则引擎的实践和思考。

### 业务场景

在围绕知识中台构建知识资产时，需要对知识文书打标签，由于需要实现的标签非常多，每个标签的代码实现类似如下:

```
  if check_words_exist(attachment_content,
                ["未开具发票","不列收入","少列收入","少计销售收入","少计销售货物收入","未入账收入","未入账含税收入","少申报收入","收入未列","未申报确认收入","未作视同销售处理","账外收入"]) or \
                check_two_words_exist(attachment_content,
                                    "销售货物",
                                    "未申报",
                                    20) or \
                check_two_words_exist(attachment_content,
                                    "少计",
                                    "收入",
                                    20) or \
                check_two_words_exist(attachment_content,
                                    "少记",
                                    "收入",
                                    20) or \
                check_two_words_exist(attachment_content,
                                    "收入",
                                    "未列",
                                    20) or \
                check_two_words_exist(attachment_content,
                                    "收入",
                                    "未入",
                                    20) or \
                check_three_words_exist(attachment_content,["未","申报","收入"],[20,20]) or \
                check_three_words_exist(attachment_content,["未","确认","收入"],[20,20]) or \
                check_three_words_exist(attachment_content,["收入","未","申报"],[20,20]):
                label_mapping["隐瞒收入"] = True
            if check_words_exist(attachment_content,
                ["私账","个人银行帐号","个人银行账户","微信","信用卡","私人账户","账外收入"]             
                                 ):
                label_mapping["公转私/个人卡"]=True
            if check_words_exist(attachment_content,["个人所得税"]):
                label_mapping["未缴或少缴个人所得税"] = True
            if (doc_type == "重大税收违法失信主体通知书" and check_two_words_exist(case_fea_paragraph,"虚开","抵扣",50)) or \
                (doc_type != "重大税收违法失信主体通知书" and check_two_words_exist(attachment_content,"虚开","抵扣",50)) or \
                (doc_type != "重大税收违法失信主体通知书" and check_words_exist(attachment_content,["让他人为自己开具","向你公司开具","开具给你公司","取得他人虚开"])) or \
                (doc_type != "重大税收违法失信主体通知书" and check_three_words_exist(attachment_content,["取得","开具","发票"],[20,20])) or \
                (doc_type != "重大税收违法失信主体通知书" and check_three_words_exist(attachment_content,["接受","开具","发票"],[20,20])) or \
                (doc_type != "重大税收违法失信主体通知书" and check_three_words_exist(attachment_content,["接受","虚开","发票"],[20,20])):
                label_mapping["虚开发票-申报抵扣"] = True
            if check_two_words_exist(attachment_content,"开具与实际经营业务情况不符","发票",50) or \
               check_two_words_exist(attachment_content,"代开与实际经营业务情况不符","发票",50) or \
               check_words_exist(attachment_content,["对外虚开","对外开具"]) or \
               check_two_words_exist(attachment_content,"你公司向","开具",50) or \
               check_two_words_exist(attachment_content,"开具给","发票",50) or \
               custom_check_type(attachment_content,"你公司","开具","发票") or \
               custom_check_type(attachment_content,"你单位","开具","发票") or \
               (check_two_words_exist(attachment_content,"虚开","发票",50) and label_mapping["虚开发票-申报抵扣"] == False):
                label_mapping["虚开发票-对外虚开"] = True
            if (doc_type == "重大税收违法失信主体通知书" and check_words_exist(case_fea_paragraph,["骗取出口退税"])) or \
                (doc_type == "重大税收违法失信主体通知书" and check_words_exist(illfact_paragraph,["骗取出口退税"])) or \
                (doc_type != "重大税收违法失信主体通知书" and check_words_exist(attachment_content,["出口"])) or \
                (doc_type != "重大税收违法失信主体通知书" and check_two_words_exist(attachment_content,"虚开发票","申报出口退税",50))  or \
                  (doc_type != "重大税收违法失信主体通知书" and check_two_words_exist(attachment_content,"骗取","出口退税",50)): 
                label_mapping["骗取出口退税"] = True
            if (doc_type == "重大税收违法失信主体通知书" and check_words_exist(case_fea_paragraph,["少缴","未缴","逃避缴纳","偷税","逃避追缴欠税"])) or \
                (doc_type == "重大税收违法失信主体通知书" and check_words_exist(illfact_paragraph,["少缴","未缴","逃避缴纳","偷税","逃避追缴欠税"])) or \
                (doc_type != "重大税收违法失信主体通知书" and check_words_exist(attachment_content,["少缴","未缴","逃避缴纳"])):
                label_mapping["少缴应纳税款"] = True
            if doc_type == "催告书":label_mapping["强制执行"] = True

```

每个标签的实现都需要开发者和业务方共同参与，经过多轮的口径调整和实现调整，直到标签的实现在召回率和精确率上达到预期水平。

因此，笔者就会思考问题如下：

+ 这是否是一个可以通过规则引擎实现口径开发和代码开发解耦的场景？

+ 能否利用LLM的能力实现打标签？（规则引擎只有一个operator，就是llm）

### 实现过程

首先，需要一个笔者能够handle的规则引擎，要求基于python实现，整个开源社区基于python的规则引擎比较少，幸运的是找到了**business_rule**，一个多年前的基于python的规则引擎，虽然star不多，不过完美满足自己的需求，能够在支持condition和action创建，定义operator，通过all和any实现chain，同时带有一个异常简陋的交互式UI。通过增加llm作为operator，实现了面向业务的快速适配。实现效果如下：


<img src="https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/tag_factory_v0.gif?raw=true" width="400" align="center"/>

上述工作称为tag
\_factory\_v0，仍然属于传统规则引擎。[knowledge_table](https://knowledge-table-demo.whyhow.ai/)是近期的一个工作，通过结合llm和rule做dataframe的处理，在交互设计上非常具有启发性。比如通过定义@作为对dataframe的列的引用，一定程度上可以解决标签开发过程中的标签依赖问题。knowledge_table也采用了Python作为后端开发语言，整体代码的质量非常高，但是直接用于笔者的场景，又显得过重。因此笔者基于gradio通过不同的方式实现了类似knowledge\_table的交互效果，实用性显著提升，记为tag\_factory\_v1，实现效果如下所示：

<img src="https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/tag_factory.gif?raw=true" width="400" align="center"/>

进一步地，回到更加灵活的规则引擎方向上，通过拖拽的方式快速拖出来一个DAG是一个极其重要的模块，称为引擎前端。解析DAG并调度运行+运维?是引擎后端。单独两块工作分别拉出来都有不错的开源的工作，但是合并在一起的工作并不多。

滴滴开源的LogicFlow可以作为一个引擎前端，Dagu作为引擎前端，可以实现DAG和Yaml的双向映射，Yaml是Python开发者的福音。开源版n8n作为前端，对于operator的支持更加的丰富，包括HTTP请求，函数，外部服务，任务等，效果如下：

<img src="https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/n8n.png?raw=true" width="400" align="center"/>

其中HTTP Request的编辑逻辑如下：

<img src="https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/n8n_http.png?raw=true" width="400" align="center"/>


apache-airflow作为引擎后端，能够将Python代码转化为DAG，同时实现DAG的调度和监控，但是没有搭配一个好的前端。DophinScheduler作为为数不多的同时拥有前端和后端的可以作为理想规则引擎的框架，但是近期看到mlflow把DS的前端拆出来，融合实现ML工作流的编排和调度，毕竟mlflow在机器学习任务的编排上比DS要做的更好（定位不同）。

因此，如果有tag\_factory\_v2的话，整体上可行的思路如下：

+ 和v1类似，独立开发一套适配业务的框架（operator定义清晰的话，ROI也很高）

+ 采用DS。强化版可以采用类似mlflow+DS的组合

+ 前端和后端分离。比如n8n+airflow的组合

### 后记

在调研和实现过程中发现的一个认知问题是：在过去的一些年，过于关注开源产品了。客观角度上看，闭源产品的产品力和技术力应该更好才对，比如这里的n8n。

在玄难的[面向不确定性的软件设计几点思考](https://www.jiqizhixin.com/articles/2018-12-12-5)中提到，整体的演化方向是从“确定性边界向内归纳抽象找相同”转化为“确定性内核向外生长演化”，而对于规则引擎而言同时包含两个特点。
 
### 参考资料

+ [How to scrape data from a website](https://blog.n8n.io/how-to-scrape-data-from-a-website/)


**[扫码加笔者好友](https://zhpmatrix.github.io/about/)，茶已备好，等你来聊~**

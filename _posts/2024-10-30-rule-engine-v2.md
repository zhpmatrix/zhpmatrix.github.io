---
layout: post
comments: true
title:  "[Python]再议规则引擎"
excerpt: ""
date:   2024-10-30 10:35:00
mathjax: true
---

前言：

既上一篇讨论规则引擎的文章[兜底哲学:规则引擎方法论](https://zhpmatrix.github.io/2020/10/21/rule-is-all-you-need/)，转眼已经过去了四年。这篇文章是笔者最近围绕规则引擎的实践和思考。

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

首先，需要一个笔者能够handle的规则引擎，要求基于python实现，整个开源社区基于python的规则引擎比较少，幸运的是找到了**business_rule**，一个多年前的基于python的规则引擎，虽然star不多，不过完美满足自己的需求，能够在支持condition和action创建，定义operator，通过all和any实现chain，同时带有一个异常简陋的交互式UI。通过增加llm作为operator，实现了面向业务的快速适配。




**[扫码加笔者好友](https://zhpmatrix.github.io/about/)，茶已备好，等你来聊~**

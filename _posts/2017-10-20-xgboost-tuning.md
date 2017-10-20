---
layout: post
title: "[ML]AwesomeXGBoost-炼丹秘籍"
excerpt: "这篇博客是为了配合组会做XGBoost的论文报告，包括XGBoost的基本超参数调节，自定义目标函数和度量函数，特征重要性，决策树绘制和保存，特征离散化。"
date: 2017-10-19 14:12:00
mathjax: true
---

前言：这篇博客是从jupyter notebook文档直接转换为markdown得到，相关资源如下。

[本篇博客的在线notebook](https://nbviewer.jupyter.org/github/zhpmatrix/awesome-xgb/blob/master/AwesomeXGBoost.ipynb)

[Github代码地址](https://github.com/zhpmatrix/awesome-xgb)

## XGBoost基本参数调节

参考：

[Hyperparameter tuning in XGBoost](https://cambridgespark.com/content/tutorials/hyperparameter-tuning-in-xgboost/index.html)

这篇博客是native XGBoost API

[Get started with XGBoost](https://cambridgespark.com/content/tutorials/getting-started-with-xgboost/index.html)

这篇博客是sklearn API

[Complete Guide to Parameter Tuning in XGBoost(with codes in Python)](https://www.analyticsvidhya.com/blog/2016/03/complete-guide-parameter-tuning-xgboost-with-codes-python/)

这篇博客是sklearn API

## 使用XGBoost自定义目标函数和评估函数


```python
import numpy as np
import xgboost as xgb
from sklearn import metrics
###
# advanced: customized loss function
#
print ('start running example to used customized objective function')

dtrain = xgb.DMatrix('data/agaricus.txt.train')
dtest = xgb.DMatrix('data/agaricus.txt.test')

# note: for customized objective function, we leave objective as default
# note: what we are getting is margin value in prediction
# you must know what you are doing
param = {'max_depth': 4, 'eta': 0.8}
watchlist = [(dtest, 'eval'), (dtrain, 'train')]
num_boost_round = 4

# user define objective function, given prediction, return gradient and second order gradient
# this is log likelihood loss
def logregobj(preds, dtrain):
    labels = dtrain.get_label()
    preds = 1.0 / (1.0 + np.exp(-preds))
    grad = preds - labels
    hess = preds * (1.0-preds)
    return grad, hess

# user defined evaluation function, return a pair metric_name, result
# NOTE: when you do customized loss function, the default prediction value is margin
# this may make builtin evaluation metric not function properly
# for example, we are doing logistic loss, the prediction is score before logistic transformation
# the builtin evaluation error assumes input is after logistic transformation
# Take this in mind when you use the customization, and maybe you need write customized evaluation function

def evalerror(preds, dtrain):
    labels = dtrain.get_label()
    # return a pair metric_name, result
    # since preds are margin(before logistic transformation, cutoff at 0)
    return 'error', float(sum(labels != (preds > 0.0))) / len(labels)

# training with customized objective, we can also do step by step training
# simply look at xgboost.py's implementation of train
bst = xgb.train(param, dtrain, num_boost_round, watchlist, logregobj, evalerror)
bst.predict(dtest)
```

    start running example to used customized objective function
    [0]	eval-error:0.007449	train-error:0.006756
    [1]	eval-error:0	train-error:0.001228
    [2]	eval-error:0	train-error:0
    [3]	eval-error:0	train-error:0





    array([-4.17207384,  4.17381191, -4.17207384, ...,  4.34276581,
           -3.77458525,  4.34276581], dtype=float32)



## 模型持久化(模型载入载出)


```python
bst.save_model('0001.model')

bst = xgb.Booster({'nthread': 4})  # init model
bst.load_model('0001.model')  # load data
bst.predict(dtest)
```




    array([-4.17207384,  4.17381191, -4.17207384, ...,  4.34276581,
           -3.77458525,  4.34276581], dtype=float32)



参考：

[XGBoost原生API漫步](http://xgboost.readthedocs.io/en/latest/python/python_intro.html)

## 利用XGBoost生成新特征和特征离散化


```python
import pandas as pd
import numpy as np  
from sklearn import metrics  
from sklearn.datasets import make_hastie_10_2
from sklearn.model_selection import train_test_split  
from xgboost.sklearn import XGBClassifier  


#生成二分类数据集(10个特征)
X, y = make_hastie_10_2(random_state=0)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)
X_train_1, X_train_2, y_train_1, y_train_2 = train_test_split(X_train, y_train, test_size=0.6, random_state=0)  

```

### 数据集划分

训练集1+训练集2=0.9 * 全部数据集

训练集2 = 0.6 * （训练集1 + 训练集2）

![数据集划分](http://wx3.sinaimg.cn/mw690/aba7d18bgy1fknspkf4jjj20fu01ydfp.jpg)

### 利用训练集1训练分类器


```python
clf = XGBClassifier(  
    learning_rate =0.2,  
    n_estimators=200,
    max_depth=8,  
    min_child_weight=10,  
    gamma=0.5,  
    subsample=0.75,  
    colsample_bytree=0.75,  
    objective= 'binary:logistic',
    nthread=8,
    scale_pos_weight=1,  
    reg_alpha=1e-05,  
    reg_lambda=10, 
    seed=0)
        
clf.fit(X_train_1, y_train_1)
```




    XGBClassifier(base_score=0.5, colsample_bylevel=1, colsample_bytree=0.75,
           gamma=0.5, learning_rate=0.2, max_delta_step=0, max_depth=8,
           min_child_weight=10, missing=None, n_estimators=200, nthread=8,
           objective='binary:logistic', reg_alpha=1e-05, reg_lambda=10,
           scale_pos_weight=1, seed=0, silent=True, subsample=0.75)



### 特征离散化和特征合并


```python
new_feature= clf.apply(X_train_2)  
X_train_new2 = np.hstack((X_train_2, new_feature))
new_feature_test= clf.apply(X_test)  
X_test_new = np.hstack((X_test, new_feature_test))
```

---

提示：矩阵合并(ndarray)

1.两个矩阵的横/纵合并: 

    D = np.hstack((A,B))   
    
    D = np.vstack((A,B))

2.多个矩阵的横/纵合并:
    
    C = np.concatenate((A,B,B,A), axis=0)
    
    C = np.concatenate((A,B,B,A), axis=1)
    
---

### 获取训练集2的AUC和准确度


```python
model = XGBClassifier(  
    learning_rate=0.05,
    n_estimators=300,  
    max_depth=7,  
    min_child_weight=1,  
    gamma=0.5,  
    subsample=0.8,  
    colsample_bytree=0.8,  
    objective= 'binary:logistic', 
    nthread=8,  
    scale_pos_weight=1,  
    reg_alpha=1e-05,  
    reg_lambda=1,  
    seed=0) 

model.fit(X_train_2, y_train_2)  
y_pre= model.predict(X_test)  
y_pro= model.predict_proba(X_test)[:,1]   

print("AUC Score :",(metrics.roc_auc_score(y_test, y_pro)))   
print("Accuracy :",(metrics.accuracy_score(y_test, y_pre)))  
```

    AUC Score : 0.988763545429
    Accuracy : 0.931666666667


### 获取训练集2(合并离散特征)的AUC和准确度


```python
model = XGBClassifier(  
    learning_rate =0.05,
    n_estimators=300,
    max_depth=7,  
    min_child_weight=1,  
    gamma=0.5,  
    subsample=0.8,  
    colsample_bytree=0.8,  
    objective= 'binary:logistic',
    nthread=8,
    scale_pos_weight=1,  
    reg_alpha=1e-05,  
    reg_lambda=1,  
    seed=0) 

model.fit(X_train_new2, y_train_2)  
y_pre= model.predict(X_test_new)  
y_pro= model.predict_proba(X_test_new)[:,1]   
print("AUC Score :",(metrics.roc_auc_score(y_test, y_pro)))   
print("Accuracy :",(metrics.accuracy_score(y_test, y_pre)))

```

    AUC Score : 0.987232564601
    Accuracy : 0.939166666667


---

提示：

    1.合并离散特征后准确度有所提升(未调参)。
    
    2.特征离散化的一种方式。
    
参考：

《Practical Lessons from Predicting Clicks on Ads at Facebook》

---

### 使用XGBoost原生接口生成新特征


```python
import xgboost as xgb
dtrain = xgb.DMatrix('data/agaricus.txt.train')
dtest = xgb.DMatrix('data/agaricus.txt.test')

param = {'max_depth':4,
         'eta':0.8,
         'objective':'binary:logistic'}

watchlist  = [(dtest,'eval'), (dtrain,'train')]
num_boost_round = 3
bst = xgb.train(param, dtrain, num_boost_round,watchlist)

print ('start testing predict the leaf indices')
### predict using first 2 tree
leafindex = bst.predict(dtest, ntree_limit=2, pred_leaf=True)
print(leafindex.shape)
print(leafindex)
### predict all trees
leafindex = bst.predict(dtest, pred_leaf = True)
print(leafindex.shape)
```

    [0]	eval-error:0.007449	train-error:0.006142
    [1]	eval-error:0	train-error:0.000614
    [2]	eval-error:0	train-error:0.000614
    start testing predict the leaf indices
    (1611, 2)
    [[10 10]
     [13  7]
     [10 10]
     ..., 
     [13  7]
     [15 14]
     [13  7]]
    (1611, 3)


---

## 使用XGBoost获取特征重要性

提示:
    
    1. kernel=Python2.7, 添加代码%matplotlib inline
    
    2. kernel=Python3.0, 不需要添加1.的代码，图片风格和1.不同且Python3.0更好
    
---


```python
%matplotlib inline
import matplotlib.pyplot as plt

ax=xgb.plot_importance(bst)
plt.show()
```


![png](http://wx3.sinaimg.cn/mw690/aba7d18bgy1fknwvh0826j20ca07t0sr.jpg)


---

## 使用XGBoost绘制和存储决策树

提示:

    1. kernel=Python2.7环境下运行，添加代码%matplotlib inline
    
    2. kernel=Python3.0，报错：You must install graphviz to plot tree(在MAC OS X系统下尚未解决且不打算解决)

---



```python
ax = xgb.plot_tree(bst)
plt.show()
```


![png](http://wx4.sinaimg.cn/mw690/aba7d18bgy1fknwvhfausj207n074aa5.jpg)



```python
import codecs
f = codecs.open('xgb_tree.png', mode='wb')
g = xgb.to_graphviz(bst)
f.write(g.pipe('png'))
f.close()
```

---
layout: post
title: "[ML]HandsomeXGBoost"
excerpt: ""
date: 2017-10-19 20:16:00
mathjax: true
---

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

### 利用训练集1训练clf


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

```


```python
import xgboost as xgb

dtrain = xgb.DMatrix('data/agaricus.txt.train')
dtest = xgb.DMatrix('data/agaricus.txt.test')

param = {'max_depth':2,
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


```python

```


```python

```


```python

```


```python

```


```python

```


```python

```


```python

```


```python

```


```python

```


```python

```


```python

```


```python

```

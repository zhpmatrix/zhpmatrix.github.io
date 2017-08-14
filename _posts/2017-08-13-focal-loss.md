---
layout: post
title: "[paper]针对密集目标检测的焦点损失函数"
excerpt: "这是何凯明老师团队8月7日挂在arXiv的一篇文章，文章原名《Focal Loss for Dense Object Detection》，恰逢我们在做的一个NLP的比赛遇到不平衡问题，小林师兄就提到这篇文章，但是苦于BigDL有点儿坑，在自定义loss的时候学习成本略大，就没用到比赛中(其实就是懒)，今天读读文章，还是有启发的。"
data: 2017-08-13 08:58
mathjax: true
---

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

关于问题提出的背景，想法直觉，实验验证等内容可以具体读论文，这篇博客只讨论Focal Loss的问题，也就是怎样将不平衡性引入到loss函数的讨论中。

对于二分类问题，交叉熵损失函数如下：

$$
CE(p,y)=
\begin{cases}
    -log(p)\quad\quad   if\quad y = 1\\\\
    -log(1-p)\quad otherwise.
\end{cases}
$$

其中\\(p\in[0,1]\\)是模型预测类标签为1的概率(sigmoid函数),\\(y\\)是真实标签，其中\\(y\in\\{+1,-1\\}\\)。在文章中，作者简化写法如下：

$$
p_{t}=
\begin{cases}
    p\quad\quad   if\quad y = 1\\\\
    1-p\quad otherwise.
\end{cases}
$$

其中\\(CE(p,y)=CE(p_{t})=-log(p_{t})\\)

为了解决正负样本不均衡的问题，在loss函数中引入参数\\(\alpha_{t}\\),如下：

$$CE(p_{t})=-\alpha_{t} log(p_{t})$$

其中，对类标签为1的样本，\\(\alpha_{t}=\alpha,\alpha\in[0,1]\\),对类标签为-1的样本，\\(\alpha_t = 1 - \alpha\\)。为什么这种方式可以解决正负样本不平衡的问题？

假设1类样本比-1类样本多好多，则可以设\\(\alpha\in[0,0.5]\\)，这样就可以减少1类样本对loss函数的误差贡献，相对的，-1类样本的贡献增加。

为了解决难易分类样本对loss函数权重贡献的问题，在loss函数中引入参数\\(\gamma\\)和项\\((1-p_{t})^\gamma\\)，自认为难分的样本容易被错分，常被错分的样本比较难分，对于易分样本，同理。

$$FL(p_{t})=-(1-p_{t})^\gamma log(p_{t})$$

为啥可行呢？(假设\\(\gamma=1\\))

\\(y=1\\)时，当样本被错分，则\\(p_{t}=p\leq 0.5\\),故\\((1-p_{t})接近1\\)，对loss函数的值贡献大；当样本被正分，则\\(p_{t}=p\geq 0.5\\),故\\((1-p_{t})接近0\\)，对loss函数的值贡献小。

当\\(y=-1\\)时，结论显然。

假设\\(\gamma=0\\),退化为传统交叉熵函数。在这里，关于\\(\gamma\\)这个参数，至少可以看到两点：第一保证了FL和CE的一脉相承，第二对\\((1-p_{t})\\)的数值意义。

此处，有木有想到万有引力公式的发现？是的，乘在一块儿就OK！当当当，我们的Focal Loss函数闪亮登场：

$$FL(p_{t})=-\alpha_{t}(1-p_{t})^\gamma log(p_{t})$$

总结：其实，关于不平衡学习的研究成果已经有好多，在我的这篇[博客](https://zhpmatrix.github.io/2017/02/20/learning-from-imbalanced-data/)中，就写了一篇关于不平衡处理的review的论文笔记，在这篇文章中，作者总结提到Cost Sensitive Method即代价敏感方法及其具体例子，在我看来，Focal Loss也是一种具体的代价敏感方法，将正负样本的不均衡性，同时将难易样本的不均衡性引入到目标函数中，并且通过naive的方法进行目标函数的构造。难能可贵的地方在于从解决的具体问题中能够洞察到问题本质，比如观察分析出One-stage Detectors的Accuracy不能提升的原因之一是样本不平衡问题，然后用简单漂亮的方法去解决。关于这个方法能否用到其他的应用场景中，还有待讨论。

同时提供一些别人的讨论：

1.[Focal Loss](http://blog.csdn.net/u014380165/article/details/77019084)

2.[何凯明团队提出Focal Loss，目标检测精度打破现有记录](https://baijiahao.baidu.com/s?id=1575357531487121&wfr=spider&for=pc)

3.[知乎关于这篇paper的讨论](https://www.zhihu.com/question/63581984)






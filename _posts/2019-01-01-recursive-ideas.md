---
layout: post
title: "[LeetCode]重说：递归"
excerpt: "最近读组里同学代码的时候，看到一个递归实现。于是借助这篇短文，回顾一些关于递归的问题。"
date: 2019-01-01 18:53:00
mathjax: true
---

**总结：**

（1）从问题的形式上来看，倾向于得到所有的解/一个解（可能的）。比如，[所有可能的满二叉树](https://leetcode-cn.com/problems/all-possible-full-binary-trees/solution/suo-you-ke-neng-de-man-er-cha-shu-by-leetcode/)，[划分为K个相等的子集](https://leetcode-cn.com/problems/partition-to-k-equal-sum-subsets/)

（2）题目的数量不多

（3）问题可以从其他领域抽象而来，该现象应该存在于很多类型的问题中。比如，[原子的数量](https://leetcode-cn.com/problems/number-of-atoms/)

很多年前，写过一个[短文](https://zhpmatrix.github.io/2016/10/11/code-tricks/)，最近在读组里同学的源码的时候，看到这样一段代码，如下：

```
def traverse_datafile(rootpath, suffix, fout_path):
    
    FILENAME_PATTERN = re.compile('^(.*?)' + suffix + '$')
    
    files = os.listdir(rootpath)
    for file in files:
        # print(file)
        if os.path.isdir(rootpath + '/' + file):
            # print(rootpath + '/' + file)
            traverse_datafile(rootpath + '/' + file, suffix, fout_path)
        else:
            if FILENAME_PATTERN.match(file):
                print(rootpath + '/' + file)
                change_format(rootpath + '/' + file, fout_path+file)
    
    return True

```
代码想要做的就是实现目录文件遍历，于是用手撸了一个遍历的逻辑。当一个目录包含文件目录和文件的时候，只使用os.listdir应该是无法实现的。当然，如果知道os.walk的情况下，可以更加优雅的实现。如下：

```
def get_ner_filenames(self)->list:
        filenames = []
        for root, dirs, files in os.walk(self.root_dir):
            for filename in files:
                if filename.endswith('.name'):
                    filenames.append(os.path.join(root,filename))
        return filenames
```
这里，os.walk返回的是一个generator，能够逐级访问一个文件目录。优点很多，比如没有recursive的stack限制，内存友好(lazy)以支持更深的遍历需求，此外，写出的代码更加优雅易懂。

但是，recursive的思想在很多时候，实现的方式是简单优雅的。在阮的一篇博客中，看到一个认识：**递归本质上是一种循环操作，纯粹的函数式编程语言没有循环操作命令，所有的循环都用递归实现。**

比如，遍历一个list的实现，多数时候，这样实现：

```
a = [1,2,3]
print(a)
```

递归改造一下吧（不考虑边界），比如这样：

```
def show_list(a):
	print(a[0])
	if len(a[1:]) > 0:
		show_list(a[1:])
```

但是，recursive的问题，包括：重复计算（这在计算斐波那契数的第N项中可以体现），递归深度受限。前者的解决方式可以是递归改为递推，后者可以采用[尾递归](https://www.ruanyifeng.com/blog/2015/04/tail-call.html)的方式实现（比如将一个类似树形的调用栈转为一个链式的调用栈）。从状态维护上来看，二者有相通之处，都是记录当前需要的状态，不需要记录历史状态。当然，结合问题的特殊之处，减少重复计算也算是一个红利了。

当然，[递归算法转化为非递归算法](https://mp.weixin.qq.com/s?__biz=MzA5ODUxOTA5Mg==&mid=2652556683&idx=2&sn=5692497d7b3d352e428be81e73f2ee08&chksm=8b7e3cd0bc09b5c67cc9b557785607f552defdcff0084297dafc4d8ba9c6e9ee8231a18685a5&mpshare=1&scene=23&srcid=1122HbnVa5L18L5MtmzspUqi&sharer_sharetime=1584768314443&sharer_shareid=0e8353dcb5f53b85da8e0afe73a0021b%23rd)是另外一个有意思的问题，这里暂不做探讨。

看几道LC的题目吧。


#### 1.[为运算表达式设计优先级](https://leetcode-cn.com/problems/different-ways-to-add-parentheses/submissions/)

题目描述：给定一个含有数字和运算符的字符串，为表达式添加括号，改变其运算优先级以求出不同的结果。你需要给出所有可能的组合的结果。有效的运算符号包含 +, - 以及 * 。示例如下：

```
输入: "2-1-1"
输出: [0, 2]
解释: 
((2-1)-1) = 0 
(2-(1-1)) = 2
```
还有一个：

```
输入: "2*3-4*5"
输出: [-34, -14, -10, -10, 10]
解释: 
(2*(3-(4*5))) = -34 
((2*3)-(4*5)) = -14 
((2*(3-4))*5) = -10 
(2*((3-4)*5)) = -10 
(((2*3)-4)*5) = 10
```

一个基本的解法：

```
def diffWaysToCompute(self, input: str) -> List[int]:
		res = []
        for i, char in enumerate(input):
            if char in ['+', '-', '*']:
             	left = diffWaysToCompute(input[:i])
                right = diffWaysToCompute(input[i+1:])
                for l in left:
                    for r in right:
                        if char == '+':
                            res.append(l + r)
                        elif char == '-':
                            res.append(l - r)
                        else:
                            res.append(l * r)

        return res
```
分析上述代码，整体的逻辑是：将原问题分解为子问题，在得到子问题的解之后，合并子问题的解。因此，从这道题也可以看出，分支和递归往往是在一块儿的，用递归的方式求解子问题。
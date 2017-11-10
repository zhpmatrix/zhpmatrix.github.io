---
layout: post
title: "[LeetCode]关于Gas Station的思考"
excerpt: "Gas Station是一道Medium类型的题目，这篇Blog仅仅是对该题的一些思考，并不是一个答案解析的过程。"
date: 2017-11-10 12:19:00
mathjax: true
---

题目的描述是这样的：

在一个环形路线上有N个加油站，每个加油站的油量是gas\[i\]。假设老王开着一辆吉普沿着该路线行驶，该吉普是油桶无限大的定制版，从加油站(i)到加油站(i+1)所需要的油量是cost\[i\]。假设老王从某个加油站出发并且出发时油桶没油。

问: 老王从哪个加油站出发可以绕路线一周恰好回到出发时的加油站。

如果考虑不仔细，可能写出下边的代码：

```c++
int canCompleteCircuit(vector<int>& gas, vector<int>& cost){
    int start_idx = -1;
    int num_gas = gas.size();
    for(int i = 0;i < num_gas;i++){
        int minus_gas = 0;
        for(int j = i;j < num_gas+i;j++){
            minus_gas += gas[j%num_gas] - cost[j%num_gas];
        }
        if(minus_gas >= 0){
            start_idx = i;
            break;
        }
    }
    return start_idx;
}
```

代码的时间复杂度为O(N^2)，想法比较简单(暴搜?)。将每个加油站作为出发点，绕路线一周，回到出发点处，判断油量是否小于0。如果小于0，则表示该加油站不能作为出发点，否则可以作为出发点，其中油量为0表示刚好回到出发点，油量用完。代码在实现的时候，满足只要发现合适的出发点就终止循环的策略。

代码乍一看，思路和实现都非常简单，但是存在一个明显的错误。

**minus\_gas是一个累积变量**，并不能以该变量作为能否遍历路线的判断条件。假设一种情况，从加油站(i)到加油站(i+1)时，该变量为负；从加油站(i+1)到加油站(i+2)时，该变量为正。那么能否认为从加油站(i)到加油站(i+2)可以遍历呢？显然不能，没油咋跑！

所以得到的启发是：必须要考虑连续加油站之间的minus\_gas值的正负。

如果从加油站(i)到加油站(i+1)的minus\_gas值为负，老王就不能从加油站(i)出发。于是有下述代码实现：

```c++
int canCompleteCircuit(vector<int>& gas, vector<int>& cost){
    int minus_gas = 0;
    int start_idx = 0;
    int neg_gas = 0;
    for(int i = 0; i < gas.size(); ++i){
        minus_gas += gas[i]-cost[i];
        if(minus_gas<0){
            neg_gas += minus_gas;
            minus_gas = 0;
            start_idx = i + 1;
        }
    }
    neg_gas += minus_gas;
    return neg_gas < 0 ? -1 : start_idx;
}
```

如果从加油站(i)到加油站(j)，连续加油站之间都可以到达，minus\_gas表示的是剩余的油量。相反，连续加油站都不可以到达，neg\_gas表示的是缺乏的油量。问题的关键如下：

```c++

    neg_gas += minus_gas;
    return neg_gas < 0 ? -1 : start_idx;

```
为什么这两行代码能够判断可达性？

答案在于连续性。假设一种情况，有6个加油站，得出可以作为出发点的加油站的索引为3，假设索引从0开始，则0->1，1->2，2->3的minus\_gas一定为负。3->4,4->5的minus\_gas一定为正。这样，当老王从索引为3的加油站出发一定能回到该加油站吗？

假设一种不能回到出发加油站的情况，0->1为正，1->2为负，2->3为正。

当老王从索引为3的加油站出发的时候，3->5的minus\_gas为正，由于从0出发时，0->1为负，当老王走到1时，3->1可能为正，但是如果3->2为负，由于2->3为负(从0出发时)，3->3一定为负(其中包含2->3)，与假设矛盾。所以，不可能呀！

上述其实是一个程序的正确性证明。上述代码的时间复杂度是线性的。















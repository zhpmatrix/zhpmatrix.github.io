---
layout: post
title: "从C++的字符串分割展开讨论"
tags: [C++]
excerpt: "C++没有内置字符串的分割函数，惊不惊喜，意不意外？"
date: 2017-10-05 10:05:00
mathjax: true
---

没有内置函数，可以自己来写。下面是我在别人代码上修改之后的一个版本。

    vector<string> split(const string& src, const string& separator){
        string str = src;
        string substring;
        string::size_type start = 0, index;
        vector<string> dest;
        while(index != string::npos){
            index = str.find_first_of(separator,start);
            if (index != string::npos){    
                    substring = str.substr(start,index-start);
                    dest.push_back(substring);
                    start = str.find_first_not_of(separator,index);
                    if (start == string::npos) break;
            }
        }
        substring = str.substr(start);
        dest.push_back(substring);
        return dest;
    }

其中，string::size_type是一种数据类型，而string::npos的解释可以直接读官网解释：

    static const size_t npos = -1;

    Maximum value for size_t
    
    npos is a static member constant value with the greatest possible value for an element of type size_t.

    This value, when used as the value for a len (or sublen) parameter in string's member functions, means "until the end of the string".

    As a return value, it is usually used to indicate no matches.

    his constant is defined with a value of -1, which because size_t is an unsigned integral type, it is the largest possible representable value for this type.

从上述表达可知，string::npos常常用于字符串中子串查找不到的返回值。幸好，C++提供了find函数的内置实现，也就是说，string::npos和find结合实现子串查找逻辑。此处据说有大坑，先留坑，后讨论。

    index = str.find_first_of(separator,start);

返回separator在str\[start:\](Python党一定知道我在说什么)中首次出现的位置。

    start = str.find_first_not_of(separator,index);

返回separator在str[index:]中首次不匹配的位置。注意，在while结构中，返回值start又作为find_first_of的参数进行下一轮循环。
    
    if (start == string::npos) break;

查找结束，退出。上文提到的大坑与这行代码相关。

    substring = str.substr(start);
    dest.push_back(substring);

不要忘记最后分割出的子串，分割结束。

关于上述大坑的描述，在这篇[博客](http://www.cnblogs.com/web100/archive/2012/12/02/cpp-string-find-npos.html)中有介绍。在此简单描述：

    int idx = str.find(substr);
    if(idx == string::npos){
        cout << "No found!";
    }else{
        cout << "Found!";
    }

作者说道，idx == string::npos会由于类型不一致导致错误！正确的做法应该是：

    string::size_type idx = str.find(substr);

或者

    if(str.find(substr) == string::npos){//TODO}

第一种解决方法声明正确的类型，第二种解决方法避免判断返回值类型。

实际上，打印出的string::npos的值是一个非常大的数，而且代码在C++11下使用int类型声明idx验证通过。坑在哪里？(难道验证姿势不对？)

在LeetCode中，C++的字符串操作是一种常见类型。涉及函数substr, replace, find, rfind,

find\_first\_of, find\_last\_of, find\_first\_not\_of, find\_last\_not\_of。

补充：

[erase指针失效问题](http://www.cppblog.com/Herbert/archive/2008/12/27/70479.html),这篇博客相对较早，给出了两种方案，代码如下：

    for(vector<int>::iterator iter = numbers.begin();iter != numbers.end();){
        if(*iter == 10){
            iter = numbers.erase(iter);
            //Not work!
            //numbers.erase(iter++);
        }else{
            iter++;
        }
    }

    iter = numbers.erase(iter);

erase返回被删除元素下一个元素的地址，所以可以使用返回值(iter)来存储下一个元素的指针(地址)。

虽然，

    numbers.erase(iter++)

表示在指针时效前完成计算，但是实验中不OK！个人感觉这种方式仍然没有解决野指针问题。












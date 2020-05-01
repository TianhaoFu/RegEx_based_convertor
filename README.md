# RegEx_based_convertor

句子的同义转换是一个很常见的NLP任务，现在很多人用深度学习的方法来做此任务。有时候结合其他方法来做同义转换能够非常有效的帮助你提高算法的某些性能或者对你的算法有启发，所以这里有一种将规则表示为正则表达式的形式来实现句子的同义转换的方法，希望对做相关问题的你有所帮助或启发~

# 0 简介
#### 基于正则表达式句子同义转换器用于完成paraphasing任务，可实现以下功能：

1）给定数据集，可从数据集中提取句子转换的规则。

数据集的基本组成单元为一对相同意思的question。

如：
emmm. how do I learn to play the guitar ? it’s so diffcult  <->  what is the best way to learn to play the guitar ?  

规则用正则表达式的形式进行表达

如：
[\,\.\?]how\sdo\si\s(.+)[\,\.\?]  <->  what is the best way to $@_0

2）可将提取的规则应用于新句子中，转换为同义不同的形式。

# 1 句子同义转换器实现机制
#### 核心思想为将转换规则表示成正则表达式对的形式，利用正则表达式的特点实现同义转换。

具体来说，设正则表达式对分别为P1和P2。问题转换前为Q1，问题转换后为Q2。

首先利用P1从Q1中提取到一些关键字，如名词，形容词等。设提取到的关键字集合为K，通过将K嵌入到P2中得到Q2从而完成问题转换的思路。

这里举一个例子：

Q1： emmm. how do I learn to play the guitar ? it’s so diffcult 

Q2： what is the best way to learn to play the guitar ?  

K：  {“learn to play the guitar” }

P1：  [\,\.\?]how\sdo\si\s(.+)[\,\.\?]

P2：  what is the best way to $@_0

流程：P1首先利用 (.+) 从Q1中提取到关键字 learn to play the guitar ，并利用[\,\.\?] 将Q1中与主干无关的部分emmm. it’s so diffcult  去掉，之后将提取到的关键字嵌入到P2（替换P2中的$@_0）中便得到Q2。
# 2 问题转换器学习思路（规则学习思路）
#### 核心思想为通过字符串及正则表达式的规则进行学习。

1）P1的生成：

P1初始时为空字符串。之后首先从Q1的第一个单词开始，循环搜索Q2中是否有同样的单词，若有则在正则表达式P1尾部加一个能够匹配关键字的项“(.+)”，若没有则将该单词原样加入到正则表达式P1尾部中。循环搜索结束后，在P1首尾分别加入[\,\.\?]，最终得到的字符串即为P1.

2）P2的生成：

P2初始时与Q2相同。首先从Q1的第一个单词开始，循环搜索Q2中是否有同样的单词，若有则将Q2（P2）中相同的单词替换为$@_i，最终改变后的Q2（P2）即为P2.

# 3 文件目录：

->quora.zip ：quora公开句子同义转换数据集

->rule_generater.py ：训练问题转换器(规则生成)

->rule_filter_test.txt ： 规则文件

->rule_test.py ：对生成的的规则进行测试

->utils.py ：工具函数文件


# 如果你觉得对你有用，请在你的代码或者论文中注明一下我的工作，如果能再给我点个star就更好啦！！！


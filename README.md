# rule
sequence to sequence
# 一、简介
## 基于正则表达式做的一套规则生成器和规则应用器用于完成paraphasing任务

1）给定数据集，可从数据集中提取句子转换的规则。

数据集的基本组成单元为一对相同意思的question
如：
what 's your name
what is the name of you

2）可将提取的规则应用于新句子中，转换为同义不同的形式。

# 二、问题转换器转换思路
## 问题转换器由一系列正则表达式对组成。

设正则表达式对分别为P1和P2。问题转换前为Q1，问题转换后为Q2。

首先利用P1从Q1中提取到一些关键字，如名词，形容词等。设提取到的关键字集合为K，将K嵌入到P2中得到Q2从而完成问题转换的思路。

例：

Q1： emmm. how do I learn to play the guitar ? it’s so diffcult 

Q2： what is the best way to learn to play the guitar ?  

K：  {“learn to play the guitar” }

P1：  [\,\.\?]how\sdo\si\s(.+)[\,\.\?]

P2：  what is the best way to $@_0

流程：P1首先利用 (.+) 从Q1中提取到关键字 learn to play the guitar ，并利用[\,\.\?] 将Q1中与主干无关的部分emmm. it’s so diffcult  去掉，之后将提取到的关键字嵌入到P2（替换P2中的$@_0）中便得到Q2。
# 三、问题转换器学习思路（正则表达式对学习思路）
## 核心思想为通过字符串及正则表达式的规则进行学习。

a.P1的生成：

P1初始时为空字符串。之后首先从Q1的第一个单词开始，循环搜索Q2中是否有同样的单词，若有则在正则表达式P1尾部加一个能够匹配关键字的项“(.+)”，若没有则将该单词原样加入到正则表达式P1尾部中。循环搜索结束后，在P1首尾分别加入[\,\.\?]，最终得到的字符串即为P1.

b.P2的生成：

P2初始时与Q2相同。首先从Q1的第一个单词开始，循环搜索Q2中是否有同样的单词，若有则将Q2（P2）中相同的单词替换为$@_i，最终改变后的Q2（P2）即为P2.

# 四、文件简介：

->rule_extractor.ipynb 训练问题转换器并且应用问题转换器进行问题的同义转换

->rule_filter.ipynb 对转换后的规则进行数据预处理

->rule_filter_test.txt 以quora数据集为例得到的同一转换规则




import pandas as pd
import numpy as np
import re
import unicodedata
import copy

"""      
    rule_generate
    contains:
        function rule_generator1(df1):Forward conversion rule generation
        function rule_generator2(df1):Reverse conversion rule generation
        function rule_filter(rules):Filter unnecessary rules
    
    规则生成文件
    包含 :
        正向转换规则生成器函数rule_generator1(df1)
        逆向转换规则生成器函数rule_generator2(df1)
        规则筛选器函数rule_filter(rules)
"""

# Forward conversion rule generation
# 正向转换规则生成器
def rule_generator1(df1):
    for i in range(len(df1)):
        sentence1 = df1['question1'][i].lower().split()
        #     sentence1 = 'what should i do if i want go home ?'.split()
        sentence1.pop()
        sentence2 = df1['question2'][i].lower().split()
        #     sentence2 = 'what can i do if i want go home ?'.split()
        sentence2.pop()

        margin = 1
        flag = True
        masked = '%@%'

        r1 = ''
        r2 = [x for x in sentence2]

        p = "\$@_\d+|\d+\$@_"  # filter p2 that contains &@_number
        for item in r2:
            if re.findall(p, item):
                flag = False
                break
        if flag:
            sentence1_len = len(sentence1)
            sentence2_len = len(sentence2)
            id_dollar = 0
            count = 0
            j = 0
            while j < len(sentence1):
                try:
                    # 对相同单词处理
                    word = sentence1[j]
                    id = sentence2.index(word)
                    maxlen = 0
                    xval = 0
                    # 计算从当前单词出发的相同字符子串长度maxlen
                    while sentence1[j + xval] == sentence2[id + xval]:
                        maxlen = maxlen + 1
                        xval = xval + 1
                        if j + xval >= sentence1_len or id + xval >= sentence2_len:
                            break

                    if maxlen > 1:
                        index = r2.index(word)
                        while xval > 0:
                            del r2[index]
                            sentence2[id + maxlen - xval] = masked
                            xval = xval - 1
                        # 修改规则r1
                        cur_word1 = r'(.+)'
                        r1 += cur_word1
                        # 修改规则r2
                        cur_word2 = '$@_{}'.format(id_dollar)
                        id_dollar += 1
                        r2.insert(index, cur_word2)
                        # 修改循环变量j
                        j = j + maxlen
                    elif maxlen == 1:
                        # 修改规则r1
                        cur_word1 = r'(\S+)'
                        r1 += cur_word1
                        # 修改规则r2
                        index = r2.index(word)
                        cur_word2 = '$@_{}'.format(id_dollar)
                        id_dollar += 1
                        r2[index] = cur_word2
                        # 修改原句sentence2
                        sentence2[id] = masked
                        # 修改循环变量j
                        j = j + 1
                except:
                    # 对不同单词处理
                    cur_word1 = word
                    pattern = ".*[\\\|\*\[\]\{\}\|\(\)\+\.\?\$\^\/].*"
                    if re.findall(pattern, cur_word1):
                        flag = False
                        break
                        # 修改规则r1
                    r1 += cur_word1
                    count = count + 1
                    # 修改循环变量j
                    j = j + 1

                if j < len(sentence1):
                    r1 += '\s'
            r2_len = len(r2)
            if count < margin or (r2_len - id_dollar - 1) < margin:  # r1、r2中至少有margin个单词以上
                flag = False
            if flag:
                r1 = '[\,\.\?]' + r1 + '[\,\.\?]'
                rule.append(''.join(r1) + '>>' + ' '.join(r2))
    #     if i > 10:
    #         break

# Reverse conversion rule generation
# 逆向转换规则生成器
def rule_generator2(df1):
    for i in range(len(df1)):
        sentence1 = df1['question2'][i].lower().split()
        sentence1.pop()
        sentence2 = df1['question1'][i].lower().split()
        sentence2.pop()

        margin = 1
        flag = True
        masked = '%@%'

        r1 = ''
        r2 = [x for x in sentence2]

        p = "\$@_\d+|\d+\$@_"  # filter p2 that contains &@_number
        for item in r2:
            if re.findall(p, item):
                flag = False
                break
        if flag:
            sentence1_len = len(sentence1)
            sentence2_len = len(sentence2)
            id_dollar = 0
            count = 0
            j = 0
            while j < len(sentence1):
                #         for j in len(sentence1):
                #             j = sentence1.index(word)
                try:
                    # 对相同单词 处理
                    word = sentence1[j]
                    id = sentence2.index(word)
                    maxlen = 0
                    xval = 0
                    # 计算从当前单词出发的相同字符子串长度maxlen
                    while sentence1[j + xval] == sentence2[id + xval]:
                        maxlen = maxlen + 1
                        xval = xval + 1
                        if j + xval >= sentence1_len or id + xval >= sentence2_len:
                            break

                    if maxlen > 1:
                        index = r2.index(word)
                        while xval > 0:
                            del r2[index]
                            sentence2[id + maxlen - xval] = masked
                            xval = xval - 1
                        # 修改规则r1
                        cur_word1 = r'(.+)'
                        r1 += cur_word1
                        # 修改规则r2
                        cur_word2 = '$@_{}'.format(id_dollar)
                        id_dollar += 1
                        r2.insert(index, cur_word2)
                        # 修改循环变量j
                        j = j + maxlen
                    elif maxlen == 1:
                        # 修改规则r1
                        cur_word1 = r'(.+)'
                        r1 += cur_word1
                        # 修改规则r2
                        index = r2.index(word)
                        cur_word2 = '$@_{}'.format(id_dollar)
                        id_dollar += 1
                        r2[index] = cur_word2
                        # 修改原句sentence2
                        sentence2[id] = masked
                        # 修改循环变量j
                        j = j + 1
                except:
                    # 对不同单词处理
                    cur_word1 = word
                    pattern = ".*[\\\|\*\[\]\{\}\|\(\)\+\.\?\$\^\/].*"
                    if re.findall(pattern, cur_word1):
                        flag = False
                        break
                        # x修改规则r1
                    r1 += cur_word1
                    count = count + 1
                    # 修改循环变量j
                    j = j + 1

                if j < len(sentence1):
                    r1 += '\s'
            r2_len = len(r2)
            if count < margin or (r2_len - id_dollar - 1) < margin:  # r1、r2中至少有margin个单词以上
                flag = False
            if flag:
                r1 = '[\,\.\?]' + r1 + '[\,\.\?]'
                rule.append(''.join(r1) + '>>' + ' '.join(r2))

# Filter unnecessary rules
#规则筛选器 筛掉一些不必要的规则
def rule_filter(rules):
    ruless = []
    for rule in rules:
        count0 = 0

        p1 = rule.split('>>')[1].split()
        p2 = rule.split('>>')[1].split()

        pattern1 = "\$\d+"
        pattern2 = "\d+\$"

        flag_filter = False

        for item1 in p1:
            list_test1 = re.findall(pattern1, item1)
            list_test2 = re.findall(pattern2, item1)

            if list_test1 or list_test2:
                flag_filter = True

        for item2 in p2:
            list_test1 = re.findall(pattern1, item2)
            list_test2 = re.findall(pattern2, item2)

            if list_test1 or list_test2:
                flag_filter = True

            if '$' == item2:
                flag_filter = True

            if '$@_' in item2:
                count0 = count0 + 1
        if flag_filter:
            continue

        if count0 > 0:
            ruless.append(rule)


if __name__ == '__main__':
    # load dataset
    # 读取数据集
    df1 = pd.read_csv('quora.csv', encoding='gbk')
    print(len(df1))
    df1.head()
    rule = []

    # rule generate
    # 用转换器生成规则
    rule_generator1(df1)
    rule_generator2(df1)

    # Merge newly generated rules with manually made rules
    # 将新生成规则与人工制定的规则合并
    with open('rule.txt', 'r') as f:
        ruless = f.read().split('\n')
        ruless.pop()
    print(ruless[:3])
    rule1 = rule + ruless

    # Sort rules by their frequency of occurrence
    # 将规则按其出现的频度排序
    dic = {}
    for r in rule1:
        if r in dic:
            dic[r] += 1
        else:
            dic[r] = 1
    sort_rule1 = sorted(dic.items(), key=lambda e: e[1], reverse=True)

    rules = []
    count = []
    for i in range(len(sort_rule1)):
        if sort_rule1[i][1] > 1:
            rules.append(sort_rule1[i][0])
            count.append(sort_rule1[i][1])

    # Screening rules
    # 筛选规则
    rule_filter(rules)

    # Export rule
    # 导出规则
    with open('rule_filter_test.txt', 'w') as f:
        for r in ruless:
            try:
                f.write(r)
                f.write('\n')
            except:
                r = r.encode("gb18030")
                r = str(r)


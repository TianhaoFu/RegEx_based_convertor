import pandas as pd
import numpy as np
import re
import unicodedata
import copy

"""
    rule_test
    contains:
        function apply_rule(pattern,sen):Rule converter
    
    测试文件
    包含
        规则转换器apply_rule(pattern,sen)
    
"""

#规则转换器
def apply_rule(pattern,sen):
#     sen_list = re.split(r'([\,\.\?])',sen)
#     for part in sen_list:
#         if not part == ',' or part == '.' or part == '?':
#             sen = '.' + part + '.'
    sen = '.' + sen + '.'
    p1 = pattern.split('>>')[0]#字符串
    p2 = pattern.split('>>')[1].split()
    if re.findall(p1,sen):
        result = re.findall(p1,sen)[0]
        same_str = []
        if isinstance(result,tuple):
            for i in range(len(result)):
                same_str.append(result[i])
        if isinstance(result,str):
            same_str.append(result)
        answer=[]
        for item in p2:
            if '$@_' in item:
                nu = int(re.findall('[0-9]+',item)[0])
                curword = same_str[nu]
                if not curword.endswith(' '):
                     curword = curword + ' '
                if(curword.startswith(' ')):
                    curword = curword[1:]

                answer.append(curword)
            else:

                if not item.endswith(' '):
                     item = item + ' '
                if(item.startswith(' ')):
                    item = item[1:]
                answer.append(item)
#             answer_list.append(answer)
        return  (''.join(answer)[:-1])
#         else:
#             answer_list.append(part)
#     answer_list.append(''.join(answer_list)[:-1])
    else:
        return ""


if __name__ == '__main__':
    # load rule
    # 读取规则
    with open('rule_filter_test.txt', 'r') as f:
        ruless = f.read().split('\n')
        ruless.pop()
    print(ruless[:10])

    #load dataset
    # 读取数据集
    df1 = pd.read_csv('quora.csv', encoding='gbk')
    print(len(df1))
    print(df1.head())

    #start test
    # 开始测试
    sen_fail = []
    count = []
    for i in range(len(df1)):
        #     sen = 'how do i go home'
        count.append(0)
        sen = df1['question1'][i].lower()
        sen = sen.replace(' ?', '')
        flag1_ = True
        for j in range(len(ruless)):
            answer = apply_rule(ruless[j], sen)
            if answer:
                flag1_ = False
                print('\n', 'sen：', sen, '\n', 'rule：', ruless[j], '\n', 'answer：', answer, '\n')
                count[i] = count[i] + 1
        if flag1_:
            sen_fail.append(df1['question1'][i])
        if i > 5:
            break



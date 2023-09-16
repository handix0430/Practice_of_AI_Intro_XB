import os
from itertools import accumulate # 用于计算累积和的序列
from bisect import bisect_right # 用于在有序列表中插入元素并返回插入位置

path = './THUCNews' # 数据集路径
wfilenames = ['train.txt', 'test.txt', 'dev.txt'] # 设置文件
num = [20000, 2000, 2000] # 设置各数据集样本数量
allnum = list(accumulate(num)) # 计算各数据集样本数量的累积和序列，用于后续判断样本应该分配到哪个数据集文件中
wfiles = [open(path+f,'w', encoding='utf-8') for f in wfilenames]  # 打开数据集文件

subpaths = os.listdir(path) # 得到各个目录，即类别名称
for pathname in subpaths:
    subpath = os.path.join(path, pathname) # 拼接当前目录和类别名称，得到子目录的完整路径，并存储在subpath变量中
    if os.path.isdir(subpath): # 如果是目录
        files = os.listdir(subpath) # 得到所有的样本文件名称
        print(pathname, len(files)) # 打印该类别名称及样本数量
        if len(files) < allnum[-1]:continue # 样本量不足24000不提取该类别样本，为了保证每个类别都有足够的样本分配到各数据集文件中。

        for i in range(allnum[-1]):
            tag = bisect_right(allnum, i) # 得到样本改写入什么文件，tag表示该样本应该分配到哪个数据集文件中，例如tag为0表示分配到训练集，tag为1表示分配到验证集，tag为2表示分配到测试集。
            with open(os.path.join(subpath, files[i]), 'r', encoding='utf-8') as f:
                line = f.readline() # 只读标题
                wfiles[tag].write(pathname+'\t'+line) #写入数据集
for f in wfiles:
    f.close()

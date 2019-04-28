import os
# os.chdir("D://OneDrive/Dev_pc/")

import numpy as np
import pandas as pd
from Train_Operation_Model import Train_Model
import datetime as dt
from functools import reduce
_start = dt.datetime.now()
print(_start)

# 生成模型参数数据
arg_x = [i for i in range(0, 8)]
arg_f1 = [i for i in range(5, 24)]
arg_f2 = [i for i in range(5, 24)]
arg_G = [i / 100 for i in range(5, 16, 1)]
arg_K = [i for i in range(0, 18)]
arg_list = [arg_x, arg_f1, arg_f2, arg_G, arg_K, ]

# 调整代码参数格式
fn = lambda x, code=',': reduce(
    lambda x, y: [
        str(i) + code + str(j) for i in x for j in y], x)

# 直接调用fn(lists, code)
res = fn(arg_list)
Arge_df = pd.DataFrame([i.split(',') for i in res], columns=[
                       'arg_x', 'arg_f1', 'arg_f2', 'arg_G', 'arg_K'])

Arge_df.iloc[:, :3] = Arge_df.iloc[:, :3].astype(int)
Arge_df['arg_G'] = Arge_df['arg_G'].astype(float)
Arge_df['arg_K'] = Arge_df['arg_K'].astype(int)
Arge_df_adj = Arge_df[~((Arge_df['arg_x'] == 0) & (
    (Arge_df['arg_f1'] + Arge_df['arg_f2'] >= 24)))]
Arge_df_adj = Arge_df_adj[~((Arge_df_adj['arg_x'] == 7) & (
    (Arge_df_adj['arg_f1'] + Arge_df_adj['arg_f2'] >= 24)))]
print(str(len(Arge_df_adj)))
# 参数代码存储
Arge_df_adj.to_csv("Arge_data_df.csv")

# 运行各参数
Data_output = Arge_df_adj.apply(lambda arge: Train_Model(
    x=arge['arg_x'],
    f1=arge['arg_f1'],
    f2=arge['arg_f2'],
    G=arge['arg_G'],
    K=arge['arg_K'],
).All_Return(), axis=1, raw=True,
    result_type='expand')
print(dt.datetime.now() - _start)
# 存储结果数据
Data_output.to_csv('finish_data.csv')

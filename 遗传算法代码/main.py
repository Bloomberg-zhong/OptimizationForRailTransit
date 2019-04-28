# -*- coding: utf-8 -*-
"""
执行脚本main.py
"""

import numpy as np
import geatpy as ga
from templet import templet

# 获取函数接口地址
AIM_M = __import__('aimfuc')
# 变量设置
x1 = [-3, 12.1]  # 自变量1的范围
x2 = [4.1, 5.8]  # 自变量2的范围
b1 = [1, 1]  # 自变量1是否包含下界
b2 = [1, 1]  # 自变量2是否包含上界
codes = [0, 0]  # 自变量的编码方式，0表示采用标准二进制编码
precisions = [4, 4]  # 在二进制/格雷码编码中代表自变量的编码精度，当控制变量是二进制/格雷编码时，该参数可控制编码的精度
scales = [0, 0]  # 是否采用对数刻度
ranges = np.vstack([x1, x2]).T  # 生成自变量的范围矩阵
borders = np.vstack([b1, b2]).T  # 生成自变量的边界矩阵
# 生成区域描述器
FieldD = ga.crtfld(ranges, borders, precisions, codes, scales)

# 调用编程模板(其中problem是表示我们所优化的问题是离散型变量还是连续型变量。I表示离散，R表示连续，其余相关参数的含义详见templet.py的函数定义)
[pop_trace, var_trace, times] = templet(AIM_M, 'aimfuc', None, None, FieldD, problem='R', maxormin=-1, MAXGEN=200,
                                        NIND=100, SUBPOP=1, GGAP=0.8, selectStyle='sus', recombinStyle='xovdp',
                                        recopt=None, pm=None, distribute=True, drawing=1)
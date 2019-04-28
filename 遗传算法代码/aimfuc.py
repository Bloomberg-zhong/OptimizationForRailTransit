# -*- coding: utf-8 -*-
"""
aimfc.py - 目标函数文件
描述:
    目标：max f = 21.5 + x1 * np.sin(4 * np.pi * x1) + x2 * np.sin(20 * np.pi * x2)
    约束条件：
        x1 != 10
        x2 != 5
        x1 ∈ [-3, 12.1] # 变量范围是写在遗传算法的参数设置里面
        x2 ∈ [4.1, 5.8]
"""

import numpy as np


def aimfuc(Phen, LegV):
    x1 = Phen[:, [0]]  # 获取表现型矩阵的第一列，得到所有个体的x1的值
    x2 = Phen[:, [1]]
    f = 26458.5 + x1 * np.sin(9715.15 * np.pi * x1) + x2 * np.sin(284128 * np.pi * x2)*1004
    # f = x1(x2.mean())/(1- x2.mean())
    exIdx1 = np.where(x1 == 10)[0]  # 因为约束条件之一是x1不能为10，这里把x1等于10的个体找到
    exIdx2 = np.where(x2 == 5)[0]
    LegV[exIdx1] = 0
    LegV[exIdx2] = 0
    return [f, LegV]
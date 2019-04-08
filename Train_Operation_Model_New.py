#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/8 15:02
# @Author  : Noel
# @Site    :
# @File    : Train_Operation_Model_New.py
# @Software: PyCharm

import os
# os.chdir("/Users/zhongpengbo/OneDrive/文档")
import pandas as pd
import numpy as np
import xlwings
ismac = False

if ismac:
    data_file_path = '/Users/zhongpengbo/OneDrive/文档/李涵论文/列车运行数据.xlsx'
else:
    data_file_path = 'C:/Users/Noel/OneDrive/文档/李涵论文/列车运行数据.xlsx'


class modle():
    def __init__(self,
                 X: 5,
                 f1: 5,
                 f2: 5,
                 G: None
                 ):
        # Q 为列车流量
        P = (pd.read_excel(data_file_path, sheet_name=0, index_col=0))
        self.P = P.iloc[:, 1:]

        # 列车每个区间间隔距离与运行时间
        pd.read_excel(data_file_path, sheet_name=1)

        # 列车上下车流量数据
        Train_Values_of_Float = pd.read_excel(
            data_file_path, sheet_name=2, index_col=0)
        self.Train_Values_of_Float = Train_Values_of_Float.iloc[:, 1:]

        # K站上车的客流量
        # Ak在K站上车的下行方向客流量
        ak = pd.read_excel(data_file_path, sheet_name=4, index_col=0)
        self.ak = ak.iloc[:, 1:]

        #  从车站i到j途经各区间的运行时间之和
        Tij = pd.read_excel(data_file_path, sheet_name=3, index_col=0)
        self.Tij = Tij .iloc[:, 1:].fillna(0)

        CT_I_J = pd.read_excel(data_file_path, sheet_name=5, index_col=0)
        self.CT_I_J = CT_I_J.iloc[:, 1:]
        self.f1 = f1  # 主线交路的开行频率 （对数）
        self.h1 = 1 / f1  # 主线交路的发车间隔（时间）
        self.f2 = f2  # 支线交路的开行频率 （对数）
        self.h2 = 1 / f2  # 支线交路的发车间隔（时间）
        self.G = G  # 大小交路发车间隔
        self.x = X

    # 乘客候车时间CW
    def Passenger_Waiting_Time(self,
                               ):
        """
            CW :计算方式
            0< x <8 # 0到X的 8的随机
        :param x:
        :return:
        """

        CW1 = (self.h1 / 2) * (np.sum(np.array(self.P.iloc[0:self.x, 0:12]))) + (
            ((self.h1 + self.h2) / 2) - self.G) * np.sum(np.array(self.P.iloc[0:self.x, 12:]))
        CW2 = (((self.h1 + self.h2) / 2) - self.G) * np.sum(np.array(self.P.iloc[self.x:8, self.x:8])) + (self.h1 / 2) * np.sum(
            np.array(self.P.iloc[self.x:8, 8:12])) + (self.h2 / 2) * np.sum(np.array(self.P.iloc[self.x:8, 12:]))
        CW3 = (self.h1 / 2) * np.sum(np.array(self.P.iloc[8:12, 8:12]))
        CW4 = (self.h2 / 2) * np.sum(np.array(self.P.iloc[12:, 12:]))
        CW = CW1 + CW2 + CW3 + CW4

        return CW

    # 乘客乘车时间CV,
    # CV = CVR + ST

    def Passenger_Travel_Time(self,
                              K: None
                              ):
        """
        CV
        """
        # 乘客乘车时间由途中纯运行时间CVR
        CVR = np.sum(np.array(self.P) * self.Tij)

        D = 1.53
        V = 4  # 列车编组量数
        N_V = 4  # 列车每节车厢门数
        ST_0 = 17  # 开门时间

        # ST列车在车站停留时间
        # 当K<X的时候，
        if K < self.x:
            FH = self.f1
        else:
            # 当K>X的时候，
            FH = (self.f1 + self.f2) / 2

        # 交路1的每列列车在车站K的停站时间——1
        # ST_0列车在车站开关门时间

        ST_H_K = pd.DataFrame((np.array(self.ak) * D) / (V * N_V * FH) + ST_0)

        ST_K = ((np.array(self.Train_Values_of_Float)[:, 2:3])) * ST_H_K

        ST_K = np.sum(ST_K)
        # ST列车在车站停留时间
        ST = sum(ST_K)
        # 乘客候车时间CW, 乘客在车时间CV，乘客换乘时间CT
        CV = CVR + ST
        print("CV:" + str(CV))

    # 乘客在站台的换乘时间CT构成。

    def Passenger_Transfer_Time(self):

        # 乘客在站台的换乘时间CT
        CT = np.sum(np.array(self.CT_I_J) * np.array(self.P))
        print(str(CT))

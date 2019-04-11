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
                 x: 5,  # 5< = x <=24
                 f1: 5,
                 f2: 5,
                 G: None,
                 K: None
                 ):
        # Q 为列车流量
        P = (pd.read_excel(data_file_path, sheet_name=0, index_col=0))
        self.P = P.iloc[:, 1:]

        # 列车每个区间间隔距离与运行时间
        self.The_Train_Miles = pd.read_excel(data_file_path, sheet_name=1)

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

        self.f1 = f1  # 主线交路的开行频率 （对数）
        self.h1 = 1 / f1  # 主线交路的发车间隔（时间）
        self.f2 = f2  # 支线交路的开行频率 （对数）
        self.h2 = 1 / f2  # 支线交路的发车间隔（时间）
        self.C_Z = 800  # 列车固定人员数
        self.T0 = 15

        self.x = x
        """
        K  = 满载率αk
        """
        if 0.05 <= G and G <= 0.15:
            self.G = G  # 大小交路发车间隔
            print("G的范围合理！G:" + str(G))
        else:
            raise Exception('G的值需要在约束条件中0.05<=G<=0.15')

        if self.x == 0:
            if self.f1 + self.f2 <= 24:
                raise Exception(u'错误:当x=0 '
                                u'\tf1 + f2 <= 24')

        if self.x == 7:
            if self.f1 > 5:
                raise Exception(u'错误:当x=7'
                                u'\tf1>5')
            if self.f2 > 5:
                raise Exception(u'错误:当x=7'
                                u'\tf2>5')
            if self.f1 <= 24:
                raise Exception(u'错误:当x=7'
                                u'\tf1<=24')
            if self.f2 <= 24:
                raise Exception(u'错误:当x=7'
                                u'\tf2<=24')

        if K < self.x:
            self.FH = self.f1

        elif 8 <= K and K <= 12:
            self.FH = self.f1

        elif 12 < K and K <= 18:
            self.FH = self.f2
        else:
            # 当K>X的时候，
            self.FH = (self.f1 + self.f2) / 2

    def Passenger_Waiting_Time(self,
                               ):
        """
            Desc:
                对乘客出行时间 进行分析
                Z1 = CW + CV + CT
            CW :计算方式
            0< x <8 # 0到X的 8的随机
        """
        CW1 = (self.h1 / 2) * (np.sum(np.array(self.P.iloc[0:self.x, 0:12]))) + (
            ((self.h1 + self.h2) / 2) - self.G) * np.sum(np.array(self.P.iloc[0:self.x, 12:]))
        CW2 = (((self.h1 + self.h2) / 2) - self.G) * np.sum(np.array(self.P.iloc[self.x:8, self.x:8])) + (self.h1 / 2) * np.sum(
            np.array(self.P.iloc[self.x:8, 8:12])) + (self.h2 / 2) * np.sum(np.array(self.P.iloc[self.x:8, 12:]))
        CW3 = (self.h1 / 2) * np.sum(np.array(self.P.iloc[8:12, 8:12]))
        CW4 = (self.h2 / 2) * np.sum(np.array(self.P.iloc[12:, 12:]))
        CW = CW1 + CW2 + CW3 + CW4
        print('乘客候车时间CW')
        print('\tCW:' + str(CW))
        return CW

    def Passenger_Travel_Time(self,):
        """
        K: 非换成节点
        X: 换成节点
        当8<=K<=12:
            Desc:
                乘客乘车时间CV
                CV = CVR + ST
        """
        # 乘客乘车时间由途中纯运行时间CVR
        CVR = np.sum(np.array(self.P) * np.array(self.Tij))

        D = 1.53
        V = 4  # 列车编组量数
        N_V = 4  # 列车每节车厢门数
        ST_0 = 17  # 开门时间

        # ST列车在车站停留时间
        # 交路1的每列列车在车站K的停站时间——1
        # ST_0列车在车站开关门时间

        ST_H_K = pd.DataFrame((np.array(self.ak) * D) /
                              (V * N_V * self.FH) + ST_0)
        ST_K = ((np.array(self.Train_Values_of_Float))) * ST_H_K

        ST_K = np.sum(ST_K)
        # ST列车在车站停留时间
        ST = sum(ST_K)
        # 乘客候车时间CW, 乘客在车时间CV，乘客换乘时间CT
        CV = CVR + ST
        print('乘客乘车时间CV')
        print("\tCVR:" + str(CVR))
        print("\tST:" + str(ST))
        print("\tCV:" + str(CV))
        return CV, CVR

    def Passenger_Transfer_Time(self):
        """
        Desc:
            乘客在站台的换乘时间CT
        """
        # 乘客在站台的换乘时间CT
        Time = (3600 / (2 * self.f2)) + self.T0
        Train_time_cros = pd.DataFrame(np.zeros(shape=(18, 18)))
        Train_time_cros.iloc[:self.x,
                             11:] = Train_time_cros.iloc[:self.x,
                                                         11:].replace(0,
                                                                      Time)
        CT = np.sum(np.array(Train_time_cros) * np.array(self.P))
        print('乘客在站台的换乘时间CT')
        print('CT:' + str(CT))
        return CT

    def The_Train_Goes_Miles(self,):
        L_1 = 48657
        if 0 <= self.x and self.x <= 7:
            pass
        else:
            return u'x被限制在0-7之间！！！'

        L_2 = self.The_Train_Miles.iloc[self.x:7, 3:4].sum().values[0] \
            + self.The_Train_Miles.iloc[11:17, 3:4].sum().values[0]
        print('列车长度L2')
        print("L_2:" + str(L_2))
        return L_1, L_2


if __name__ == '__main__':
    M = modle(
        x=6,
        f1=6,
        f2=6,
        G=0.05,
        K=5
    )
    # M.Passenger_Waiting_Time()
#     M.Passenger_Travel_Time()
#     M.Passenger_Transfer_Time()
    M.The_Train_Goes_Miles()

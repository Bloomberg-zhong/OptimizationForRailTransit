#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/14 17:03
# @Author  : Noel
# @Site    : 
# @File    : BaseModel.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import xlwings
import plotly

class BaseModel:

    def __init__(self):
        """
        Desc:
            城市轨道交通己经成为我国公共交通的骨干，乘客对服务水平的关注度越来越大，运营企业的对运输成本也越来越重视。
            本章以乘客出行时间最小和企业运输成本最少为目标函数，
            考虑线路通过能力等约束，建立了Ｙ型线列车交路方案优化模型，
            选取相关运营指标，模型求解所得最优列车交路方案与其他交路方案效果进行对比，
            旨在实现同时满足减少乘客出行总时间和降低企业运营成本的效果，
            提升城市轨道交通服务水平。本章设计了遗传算法，对模型进行求解。

    Args:
        Station_Number = [1,N) S
        Station_Number_Can_Return= List   具备折返功能的车站集合 S_1
        Train_Routing = List   列车交路集合 H
        Passenger_Flow_Volume_F2W = 客流量 from ? to ?
        Decision_Variable = 0-1 当交路承担客流时取值为1,否则为0 ,控制是否发车是否有人坐车
        Departure_Frequency =  发车频率  对／小时 ；
        Minimum_Interval_Return = 列车折返最小间隔时间，单位 ： ｓ ； 
        Road_Extent_L = Ｌｈ 交路 Ａ 的长 度 ， 单位 ： ． ｋｍ ;
        User_Travel_time =  乘客出行时间，单位:ｓ;
        User_Hold_on_Station_time =   乘客站台候车时间,单位:ｓ;
        User_Hold_on_Train_time =  乘客在车时间,单位:ｓ;
        Passenger_Transfer_time =  ＣＴ — — 乘客换乘时间,单位:ｓ;  
        Train_Travel_Distance = Ｚ２-- 列车走 行公 里 ， 单位 ： ｋｍ ；  
        Users_Debus = List   Ｄｔｊ 一 一从车站 i,上车到 j． 下车客流量,单位:人 ;
        Train_Marshalling_Cars =   列车编组辆数
        Train_Door_Number=  列车每节车厢车门数

        """
        pass


    def User_Travel_Time_All(self):
        """
        Desc:
            城市轨道交通乘客出行时间Ｚ，由乘客候车时间ＣＦ、乘客在车时间ＣＫ和乘客换乘时间ＣＴ构成。
            乘客候车时间等于客流量与乘客在站台平均候车时间的乘积，与覆盖车站的列车交路种类及发车频率有关。
            乘客在车时间等于乘客途径区间列车的区间运行时间和列车停站时间之和与客流量的乘积，列车区间运行时间和列车停站时间为固定值。
            乘客换乘时间为乘客换乘走行时间和换乘等待时间之和，与交路折返位置和发车频率有关。乘客出行时间可以表示为：
            ＺＸ＝ ＣＷ＋ ＣＶ＋Ｃ
        """

    def User_Travel_Wailt_Time(self):



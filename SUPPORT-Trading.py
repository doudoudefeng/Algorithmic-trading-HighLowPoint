# encoding: UTF-8
import pandas as pd
import numpy as np
class upgrade(object):
    # 输入新的三格数据
    def __init__(self, yuzhi=0.0002):
        self.yu = yuzhi
        self.IndexH = []
        self.IndexL = []
        self.equ_ppredata = []
        self.equ_predata = []
        self.Hline = np.NAN
        self.Lline = np.NAN

    def Input(self, hldata):

        if len(hldata) < 3:
            return None
        ppredata = hldata.iloc[-3]
        preldata = hldata.iloc[-2]
        nowdata = hldata.iloc[-1]

        # 初始化
        if len(self.equ_ppredata) == 0 or len(self.equ_predata) == 0:
            self.equ_ppredata = ppredata
            self.equ_predata = preldata
            return None
        if abs(preldata.close - nowdata.close) < self.yu * nowdata.close:
            # 走平了
            # 前前点不变
            # 前点更新
            self.equ_predata = nowdata
            return None
        else:
            # 未走平
            # 做出判断

            # 与原本一致
            Boolpre = self.equ_ppredata.close < self.equ_predata.close
            Boolnow = self.equ_predata.close < nowdata.close
            if Boolpre and Boolnow:
                # 正正
                self.equ_ppredata = preldata
                self.equ_predata = nowdata
                return None

            elif not Boolpre and not Boolnow:
                # 负负
                self.equ_ppredata = preldata
                self.equ_predata = nowdata
                return None

            # 与原本不一致
            else:
                if Boolpre and not Boolnow:
                    # 正负，高点
                    self.IndexH.append(self.equ_predata)
                    self.equ_ppredata = preldata
                    self.equ_predata = nowdata
                    return 1
                elif not Boolpre and Boolnow:
                    # 负正，低点
                    self.IndexL.append(self.equ_predata)
                    self.equ_ppredata = preldata
                    self.equ_predata = nowdata
                    return -1
            # 无论什么判断，都要更新高低点


def label(Data):
    """
    输入[Dataframe,Dataframe]
    输出方向1,0，-1
    """
    if len(Data) < 2:
        return 0
    else:
        if Data[-1].close > Data[-2].close:
            # 向上
            return 1
        elif Data[-1].close < Data[-2].close :
            # 向下
            return -1
        else:
            return 0

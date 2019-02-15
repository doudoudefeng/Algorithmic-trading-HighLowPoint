# encoding: UTF-8

from __future__ import division

from vnpy.trader.vtObject import VtBarData
# from vnpy.trader.vtConstant import EMPTY_STRING
from vnpy.trader.app.ctaStrategy.ctaTemplate import (CtaTemplate,
                                                     BarGenerator,
                                                     ArrayManager)
from support import *

#################################################基本参数设定###############################################
class HL(CtaTemplate):
    """基于Renko的交易策略"""
    className = 'HL_test'
    author = u'doudoudefeng'

    # 策略参数
    initDays = 30  # 初始化数据所用的天数
    fixedSize = 1  # 每次交易的数量

    # 策略变量


    buyOrderIDList = []  # OCO委托买入开仓的委托号
    shortOrderIDList = []  # OCO委托卖出开仓的委托号
    orderList = []  # 保存委托代码的列表


    # 参数列表，保存了参数的名称
    paramList = ['name',
                 'className',
                 'author',
                 'vtSymbol']

    # 变量列表，保存了变量的名称
    varList = ['inited',
               'trading',
               'pos'
               'label_G2'
               'label_G3'
               'label_G4'
               'label_G5'
               'label_G2pre'
               'label_G3pre'
               'label_G4pre'
               'label_G5pre'
               'tmpdata'
               'trend']

    # 同步列表，保存了需要保存到数据库的变量名称
    syncList = ['pos']


    # ----------------------------------------------------------------------
    def __init__(self, ctaEngine, setting):
        """Constructor"""
        super(HL, self).__init__(ctaEngine, setting)

        #self.bg = BarGenerator(self.onBar, 5, self.onFiveBar)  # 创建K线合成器对象
        #self.am = ArrayManager()

        self.buyOrderIDList = []
        self.shortOrderIDList = []
        self.orderList = []

        self.G1 = upgrade()
        self.G2up = upgrade()
        self.G2down = upgrade()
        self.G3up = upgrade()
        self.G3down = upgrade()
        self.G4up = upgrade()
        self.G4down = upgrade()
        self.G5up = upgrade()
        self.G5down = upgrade()

        self.label_G2 = np.NAN
        self.label_G3 = np.NAN
        self.label_G4 = np.NAN
        self.label_G5 = np.NAN

        self.shang = 2
        self.xia = 0.5

        self.label_G2pre = np.NAN
        self.label_G3pre = np.NAN
        self.label_G4pre = np.NAN
        self.label_G5pre = np.NAN

        self.tmpdata = []  # 必须是回测系统变量
        self.trend = 0
        self.N = 0


    ##############################################策略模块的基本操作###############################################
    # ----------------------------------------------------------------------
    def onInit(self):
        """初始化策略（必须由用户继承实现）"""
        self.writeCtaLog(u'%s策略初始化' % self.name)

        # 载入历史数据，并采用回放计算的方式初始化策略数值
        initData = self.loadBar(self.initDays)
        for bar in initData:
            Data = pd.DataFrame([bar.date+' '+bar.time,bar.close],index= ['tradeDate','close']).T.iloc[0]

            if self.N == 0 or self.N == 1 or self.N == 2:
                self.tmpdata.append(Data)
                self.N = self.N + 1
            else:
                self.N = self.N + 1
                self.tmpdata.append(Data)
                if len(self.tmpdata)>3:
                    self.tmpdata = self.tmpdata[-3:]
                #########################################趋势判别向################################################################

                R1 = self.G1.Input(pd.DataFrame(self.tmpdata))

                if R1 == None:
                    pass
                elif R1 == 1:
                    # 高点
                    # 确认标记
                    R2 = self.G2up.Input(pd.DataFrame(self.G1.IndexH[-3:]))
                    if R2 == None:
                        pass
                    elif R2 == 1:
                        # 高点
                        # 确认标记
                        L = label(self.G2up.IndexH[-2:])
                        if L == 0:
                            pass
                        else:
                            if L == 1:
                                self.G2up.Hline = Data.close * self.shang
                                self.G2down.Lline = self.G2down.IndexL[-1].close
                            else:
                                self.G2up.Hline = self.G2up.IndexH[-1].close
                            self.label_G2 = L * 2

                        R3 = self.G3up.Input(pd.DataFrame(self.G2up.IndexH[-3:]))
                        if R3 == None:
                            pass
                        elif R3 == 1:
                            # 确认标记
                            L = label(self.G3up.IndexH[-2:])
                            if L == 0:
                                pass
                            else:
                                # 确认突破线
                                if L == 1:
                                    self.G3up.Hline = Data.close * self.shang
                                    self.G3down.Lline = self.G3down.IndexL[-1].close
                                else:
                                    self.G3up.Hline = self.G3up.IndexH[-1].close
                                self.label_G3 = L * 3

                            R4 = self.G4up.Input(pd.DataFrame(self.G3up.IndexH[-3:]))
                            if R4 == None:
                                pass
                            elif R4 == 1:
                                # 确认标记
                                L = label(self.G4up.IndexH[-2:])
                                if L == 0:
                                    pass
                                else:
                                    if L == 1:
                                        self.G4up.Hline = Data.close * self.shang
                                        self.G4down.Lline = self.G4down.IndexL[-1].close
                                    else:
                                        self.G4up.Hline = self.G4up.IndexH[-1].close
                                    self.label_G4 = L * 4
                                R5 = self.G5up.Input(pd.DataFrame(self.G4up.IndexH[-3:]))
                                if R5 == None:
                                    pass
                                elif R5 == 1:
                                    # 确认标记
                                    L = label(self.G5up.IndexH[-2:])
                                    if L == 0:
                                        pass
                                    else:
                                        if L == 1:
                                            self.G5up.Hline = Data.close * self.shang
                                            if len(self.G5down.IndexL) != 0:
                                                self.G5down.Lline = self.G5down.IndexL[-1].close
                                        else:
                                            self.G5up.Hline = self.G5up.IndexH[-1].close
                                        self.label_G5 = L * 5

                        else:
                            pass

                    else:
                        pass
                else:
                    # 低点
                    R2 = self.G2down.Input(pd.DataFrame(self.G1.IndexL[-3:]))
                    if R2 == None:
                        pass
                    elif R2 == -1:
                        # 确认标记
                        L = label(self.G2down.IndexL[-2:])
                        if L == 0:
                            pass
                        else:
                            if L == -1:
                                self.G2down.Lline = Data.close * self.xia
                                self.G2up.Hline = self.G2up.IndexH[-1].close
                            else:
                                self.G2down.Lline = self.G2down.IndexL[-1].close
                            self.label_G2 = L * 2
                        R3 = self.G3down.Input(pd.DataFrame(self.G2down.IndexL[-3:]))
                        if R3 == None:
                            pass
                        elif R3 == -1:
                            # 确认标记
                            L = label(self.G3down.IndexL[-2:])
                            if L == 0:
                                pass
                            else:
                                # 确认突破线
                                if L == -1:
                                    self.G3down.Lline = Data.close * self.xia
                                    self.G3up.Hline = self.G3up.IndexH[-1].close
                                else:
                                    self.G3down.Lline = self.G3down.IndexL[-1].close
                                self.label_G3 = L * 3

                            R4 = self.G4down.Input(pd.DataFrame(self.G3down.IndexL[-3:]))
                            if R4 == None:
                                pass
                            elif R4 == -1:
                                # 确认标记
                                L = label(self.G4down.IndexL[-2:])
                                if L == 0:
                                    pass
                                else:
                                    if L == -1:
                                        self.G4down.Lline = Data.close * self.xia
                                        if len(self.G4up.IndexH) != 0:
                                            self.G4up.Hline = self.G4up.IndexH[-1].close
                                    else:
                                        self.G4down.Lline = self.G4down.IndexL[-1].close
                                    self.label_G4 = L * 4
                                R5 = self.G5down.Input(pd.DataFrame(self.G5down.IndexL[-3:]))
                                if R5 == None:
                                    pass
                                elif R5 == -1:
                                    # 确认标记
                                    L = label(self.G5down.IndexL[-2:])
                                    if L == 0:
                                        pass
                                    else:
                                        if L == -1:
                                            self.G5down.Lline = Data.close * self.xia
                                            if len(self.G5up.IndexH) != 0:
                                                self.G5up.Hline = self.G5up.IndexH[-1].close
                                        else:
                                            self.G5down.Lline = self.G5down.IndexL[-1].close
                                        self.label_G5 = L * 5
                        else:
                            pass

                # 3
                if self.label_G3 == -3 and Data.close > self.G3up.Hline:
                    self.label_G3 = 3
                if self.label_G3 == 3 and Data.close < self.G3down.Lline:
                    self.label_G3 = -3


                if self.label_G4 == -4 and Data.close > self.G4up.Hline:
                    self.label_G4 = 4
                if self.label_G4 == 4 and Data.close < self.G4down.Lline:
                    self.label_G4 = -4

                if self.label_G5 == -5 and Data.close > self.G5up.Hline:
                    self.label_G5 = 5
                if self.label_G5 == 5 and Data.close < self.G5down.Lline:
                    self.label_G5 = -5

            self.label_G2pre = self.label_G2
            self.label_G3pre = self.label_G3
            self.label_G4pre = self.label_G4
            self.label_G5pre = self.label_G5



        self.putEvent()

    # ----------------------------------------------------------------------
    def onStart(self):
        """启动策略（必须由用户继承实现）"""
        self.writeCtaLog(u'%s策略启动' % self.name)
        self.putEvent()

    # ----------------------------------------------------------------------
    def onStop(self):
        """停止策略（必须由用户继承实现）"""
        self.writeCtaLog(u'%s策略停止' % self.name)
        self.putEvent()

    ##################################################策略逻辑模块#################################################
    # ----------------------------------------------------------------------
    def onTick(self, tick):
        """收到行情TICK推送（必须由用户继承实现）"""
        self.bg.updateTick(tick)

    # ----------------------------------------------------------------------
    def onBar(self, bar):
        """收到Bar推送（必须由用户继承实现）"""
        # 撤销之前发出的尚未成交的委托（包括限价单和停止单）
        for orderID in self.orderList:
            self.cancelOrder(orderID)
        self.orderList = []

        Data = pd.DataFrame([bar.date + ' ' + bar.time, bar.close], index=['tradeDate', 'close']).T.iloc[0]

        if self.N == 0 or self.N == 1 or self.N == 2:
            self.tmpdata.append(Data)
            self.N = self.N + 1
        else:
            self.N = self.N + 1
            self.tmpdata.append(Data)
            if len(self.tmpdata) > 3:
                self.tmpdata = self.tmpdata[-3:]
            #########################################趋势判别向################################################################

            R1 = self.G1.Input(pd.DataFrame(self.tmpdata))

            if R1 == None:
                pass
            elif R1 == 1:
                # 高点
                # 确认标记
                R2 = self.G2up.Input(pd.DataFrame(self.G1.IndexH[-3:]))
                if R2 == None:
                    pass
                elif R2 == 1:
                    # 高点
                    # 确认标记
                    L = label(self.G2up.IndexH[-2:])
                    if L == 0:
                        pass
                    else:
                        if L == 1:
                            self.G2up.Hline = Data.close * self.shang
                            self.G2down.Lline = self.G2down.IndexL[-1].close
                        else:
                            self.G2up.Hline = self.G2up.IndexH[-1].close
                        self.label_G2 = L * 2

                    R3 = self.G3up.Input(pd.DataFrame(self.G2up.IndexH[-3:]))
                    if R3 == None:
                        pass
                    elif R3 == 1:
                        # 确认标记
                        L = label(self.G3up.IndexH[-2:])
                        if L == 0:
                            pass
                        else:
                            # 确认突破线
                            if L == 1:
                                self.G3up.Hline = Data.close * self.shang
                                self.G3down.Lline = self.G3down.IndexL[-1].close
                            else:
                                self.G3up.Hline = self.G3up.IndexH[-1].close
                            self.label_G3 = L * 3

                        R4 = self.G4up.Input(pd.DataFrame(self.G3up.IndexH[-3:]))
                        if R4 == None:
                            pass
                        elif R4 == 1:
                            # 确认标记
                            L = label(self.G4up.IndexH[-2:])
                            if L == 0:
                                pass
                            else:
                                if L == 1:
                                    self.G4up.Hline = Data.close * self.shang
                                    self.G4down.Lline = self.G4down.IndexL[-1].close
                                else:
                                    self.G4up.Hline = self.G4up.IndexH[-1].close
                                self.label_G4 = L * 4
                            R5 = self.G5up.Input(pd.DataFrame(self.G4up.IndexH[-3:]))
                            if R5 == None:
                                pass
                            elif R5 == 1:
                                # 确认标记
                                L = label(self.G5up.IndexH[-2:])
                                if L == 0:
                                    pass
                                else:
                                    if L == 1:
                                        self.G5up.Hline = Data.close * self.shang
                                        if len(self.G5down.IndexL) != 0:
                                            self.G5down.Lline = self.G5down.IndexL[-1].close
                                    else:
                                        self.G5up.Hline = self.G5up.IndexH[-1].close
                                    self.label_G5 = L * 5

                    else:
                        pass

                else:
                    pass
            else:
                # 低点
                R2 = self.G2down.Input(pd.DataFrame(self.G1.IndexL[-3:]))
                if R2 == None:
                    pass
                elif R2 == -1:
                    # 确认标记
                    L = label(self.G2down.IndexL[-2:])
                    if L == 0:
                        pass
                    else:
                        if L == -1:
                            self.G2down.Lline = Data.close * self.xia
                            self.G2up.Hline = self.G2up.IndexH[-1].close
                        else:
                            self.G2down.Lline = self.G2down.IndexL[-1].close
                        self.label_G2 = L * 2
                    R3 = self.G3down.Input(pd.DataFrame(self.G2down.IndexL[-3:]))
                    if R3 == None:
                        pass
                    elif R3 == -1:
                        # 确认标记
                        L = label(self.G3down.IndexL[-2:])
                        if L == 0:
                            pass
                        else:
                            # 确认突破线
                            if L == -1:
                                self.G3down.Lline = Data.close * self.xia
                                self.G3up.Hline = self.G3up.IndexH[-1].close
                            else:
                                self.G3down.Lline = self.G3down.IndexL[-1].close
                            self.label_G3 = L * 3

                        R4 = self.G4down.Input(pd.DataFrame(self.G3down.IndexL[-3:]))
                        if R4 == None:
                            pass
                        elif R4 == -1:
                            # 确认标记
                            L = label(self.G4down.IndexL[-2:])
                            if L == 0:
                                pass
                            else:
                                if L == -1:
                                    self.G4down.Lline = Data.close * self.xia
                                    if len(self.G4up.IndexH) != 0:
                                        self.G4up.Hline = self.G4up.IndexH[-1].close
                                else:
                                    self.G4down.Lline = self.G4down.IndexL[-1].close
                                self.label_G4 = L * 4
                            R5 = self.G5down.Input(pd.DataFrame(self.G5down.IndexL[-3:]))
                            if R5 == None:
                                pass
                            elif R5 == -1:
                                # 确认标记
                                L = label(self.G5down.IndexL[-2:])
                                if L == 0:
                                    pass
                                else:
                                    if L == -1:
                                        self.G5down.Lline = Data.close * self.xia
                                        if len(self.G5up.IndexH) != 0:
                                            self.G5up.Hline = self.G5up.IndexH[-1].close
                                    else:
                                        self.G5down.Lline = self.G5down.IndexL[-1].close
                                    self.label_G5 = L * 5
                    else:
                        pass

            # 3
            if self.label_G3 == -3 and Data.close > self.G3up.Hline:
                self.label_G3 = 3
            if self.label_G3 == 3 and Data.close < self.G3down.Lline:
                self.label_G3 = -3

            if self.label_G4 == -4 and Data.close > self.G4up.Hline:
                self.label_G4 = 4
            if self.label_G4 == 4 and Data.close < self.G4down.Lline:
                self.label_G4 = -4

            if self.label_G5 == -5 and Data.close > self.G5up.Hline:
                self.label_G5 = 5
            if self.label_G5 == 5 and Data.close < self.G5down.Lline:
                self.label_G5 = -5

        #######################################信号判断#######################################################
        # 撤销之前发出的尚未成交的委托（包括限价单和停止单）
        for orderID in self.orderList:
            self.cancelOrder(orderID)
        self.orderList = []

        """
        逻辑1
            入：当趋势早已为正，且当前次级趋势为正
            出：当前次级趋势为负
        """
        if self.label_G2 > 0 and self.label_G3 > 0 and self.label_G3pre > 0 and (self.trend == 0 or self.trend == -1):
            self.trend = 1
            print "入场+"
            print Data.tradeDate, self.label_G3, self.label_G5
            #平空仓
            if self.pos < 0:
                l = self.cover(bar.close, abs(self.pos))
                self.orderList.extend(l)
            #入多仓
            if self.pos <= 0:
                l = self.buy((bar.close * 1.1), self.fixedSize)
                self.orderList.extend(l)

        if self.label_G2 < 0 and self.trend == 1:
            self.trend = 0
            print "出场+"
            print Data.tradeDate, self.label_G3, self.label_G5
            #平多仓
            if self.pos > 0:
                l = self.sell(bar.close, abs(self.pos))
                self.orderList.extend(l)

        if self.label_G2 < 0 and self.label_G3 < 0 and self.label_G3pre < 0 and (self.trend == 0 or self.trend == 1):
            self.trend = -1
            print "入场-"
            print Data.tradeDate, self.label_G3, self.label_G5
            #平多仓
            if self.pos > 0:
                l = self.sell(bar.close, abs(self.pos))
                self.orderList.extend(l)
            #入空仓
            if self.pos >= 0 :
                l = self.short((bar.close * 0.9), self.fixedSize)
                self.orderList.extend(l)

        if self.label_G2 > 0 and self.trend == -1:
            self.trend = 0
            print "出场-"
            print Data.tradeDate, self.label_G3, self.label_G5
            #平空仓
            if self.pos < 0:
                l = self.cover(bar.close, abs(self.pos))
                self.orderList.extend(l)
        #######################################更新标签#######################################################
        self.label_G2pre = self.label_G2
        self.label_G3pre = self.label_G3
        self.label_G4pre = self.label_G4
        self.label_G5pre = self.label_G5


        # 同步数据到数据库
        self.saveSyncData()

        # 发出状态更新事件
        self.putEvent()

    # ----------------------------------------------------------------------
    def onOrder(self, order):
        """收到委托变化推送（必须由用户继承实现）"""
        # 对于无需做细粒度委托控制的策略，可以忽略onOrder
        pass

    ###############################################交易模块####################################################
    # ----------------------------------------------------------------------
    def onTrade(self, trade):
        if self.pos != 0:
            # 多头开仓成交后，撤消空头委托
            if self.pos > 0:
                for shortOrderID in self.shortOrderIDList:
                    self.cancelOrder(shortOrderID)
            # 反之同样
            elif self.pos < 0:
                for buyOrderID in self.buyOrderIDList:
                    self.cancelOrder(buyOrderID)

            # 移除委托号
            for orderID in (self.buyOrderIDList + self.shortOrderIDList):
                if orderID in self.orderList:
                    self.orderList.remove(orderID)

        # 发出状态更新事件
        self.putEvent()

    # ----------------------------------------------------------------------
    def sendOcoOrder(self, buyPrice, shortPrice, volume):
        """
        发送OCO委托

        OCO(One Cancel Other)委托：
        1. 主要用于实现区间突破入场
        2. 包含两个方向相反的停止单
        3. 一个方向的停止单成交后会立即撤消另一个方向的
        """
        # 发送双边的停止单委托，并记录委托号
        self.buyOrderIDList = self.buy(buyPrice, volume, True)
        self.shortOrderIDList = self.short(shortPrice, volume, True)

        # 将委托号记录到列表中
        self.orderList.extend(self.buyOrderIDList)
        self.orderList.extend(self.shortOrderIDList)

    # ----------------------------------------------------------------------
    def onStopOrder(self, so):
        """停止单推送"""
        pass
        """

        """

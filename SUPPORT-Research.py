def label(Data,Index,Indexlabel,n):
    for i in range(len(Index)):
        if i == 0:
            pass
        else:
            if Data.loc[Index[i-1],'close'] > Data.loc[Index[i],'close']:
                Data.loc[Index[i],Indexlabel] = -n
            elif Data.loc[Index[i-1],'close'] < Data.loc[Index[i],'close']:
                Data.loc[Index[i],Indexlabel] = n
    return Data


def upgrade(hldata, yu=0.0002):
    """
    寻找高低点
    输入：
        Dataframe，时间(可以非连续)，价格
    输出：
        index1，index2, 分别是高点的坐标 和 低点的坐标
    """
    IndexH = []
    IndexL = []
    equ_ppredata = []
    equ_predata = []
    for i in range(len(hldata)):
        if i == 0 or i == 1:
            pass
        else:
            ppredata = hldata.iloc[i - 2]
            preldata = hldata.iloc[i - 1]
            nowdata = hldata.iloc[i]

            # 初始化
            if len(equ_ppredata) == 0 or len(equ_predata) == 0:
                equ_ppredata = ppredata
                equ_predata = preldata

            if abs(preldata.close - nowdata.close) < yu * nowdata.close:
                # 走平了
                # 前前点不变
                # 前点更新
                equ_predata = nowdata
            else:
                # 未走平
                # 做出判断

                # 与原本一致
                Boolpre = equ_ppredata.close < equ_predata.close
                Boolnow = equ_predata.close < nowdata.close
                if Boolpre and Boolnow:
                    # 正正
                    equ_ppredata = preldata
                    equ_predata = nowdata

                elif not Boolpre and not Boolnow:
                    # 负负
                    equ_ppredata = preldata
                    equ_predata = nowdata

                # 与原本不一致
                else:
                    if Boolpre and not Boolnow:
                        # 正负，高点
                        IndexH.append(equ_predata.name)
                        equ_ppredata = preldata
                        equ_predata = nowdata
                    elif not Boolpre and Boolnow:
                        # 负正，低点
                        IndexL.append(equ_predata.name)
                        equ_ppredata = preldata
                        equ_predata = nowdata
                # 无论什么判断，都要更新高低点
    return IndexH, IndexL

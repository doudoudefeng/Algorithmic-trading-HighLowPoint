# Algorithmic trading-HighLowPoint
Algorithmic trading
本项目为 知乎专栏：。。。 配套程序  
环境：  
  研究：jupyter notebook  
  回测框架：VNPY  
  数据库：mongoDB  
本项目一共分为两个部分  
1. 研究环境下的的指标计算和画图，环境为 jupyter notebook  
  1.1 SUPPORT-Research   
  1.2 Research  
2. 交易环境下的指标计算和回测框架，环境为 vnpy  
  2.1 SUPPORT-Trading  
  2.2 BackTest  

在本项目中一共实现了两种方式去完成高低点分型迭代的计算，分别对应研究模式下的计算和回测模式下的计算  
SUPPORT-Research 研究环境下高低点分型迭代的计算，为了提高效率，使用了矩阵运算，使用时需要将数据全部导入到函数中  
SUPPORT-Trading 策略环境下高低点分型迭代的计算，为了代码能够在不同交易框架下移植，所有的运算和数据储存全部在类对象内进行，使用时需要逐k线输入数据  
Research 研究文档，包括数据的导入，指标的计算，数据可视化  
BackTest 回测文档，在vnpy回测框架下的高低点分型策略的策略文件  
 

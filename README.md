# 2024CSIG-飞桨、工银瑞信金融科技挑战赛
## 赛题
###基于股票K线图的股票预测

##任务描述
  股票市场是一个充满挑战与机遇的领域，其动态变化的特性要求投资者具备敏锐的洞察力和高效的决策能力。近年来，随着计算机视觉技术的飞速发展，其在金融领域的应用也逐渐受到广泛关注。
  本赛题由百度飞桨和工银瑞信联合设置，旨在通过利用计算机视觉的模型和网络结构，结合交易数据（如高开低收、成交量、成交金额等），探索一种新型的股票排名预测方法。
  参赛者需要完成以下两个主要任务：
  1、K线图的创新绘制：基于给定的交易数据，参赛者需要设计并绘制一种新型的K线图。这种K线图可以不是传统的形式，而是需要开动脑筋，创造出对计算机视觉模型更加友好的图形或像素图。这要求参赛者不仅要理解K线图的本质，还要具备创新思维和图形设计能力。
  2、股票排名预测：利用计算机视觉相关的技术，对自定义的股票K线图进行分析，并预测股票的排名。参赛者需要选择合适的计算机视觉模型和网络结构，对K线图进行特征提取和模式识别，从而实现对股票排名的预测。请注意，模型的设计应避免过拟合，并且应根据股票数据的特性对原有网络结构进行必要的定制化修改。

## 评价标准
评价标准为Rank IC（Rank Information Coefficient），即计算预测分值的排序值与未来5天收益率排序值之间的相关系数。

## 初赛阶段
在初赛阶段，排名将在AI Studio（https://aistudio.baidu.com/ ）排行榜中公布。根据排行榜分数决定晋级团队，晋级比例后续公布。报名后可见“数据集tab”。

## 复赛阶段
在复赛阶段，参赛者需根据组织者公布的最近一周交易日的股票因子特征预测下一周交易日的股票排名得分。最终得分=股票排名得分（40%）+算法报告（40%）+K线图重绘策略（20%）。 组织者将根据参赛提交的股票排名得分同实盘排名做相似度计算，根据股票上中下分段中各选N支股票，做收益区分度计算，并做综合评分。

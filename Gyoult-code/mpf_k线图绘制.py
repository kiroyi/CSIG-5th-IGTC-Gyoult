# 导入包
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import zipfile
import warnings
import json
import mplfinance as mpf
from collections import defaultdict
from tqdm import tqdm
import os
import pickle
import argparse

# 忽略所有警告
warnings.filterwarnings("ignore")
# 导入自定义包
sys.path.append("work")


# 转换 int64 为 int
def convert_to_int(data):
    if isinstance(data, np.ndarray):
        return data.tolist()  # 如果是数组，转换为列表
    elif isinstance(data, dict):
        return {key: convert_to_int(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_to_int(item) for item in data]
    elif isinstance(data, np.int64):
        return int(data)  # 转换为 int
    return data  # 其他类型保持不变


custom_style = mpf.make_mpf_style(
    base_mpf_style='charles',   # 基础样式
    # gridaxis='both',
    gridstyle='',
    # y_on_right=True,
    # marketcolors=mc,
    # edgecolor='b',
    # figcolor='white',
    # facecolor='white', 
    # gridcolor='c'
    )


binance_dark = {
    "base_mpl_style": "dark_background",
    "marketcolors": {
        "candle": {"up": "#3dc985", "down": "#ef4f60"},  
        "edge": {"up": "#3dc985", "down": "#ef4f60"},  
        "wick": {"up": "#3dc985", "down": "#ef4f60"},  
        # "ohlc": {"up": "#3dc985", "down": "#ef4f60"},
        "ohlc": {"up": "green", "down": "red"},
        # "volume": {"up": "#3dc985", "down": "#ef4f60"},  
        # "vcedge": {"up": "#3dc985", "down": "#ef4f60"},  
        "volume": {"up": "#247252", "down": "#82333f"},  
        "vcedge": {"up": "#247252", "down": "#82333f"},  
        "vcdopcod": False,
        "alpha": 1,
    },
    "mavcolors": ("#ad7739", "#a63ab2", "#62b8ba"),
    "facecolor": "#1b1f24",
    "gridcolor": "#2c2e31",
    "gridstyle": "",
    "y_on_right": True,
    "rc": {
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.edgecolor": "#474d56",
        "axes.titlecolor": "red",
        "figure.facecolor": "#161a1e",
        "figure.titlesize": "x-large",
        "figure.titleweight": "semibold",
    },
    "base_mpf_style": "binance-dark",

}

def process_stock(stock, size=5.12):
    train_idx = []
    train_feature = []
    train_label = []

    groups = list(grouped_dict[stock].keys())
    for i in range(len(groups) - 1):

        group = groups[i]
        if (stock, group) not in train_idx:
            
            tmp = grouped_dict[stock][group]

            # 检查 NaN 值
            if np.any(np.isnan(tmp['Label'].values)):
                continue
            
            # 定义添加的移动平均线和 MACD 信息
            add_plots = [
                # K线图平均线
                mpf.make_addplot(tmp['MA_5'], color='#ad7739', width=1, panel=0),
                mpf.make_addplot(tmp['MA_10'], color='#a63ab2', width=1, panel=0),
                mpf.make_addplot(tmp['MA_20'], color='#62b8ba', width=1, panel=0),
                mpf.make_addplot(tmp['MA_30'], color='#4e79a7', width=1, panel=0),
                
                # 成交量信息
                mpf.make_addplot(tmp['Trunover'], width=1, color='#76b7b2', panel=1), # 青色
                mpf.make_addplot(tmp['Volume_MA_5'], width=1, color='#edc948', panel=1), # 黄色
                mpf.make_addplot(tmp['Volume_MA_10'], width=1, color='#b07aa1', panel=1), # 紫色
                

                # 添加 MACD 柱状图
                mpf.make_addplot(tmp['MACD Histogram'], panel=2, type='bar', color=np.where(tmp['MACD Histogram'] > 0, "#3dc985", "#ef4f60")),
                # 添加 MACD 信息
                mpf.make_addplot(tmp['DIFF'], width=1, color='#ff9da7', panel=2),
                mpf.make_addplot(tmp['DEA'], width=1, color='#9c755f', panel=2),
            ]
                
            # 绘制图像
            fig, axes = mpf.plot(
                tmp,
                type='candle',
                style=binance_dark,  # 应用自定义样式
                ylabel="",
                ylabel_lower="",
                volume=True,
                addplot=add_plots,
                panel_ratios=(3, 1, 1),  # 上部分K线图、中间成交量图、下部分MACD图的比例
                figsize=(size, size),  # 设置图表大小为 512x512 像素
                update_width_config=dict(candle_linewidth=0.5, candle_width=0.5),
                axisoff=True,
                # savefig='test-mplfiance.png',
                returnfig=True  # 返回 Figure 对象
            )
            
            # 保存图像为矩阵
            fig.canvas.draw()  # 绘制图像
            image_array = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)  # 获取 RGB 数据
            image_array = image_array.reshape(fig.canvas.get_width_height()[::-1] + (3,))  # 转换为矩阵格式
            
            train_idx.append((stock, group))
            train_feature.append(image_array)
            train_label.append(tmp['Label'].values)
    
    # 如何该股票没有可用数据
    if not train_feature:
        return
    
    # mpf绘制得更精细，因此以股票为单位进行保存
    np.save(f"train_k_line_5/features/{stock}.npy", np.stack(train_feature))
    
    data_for_json = [list(item) for item in train_idx]
    data_for_json = convert_to_int(data_for_json)
    # 保存索引信息
    with open(f'train_k_line_5/indices/{stock}.json', 'w') as file:
        json.dump(data_for_json, file, indent=4)

    # 保存标签信息
    labels_arr = np.stack(train_label)
    np.save(f"train_k_line_5/labels/{stock}.npy", labels_arr)
    
    return 



# 创建二级索引的 defaultdict
grouped_dict = defaultdict(dict)
# 从 pickle 文件加载 grouped_dict
with open('train_grouped_dict.pkl', 'rb') as f:
    grouped_dict = pickle.load(f)

if __name__ == "__main__":
    
    os.makedirs("train_k_line_5/features", exist_ok=True)
    os.makedirs("train_k_line_5/indices", exist_ok=True)
    os.makedirs("train_k_line_5/labels", exist_ok=True)
    
    # Create parser
    parser = argparse.ArgumentParser(description="train of argparse")
    
    # Add parameters
    parser.add_argument("--start", type=int, default=0, help="start index")
    parser.add_argument("--end", type=int, default=5464, help="end  index") 

    args = parser.parse_args()
    
    p_start = args.start
    p_end = args.end    
    
    slice = dict(list(grouped_dict.items())[p_start:p_end])
    
    # 循环处理每一只股票
    for stock in tqdm(slice.keys()):
        process_stock(stock)
        
    print("------finished-----")
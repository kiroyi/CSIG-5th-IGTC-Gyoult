# 导入包
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import zipfile
import warnings
import pickle
from collections import defaultdict
from tqdm import tqdm
import json
import os
import argparse

# 忽略所有警告
warnings.filterwarnings("ignore")
# 导入自定义包
sys.path.append("work")
from candle2 import Canva

# 加载保存的预处理分组数据
# 创建二级索引的 defaultdict
grouped_dict = defaultdict(dict)

with open('train_grouped_dict.pkl', 'rb') as f:
    try:
        grouped_dict = pickle.load(f)
    except EOFError:
        print("EOFError: The file might be empty or corrupted.")
        

# 对单只股票进行处理
# 这里的 train_idx 是 (stock, group) 的元组，表示某一周某一只特定股票
# train_feature 就是 K 线图的 numpy 矩阵。这里采用了一周的数据绘制 K 线图
# train_label 则是该股票本周每一天对应的 label
def process_stock(stock, size=64):
    train_idx = []
    train_feature = []
    train_label = []

    groups = list(grouped_dict[stock].keys())
    for i in range(len(groups) - 1):
        group = groups[i]
        if (stock, group) not in train_idx:
            tmp = grouped_dict[stock][group]
            label_arr = tmp['Label'].values
            canva = Canva(size, tmp)
            if not np.any(np.isnan(label_arr)):
                train_idx.append((stock, group))
                canva.draw_all_bars(width=10)
                train_feature.append(canva.matrix)
                train_label.append(label_arr)
    
    return train_idx, train_feature, train_label

if __name__ == "__main__":

    os.makedirs("work/train_k_line_5/", exist_ok=True)
    
    train_indices = []
    train_features = []
    train_labels = []
    
    # 绘制的图像为彩色，且图像大小增加到了160 × 160，因此只能分片进行处理并保存
    # 32G机器下我们的分片是：0-2000，2000-4000，4000-5464  
     
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
        # print(stock)
        train_idx, train_feature, train_label = process_stock(stock, 160)
        train_indices.extend(train_idx)
        train_features.extend(train_feature)
        train_labels.extend(train_label)

    data_for_json = [list(item) for item in train_indices]

    # 保存索引信息
    with open(f'work/train_k_line_5/test_indices_{p_start}_{p_end}.json', 'w') as file:
        json.dump(data_for_json, file, indent=4)

    # 保存标签信息
    labels_arr = np.stack(train_labels)
    np.save(f"work/train_k_line_5/train_labels_{p_start}_{p_end}.npy", labels_arr)
    
    
    
    # 保存 K 线图 (train_features) 为 numpy 格式
    chunk_size = 100000  # 根据你的内存情况调整这个值，内存过大就不用分 chunk 存储
    num_chunks = (len(train_features) + chunk_size - 1) // chunk_size

    for i in tqdm(range(num_chunks)):
        start = i * chunk_size
        end = min(start + chunk_size, len(train_features))
        chunk = np.stack(train_features[start:end])
        # 这里的1需要手动调整，避免名称重复，我们的结果是：0-2000(生成3个)，2000-4000(生成3个)，4000-5464(生成2个)
        np.save(f"work/test_dataset/test_features_{i+1}.npy", chunk)
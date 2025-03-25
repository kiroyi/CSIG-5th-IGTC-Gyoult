#!/bin/bash

# 设置参数
p1_start=0
p1_end=2000

p2_start=2000
p2_end=4000

p3_start=4000
p3_end=5464


python3 plt_k线图绘制.py --start $p1_start --end $p1_end
python3 plt_k线图绘制.py --start $p2_start --end $p2_end
python3 plt_k线图绘制.py --start $p3_start --end $p3_end
#!/bin/bash

# 请在使用前安装mplfinance包
# pip3 install mplfinance
# 因为生成得图像更复杂，因此只能每500个进行分片

# 设置参数
p1_start=0
p1_end=500

p2_start=500
p2_end=1000

p3_start=1000
p3_end=1500

p4_start=1500
p4_end=2000

p5_start=2000
p5_end=2500

p6_start=2500
p6_end=3000

p7_start=3000
p7_end=3500

p8_start=3500
p8_end=4000

p9_start=4000
p9_end=5000

p10_start=5000
p10_end=5464


python3 mpf_k线图绘制.py --start $p1_start --end $p1_end
python3 mpf_k线图绘制.py --start $p2_start --end $p2_end
python3 mpf_k线图绘制.py --start $p3_start --end $p3_end
python3 mpf_k线图绘制.py --start $p4_start --end $p4_end
python3 mpf_k线图绘制.py --start $p5_start --end $p5_end
python3 mpf_k线图绘制.py --start $p6_start --end $p6_end
python3 mpf_k线图绘制.py --start $p7_start --end $p7_end
python3 mpf_k线图绘制.py --start $p8_start --end $p8_end
python3 mpf_k线图绘制.py --start $p9_start --end $p9_end
python3 mpf_k线图绘制.py --start $p10_start --end $p10_end
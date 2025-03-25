import numpy as np


class Canva:
    def __init__(self, size, data, n_bars=5, price_plot_ratio=2/3):
        """
        初始化画布类。

        参数:
        size (int): 画布的大小（正方形）。
        data (DataFrame): 包含开盘价、最高价、最低价、收盘价和成交量的数据。
        n_bars (int): 要绘制的K线数量。
        price_plot_ratio (float): 价格部分在画布中的比例。
        """
        self.size = size
        self.n_bars = n_bars
        self.step = self.size / self.n_bars  # 每个K线的宽度
        self.matrix = np.full((size, size, 3), 255, dtype=np.uint8)  # 初始化画布矩阵，填充白色
        self.data = data
        self.all_data = self.data[['Open', 'High', 'Low', 'Close', 'MA_5']].values
        
        min_val = self.all_data.min()  # 价格的最小值
        max_val = self.all_data.max()  # 价格的最大值     
        
        self.prices = self.data[['Open', 'High', 'Low', 'Close']].values  # 提取价格数据
        
        a, b = 0.2, 0.8  # 定义缩放范围
        self.prices = a + (self.prices - min_val) / (max_val - min_val) * (b - a)  # 将价格数据归一化到[0.2, 0.8]
        self.price_offset = (1 - price_plot_ratio) * self.size  # 价格部分的偏移量
        self.prices = self.prices * price_plot_ratio * self.size + self.price_offset - 1  # 将价格数据映射到画布上


        self.volume = self.data['Volume'].abs().values
        self.volume = self.volume / self.volume.max() * (1 - price_plot_ratio) * self.size  # 将成交量数据映射到画布上


        # prices_ma5
        self.prices_ma5 = self.data['MA_5'].values
        self.prices_ma5 = a + (self.prices_ma5 - min_val) / (max_val - min_val) * (b - a)
        self.prices_ma5 = self.prices_ma5 * price_plot_ratio * self.size + self.price_offset - 1 
 
        
        self.volume_ma5 = self.data['Volume_MA_5'].abs().values 
        self.volume_ma5 = self.volume_ma5 / self.volume_ma5.max() * (1 - price_plot_ratio) * self.size # 将成交量数据映射到画布上
        
        if len(self.data) != self.n_bars:
            raise ValueError("Data length must be same as n bars!")  # 数据长度必须与K线数量一致

    def draw_line(self, point_1, point_2, color):
        """
        绘制从 (x1, y1) 到 (x2, y2) 的直线，颜色为 color。

        参数:
        point_1 (tuple): 起点坐标 (x1, y1)。
        point_2 (tuple): 终点坐标 (x2, y2)。
        color (int): 颜色值。
        """
        x1, y1 = point_1
        x2, y2 = point_2
        
        r, g, b = color

        x1, x2 = int(x1), int(x2)
        y1, y2 = int(y1), int(y2)
        
        num_points = max(int(abs(x2 - x1)), int(abs(y2 - y1))) + 1
        x, y = np.linspace(int(x1), int(x2), num_points), np.linspace(int(y1), int(y2), num_points)
        # x, y = np.linspace(int(x1), int(x2), int(abs(x2 - x1)) + 1), np.linspace(int(y1), int(y2), int(abs(y2 - y1)) + 1)    
        
        self.matrix[x.astype(int), y.astype(int), 0] = r
        self.matrix[x.astype(int), y.astype(int), 1] = g
        self.matrix[x.astype(int), y.astype(int), 2] = b


    def draw_filled_rectangle(self, point_1, point_2, color):
        """
        绘制从 (x1, y1) 到 (x2, y2) 的填充矩形，颜色为 color。

        参数:
        point_1 (tuple): 矩形的左下角坐标 (x1, y1)。
        point_2 (tuple): 矩形的右上角坐标 (x2, y2)。
        color (int): 颜色值。
        """
        x1, y1 = point_1
        x2, y2 = point_2
        r, g, b = color
        
        # 确保坐标顺序
        x_min, x_max = round(min(x1, x2)), round(max(x1, x2))
        y_min, y_max = round(min(y1, y2)), round(max(y1, y2))
        
        # 给 RGB 矩阵的指定区域上色
        self.matrix[x_min:x_max + 1, y_min:y_max + 1, 0] = r  # 红色通道
        self.matrix[x_min:x_max + 1, y_min:y_max + 1, 1] = g  # 绿色通道
        self.matrix[x_min:x_max + 1, y_min:y_max + 1, 2] = b  # 蓝色通道


    def draw_hollow_rectangle(self, point_1, point_2, color):
        """
        绘制从 (x1, y1) 到 (x2, y2) 的空心矩形，颜色为 RGB 形式。

        参数:
        point_1 (tuple): 矩形的左下角坐标 (x1, y1)。
        point_2 (tuple): 矩形的右上角坐标 (x2, y2)。
        color (tuple): 颜色值，格式为 (r, g, b)。
        """
        x1, y1 = point_1
        x2, y2 = point_2
        r, g, b = color

        # 确保坐标顺序正确
        x_min, x_max = round(min(x1, x2)), round(max(x1, x2))
        y_min, y_max = round(min(y1, y2)), round(max(y1, y2))
              
        # 绘制矩形的上下边缘
        self.matrix[x_min:x_max + 1, y_min, 0] = r  # 红色通道
        self.matrix[x_min:x_max + 1, y_min, 1] = g  # 绿色通道
        self.matrix[x_min:x_max + 1, y_min, 2] = b  # 蓝色通道

        self.matrix[x_min:x_max + 1, y_max, 0] = r  # 红色通道
        self.matrix[x_min:x_max + 1, y_max, 1] = g  # 绿色通道
        self.matrix[x_min:x_max + 1, y_max, 2] = b  # 蓝色通道

        # 绘制矩形的左右边缘
        self.matrix[x_min, y_min:y_max + 1, 0] = r  # 红色通道
        self.matrix[x_min, y_min:y_max + 1, 1] = g  # 绿色通道
        self.matrix[x_min, y_min:y_max + 1, 2] = b  # 蓝色通道

        self.matrix[x_max, y_min:y_max + 1, 0] = r  # 红色通道
        self.matrix[x_max, y_min:y_max + 1, 1] = g  # 绿色通道
        self.matrix[x_max, y_min:y_max + 1, 2] = b  # 蓝色通道

    def draw_bar(self, idx, ohlc, width=6):
        """
        绘制单个K线。

        参数:
        idx (int): K线的索引。
        ohlc (tuple): 包含开盘价、最高价、最低价和收盘价的元组。
        width (int): K线的宽度。
        """
        open_price, high_price, low_price, close_price = ohlc
        x_coord = self.step / 2 + idx * self.step

        min_oc = min(open_price, close_price)
        max_oc = max(open_price, close_price)
        box_bottom_left = (x_coord - width / 2, min_oc)
        box_upper_right = (x_coord + width / 2, max_oc)
        
        if min_oc == open_price:
            color = (239, 79, 96)
            self.draw_filled_rectangle(box_bottom_left, box_upper_right, color)  # 绿色实心矩形表示开盘价高于收盘价
        else:
            color = (61, 201, 133)
            self.draw_hollow_rectangle(box_bottom_left, box_upper_right, color)  # 空色空心矩形表示开盘价高于收盘价

        self.draw_line((x_coord, low_price), (x_coord, high_price), color)  # 绘制最高价和最低价的竖线

    
    def draw_volume(self, idx, volume, width=6):
        """
        绘制单个成交量柱。

        参数:
        idx (int): 成交量的索引。
        volume (float): 成交量值。
        width (int): 成交量柱的宽度。
        """
        
        
        open_price, high_price, low_price, close_price = self.prices[idx]
        min_oc = min(open_price, close_price)
        
        x_coord = self.step / 2 + idx * self.step

        box_bottom_left = (x_coord - width / 2, 0)
        box_upper_right = (x_coord + width / 2, volume)
        if min_oc == open_price:
            color = (239, 79, 96)
            self.draw_filled_rectangle(box_bottom_left, box_upper_right, color)  # 绿色实心矩形表示开盘价高于收盘价
        else:
            color = (61, 201, 133)
            self.draw_hollow_rectangle(box_bottom_left, box_upper_right, color)  # 空色空心矩形表示开盘价高于收盘价
    
    
    def draw_ma_line(self, ma_values, color):
        """
        绘制单个ma线。

        参数:
        """
        for idx, value in enumerate(ma_values):
            if idx == 0:
                continue
            
            x_coord_start = self.step / 2 + (idx - 1) * self.step
            x_coord_end = self.step / 2 + idx * self.step

            y_coord_start = ma_values[idx - 1]
            y_coord_end = ma_values[idx]
            
            self.draw_line((x_coord_start, y_coord_start), (x_coord_end, y_coord_end), color)
    
    def draw_all_bars(self, width=6):
        """
        绘制所有K线和成交量柱。

        参数:
        width (int): K线和成交量柱的宽度。
        """
        # for idx, macd in enumerate(self.macd):
        #     self.draw_macd(idx, macd, self.macd_offset - 1, width)  # 绘制所有,macd
        for idx, volume in enumerate(self.volume):
            self.draw_volume(idx, volume, width)  # 绘制所有成交量柱
        for idx, ohlc in enumerate(self.prices):
            self.draw_bar(idx, ohlc, width)  # 绘制所有K线
            
        # 绘制price ma5折线
        self.draw_ma_line(self.prices_ma5, color=(173, 119, 57))
        # 绘制volume ma5折线
        self.draw_ma_line(self.volume_ma5, color=(78, 121, 167))
        

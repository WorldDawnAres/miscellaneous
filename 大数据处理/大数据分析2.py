import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
matplotlib.rcParams['axes.unicode_minus'] = False
# 构造模拟数据
np.random.seed(42)
num_products = 100
prices = np.random.uniform(100, 2000, size=num_products)  # 随机价格 100~2000 元
sales = (3000 / (prices + 100)) * np.random.uniform(0.5, 1.5, size=num_products) * 100  # 模拟销量呈价格负相关

df = pd.DataFrame({'价格': prices, '销量': sales})

# 绘制散点图
plt.figure(figsize=(8, 5))
plt.scatter(df['价格'], df['销量'], alpha=0.7, color='teal')
plt.title('商品销量与价格关系散点图')
plt.xlabel('价格（元）')
plt.ylabel('销量（件）')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
# 模拟商品品类与销量数据
categories = ['手机', '电脑', '耳机', '路由器', '手表', '平板', '电视', '显示器', '音响', '键盘', '鼠标', '相机']
sales = np.random.randint(5000, 30000, size=len(categories))
df2 = pd.DataFrame({'品类': categories, '销量': sales})
df2 = df2.sort_values(by='销量', ascending=False).head(10)

# 绘制条形图
plt.figure(figsize=(8, 5))
plt.bar(df2['品类'], df2['销量'], color='coral')
plt.title('热销品类Top10条形图')
plt.xlabel('商品品类')
plt.ylabel('销量（件）')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

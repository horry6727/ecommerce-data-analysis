import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine

# ========== 1. 连接数据库，获取完整数据 ==========
db_connection_str = 'mysql+pymysql://root:123456@localhost:3306/ecommerce_db?charset=utf8mb4'
engine = create_engine(db_connection_str)

# 查询需要包含 title 字段，用于画图4
query = "SELECT title, price, rating FROM books"
df = pd.read_sql(query, engine)

# 中文显示设置（防止图表中文变成方框）
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False 

# ========== 2. 创建 2x2 四宫格画布 ==========
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('电商书籍数据分析看板 (无分类字段版)', fontsize=18, fontweight='bold', y=0.95)

# ---------- 图1：评分分布（回答：评分主要集中在哪个区间？） ----------
axes[0, 0].hist(df['rating'], bins=20, color='mediumpurple', edgecolor='white')
axes[0, 0].set_title('书籍评分分布', fontsize=14)
axes[0, 0].set_xlabel('评分')
axes[0, 0].set_ylabel('书籍数量')

# ---------- 图2：价格与评分关系（回答：书越贵，评分越高吗？） ----------
axes[0, 1].scatter(df['price'], df['rating'], color='royalblue', alpha=0.6)
axes[0, 1].set_title('价格与评分的相关性', fontsize=14)
axes[0, 1].set_xlabel('价格 (元)')
axes[0, 1].set_ylabel('评分')

# ---------- 图3：价格分布（回答：书籍价格集中在什么区间？） ----------
axes[1, 0].hist(df['price'], bins=30, color='seagreen', edgecolor='white')
axes[1, 0].set_title('书籍价格分布', fontsize=14)
axes[1, 0].set_xlabel('价格 (元)')
axes[1, 0].set_ylabel('书籍数量')

# ---------- 图4：最贵的10本书（回答：哪些书最贵？） ----------
# 提取价格最高的前10条数据，并按价格从低到高排序（方便画图）
top10_expensive = df.nlargest(10, 'price').sort_values('price')

# 绘制水平柱状图，用书名作为Y轴，价格作为X轴
axes[1, 1].barh(top10_expensive['title'], top10_expensive['price'], color='coral')
axes[1, 1].set_title('最贵的Top 10书籍', fontsize=14)
axes[1, 1].set_xlabel('价格 (元)')
axes[1, 1].tick_params(axis='y', labelsize=8) # 设置Y轴字体大小，防止书名太长

plt.tight_layout() # 自动调整子图间距
plt.savefig('data/cleaned/raw/books_dashboard_v2.png', dpi=150, bbox_inches='tight')
plt.show()

print("图表已生成并保存！")
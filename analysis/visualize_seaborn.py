import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine

# ========== 1. 强制激活中文字体 ==========
# 核心：同时兼容 Windows 和 macOS 的常见中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans'] 
plt.rcParams['axes.unicode_minus'] = False

# 连接数据库
db_connection_str = 'mysql+pymysql://root:123456@localhost:3306/ecommerce_db?charset=utf8mb4'
engine = create_engine(db_connection_str)
query = "SELECT title, price, rating FROM books"
df = pd.read_sql(query, engine)

# ========== 2. 全局设置 Seaborn 主题 ==========
# 核心：设置全局主题，并直接将全局字体强制设为 "SimHei" (黑体)
sns.set_theme(style="whitegrid", font='SimHei') 

# ========== 3. 创建画布 ==========
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
# 注意：大标题的字体也要在这里强制指定
fig.suptitle('电商书籍数据分析看板 (Seaborn美化版)', fontsize=18, fontweight='bold', fontfamily='SimHei', y=0.98)

# ---------- 图1：评分分布 ----------
sns.histplot(df['rating'], bins=20, color='#8e44ad', kde=True, ax=axes[0, 0])
# 注意：子标题也要指定 fontfamily
axes[0, 0].set_title('书籍评分分布', fontfamily='SimHei')

# ---------- 图2：价格与评分关系 ----------
sns.scatterplot(x=df['price'], y=df['rating'], color='#3498db', ax=axes[0, 1])
axes[0, 1].set_title('价格与评分的相关性', fontfamily='SimHei')

# ---------- 图3：价格分布 ----------
sns.histplot(df['price'], bins=30, color='#2ecc71', kde=True, ax=axes[1, 0])
axes[1, 0].set_title('书籍价格分布', fontfamily='SimHei')

# ---------- 图4：最贵的Top 10书籍 ----------
top10_expensive = df.nlargest(10, 'price').sort_values('price')
sns.barplot(x='price', y='title', data=top10_expensive, palette='RdYlBu', ax=axes[1, 1])
axes[1, 1].set_title('最贵的Top 10书籍', fontfamily='SimHei')
axes[1, 1].tick_params(axis='y', labelsize=8)

# 自动调整子图间距
plt.tight_layout() 
plt.savefig('data/cleaned/raw/books_dashboard_seaborn_final.png', dpi=150, bbox_inches='tight')
plt.show()

print("图表已生成！")
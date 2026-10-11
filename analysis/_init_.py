import pandas as pd

# ==================== Step 1: 读取数据 ====================
df = pd.read_csv("data/cleaned/dataproducts_cleaned.csv")
print("=== 数据前5行 ===")
print(df.head())

# ==================== Step 2: 基本信息 ====================
print("\n=== 数据基本信息 ===")
print(df.info())
print("\n=== 描述性统计 ===")
print(df.describe())
print("\n=== 缺失值检查 ===")
print(df.isnull().sum())
print(f"\n数据维度: {df.shape}")

# ==================== Step 3: 基础业务指标 ====================
print("\n=== 基础业务指标 ===")
print(f"采集图书总数: {len(df)}")
print(f"平均价格: {df['price'].mean():.2f}")
print(f"价格中位数: {df['price'].median():.2f}")
print(f"价格标准差: {df['price'].std():.2f}")
print(f"最高价格: {df['price'].max()}, 最低价格: {df['price'].min()}")
print(f"平均评分: {df['rating'].mean():.2f}")
print(f"评分最高: {df.loc[df['rating'].idxmax(), 'title']} ({df['rating'].max()}分)")
print(f"评分最低: {df.loc[df['rating'].idxmin(), 'title']} ({df['rating'].min()}分)")

# ==================== Step 4: 条件筛选与排序 ====================
print("\n=== 条件筛选 ===")
print(f"价格<50的书: {len(df[df['price'] < 50])} 本")
print(f"评分>4.5的书: {len(df[df['rating'] > 4.5])} 本")

# 多条件筛选
target = df[(df["price"] >= 30) & (df["price"] <= 100) & (df["rating"] > 4.0)]
print(f"价格30-100且评分>4.0的书: {len(target)} 本")

# 排序
print("\n=== 价格Top3 ===")
print(df.sort_values("price", ascending=False).head(3))

# ==================== Step 5: 价格区间分组 ====================
print("\n=== 价格区间分组统计 ===")
df["price_range"] = pd.cut(
    df["price"],
    bins=[0, 30, 80, float('inf')],
    labels=["低价(0-30)", "中价(30-80)", "高价(80+)"],
    right=False
)

group_stats = df.groupby("price_range", observed=True).agg(
    书籍数量=("title", "count"),
    平均评分=("rating", "mean")
).reset_index()
print(group_stats)

# ==================== Step 6: 导出结果 ====================
group_stats.to_csv("data/cleaned/price_range_stats.csv", index=False, encoding="utf-8-sig")
print("\n分析结果已保存至 data/cleaned/price_range_stats.csv")
import os
import sys

# 确保能导入同级目录下的模块
sys.path.insert(0, '.')

# ================= 第1步：数据采集 =================
from crawler.spider import scrape_products

print("=" * 50)
print("电商数据采集分析系统 - 主流程启动")
print("=" * 50)

print("\n[1/5] 正在执行数据采集...")
raw_data = scrape_products(max_pages=3)
print(f"      采集完成，共 {len(raw_data)} 条原始数据")

# ================= 第2步：数据清洗 =================
print("\n[2/5] 正在执行数据清洗...")
from clean import clean_data

df = clean_data("data/raw/dataproducts.csv")

os.makedirs("data/cleaned", exist_ok=True)

df.to_csv(
    "data/cleaned/dataproducts_cleaned.csv",
    index=False,
    encoding="utf-8-sig"
)
print("      清洗完成，已保存至 data/cleaned/dataproducts_cleaned.csv")

# ================= 第3步：写入数据库 =================
print("\n[3/5] 正在写入数据库...")
import database.mysql
# database/mysql.py 是脚本式模块，import 后自动读取 CSV 并写入 MySQL

# ================= 第4步：数据分析 =================
print("\n[4/5] 正在执行数据分析...")
import analysis.read_db
# analysis/read_db.py 是脚本式模块，import 后自动执行分析逻辑

# ================= 第5步：数据可视化 =================
print("\n[5/5] 正在生成可视化图表...")
import analysis.visualize_seaborn
# analysis/visualize_seaborn.py 是脚本式模块，import 后自动画图

print("\n" + "=" * 50)
print("主流程执行完毕！")
print("=" * 50) 
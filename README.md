# 电商商品数据采集与分析系统

## 1. 项目简介

本项目是一个完整的电商商品数据采集与分析系统，覆盖了从数据采集、清洗、入库、分析到可视化的全链路流程。项目通过 Playwright 自动化采集公开网页上的商品信息，经过 Pandas 清洗后存入 MySQL 数据库，最终使用 SQL 和 Pandas 完成数据分析并生成可视化图表。

## 2. 项目目标

- 掌握 Python 爬虫技术（Playwright 浏览器自动化）
- 掌握数据处理全流程（采集 → 清洗 → 入库 → 分析 → 可视化）
- 掌握 MySQL 数据库的基本操作（建表、插入、查询）
- 掌握 Pandas 数据分析与 Matplotlib/Seaborn 可视化
- 掌握 Git/GitHub 版本管理与项目交付

## 3. 技术栈

| 技术 | 用途 |
|------|------|
| Python | 项目主语言、数据处理、流程控制 |
| Playwright | 浏览器自动化与网页数据采集 |
| CSV | 原始/中间数据保存 |
| Pandas | 数据清洗、统计、分析 |
| MySQL | 结构化数据存储与查询 |
| SQL | 统计、筛选、排序、分组、聚合 |
| Matplotlib / Seaborn | 生成分析图表与可视化 |
| Git / GitHub | 版本管理与项目展示 |

## 4. 项目结构

```
ecommerce-data-analysis/
├── .venv/                  # 虚拟环境目录
├── analysis/               # 数据分析与可视化模块
│   ├── __init__.py
│   ├── read_db.py          # [分析] 从数据库读取数据并进行统计
│   ├── visualize.py        # [可视化] 基础可视化脚本
│   └── visualize_seaborn.py# [可视化] Seaborn 高级图表生成
├── crawler/                # 数据采集模块
│   ├── __pycache__/
│   ├── __init__.py
│   ├── spider.py           # [爬虫] Playwright 自动化采集脚本
│   └── spider(first).py    # [爬虫] 早期测试版本爬虫
├── data/                   # 📁 数据存储中心 (核心)
│   ├── cleaned/            # ✅ 清洗后的数据 & 分析报告
│   │   ├── raw/            # ⚠️ 注意：这里存放了生成的图片和部分CSV
│   │   │   ├── all_books.csv
│   │   │   ├── rating_5_books.csv
│   │   │   ├── books_dashboard_seaborn.png  # (生成的图表)
│   │   │   └── books_dashboard_v2.png       # (生成的图表)
│   │   └── dataproducts_cleaned.csv         # [核心] 清洗后的标准数据集
│   └── raw/                # 📥 原始采集数据
│       └── dataproducts.csv                 # [核心] 爬虫抓取的原始数据
├── database/               # 数据库模块
│   └── mysql.py            # [入库] 将 CSV 写入 MySQL 数据库
├── reports/                # 项目报告/文档目录
├── .gitignore              # Git 忽略配置
├── clean.py                # [清洗] 数据预处理脚本 (Pandas)
├── main.py                 # 🚀 主程序入口 (串联全流程)
├── README.md               # 项目说明文档
└── requirements.txt        # 依赖库列表
## 6. 数据清洗

数据清洗模块 `clean.py` 使用 Pandas 完成以下清洗规则：

1. **删除无用列**：移除 url 字段（不适合数值分析）
2. **缺失值处理**：检查并删除包含缺失值的记录
3. **重复值处理**：检测并删除重复记录
4. **价格格式转换**：去除英镑符号"£"，将字符串转换为浮点数值
5. **输出清洗后数据**：保存至 `data/cleaned/dataproducts_cleaned.csv`

保留原始 CSV 和清洗后 CSV 两份数据，方便排查问题。

## 7. MySQL 数据库设计

数据库名为 `ecommerce_db`，核心表结构如下：

```sql
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2),
    rating FLOAT,
    url TEXT
);
```

入库模块 `database/mysql.py` 使用 SQLAlchemy 连接 MySQL，通过 Pandas 的 `to_sql` 方法将清洗后的 CSV 数据批量写入数据库。

## 8. SQL 分析

通过 SQL 可完成以下分析查询：

- **商品总数**：`SELECT COUNT(*) FROM books;`
- **平均价格**：`SELECT AVG(price) FROM books;`
- **价格最高的商品**：`SELECT * FROM books ORDER BY price DESC LIMIT 10;`
- **分类商品数量统计**：`SELECT category, COUNT(*) AS count FROM books GROUP BY category ORDER BY count DESC;`
- **分类平均价格**：`SELECT category, AVG(price) AS avg_price FROM books GROUP BY category ORDER BY avg_price DESC;`
- **价格筛选**：`SELECT * FROM books WHERE price > 100 ORDER BY price DESC;`

Pandas 通过 `pd.read_sql` 读取数据库查询结果，完成进一步的数据处理和分析。

## 9. 可视化结果

可视化模块 `analysis/visualize_seaborn.py` 使用 Matplotlib 和 Seaborn 生成以下图表（保存至 `reports/` 目录）：

- **分类商品数量分布图**：展示各分类下商品数量的差异
- **分类平均价格对比图**：展示不同分类商品的平均价格水平
- **价格分布直方图**：展示商品价格的分布情况
- **价格与评分关系散点图**：分析价格与评分之间的相关性

## 10. 项目运行方法

### 环境准备

```bash
# 1. 创建虚拟环境
python -m venv .venv
# Windows 激活
.venv\Scripts\Activate.ps1
# macOS/Linux 激活
source .venv/bin/activate

# 2. 安装依赖
pip install playwright pandas matplotlib seaborn pymysql sqlalchemy

# 3. 安装 Playwright 浏览器
playwright install
```

### 运行主流程

```bash
# 确保 MySQL 服务已启动，且数据库 ecommerce_db 已创建
# 修改 database/mysql.py 中的数据库密码为本地实际密码

python main.py
```

主流程依次执行：数据采集 → 数据清洗 → 数据库入库 → 数据分析 → 可视化图表生成。

## 11. 项目难点与解决方法

1. **Playwright 元素定位**：不同网页的 DOM 结构不同，需要通过浏览器开发者工具（F12）检查元素的 class、id、CSS Selector 或 XPath 来精确定位目标数据。

2. **数据格式清洗**：网页采集的价格数据通常包含货币符号（如"£"）、千分位逗号等字符，需要通过字符串替换和类型转换才能变为可用的数值类型。

3. **模块间数据传递**：各模块（采集、清洗、入库、分析、可视化）独立编写，通过 CSV 文件和数据库作为数据中转站，实现了模块间的解耦。

4. **数据库连接配置**：使用 SQLAlchemy 统一数据库连接接口，通过 `create_engine` 创建引擎，配合 `to_sql` 方法简化数据写入流程。

## 12. 项目不足

1. 数据采集量较小（第一版仅采集少量页面），可后续增加翻页逻辑采集更多数据
2. 未实现异常重试机制，网络波动时采集可能中断
3. 数据库密码硬编码在代码中，应改用环境变量或 .env 文件管理敏感信息
4. 缺少单元测试，各模块的健壮性有待提升
5. 可视化图表数量和类型较为基础，可丰富图表维度

## 13. 后续计划

- **V2**：增加采集页面数量，扩展商品字段（库存、评论数、分类等）
- **V3**：加入定时采集任务（如 APScheduler），实现定期自动更新数据
- **V4**：学习 FastAPI，将数据查询和统计结果封装为 RESTful API
- **V5**：学习 Vue/前端框架，搭建网页数据分析展示平台
- **V6**：引入 AI 能力，实现数据自动解读与智能推荐
import pandas as pd
import pymysql
from sqlalchemy import create_engine

# 1. 读取 CSV
csv_path = "data/cleaned/dataproducts_cleaned.csv"
df = pd.read_csv(csv_path)

# 2. 连接 MySQL
db_connection_str = 'mysql+pymysql://root:123456@localhost:3306/ecommerce_db?charset=utf8mb4'
db_connection = create_engine(db_connection_str)

# 3. 写入数据库
try:
    df.to_sql('books', con=db_connection, if_exists='append', index=False)
    print("✅ 成功导入 {} 条数据到 MySQL 的 books 表中！".format(len(df)))
except Exception as e:
    print("❌ 导入失败，错误信息：", e)
finally:
    db_connection.dispose()
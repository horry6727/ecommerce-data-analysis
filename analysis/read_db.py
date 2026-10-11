import pandas as pd
from sqlalchemy import create_engine

# 1. 连接数据库
db_connection_str = 'mysql+pymysql://root:123456@localhost:3306/ecommerce_db?charset=utf8mb4'
engine = create_engine(db_connection_str)

# 2. 查询评分为5.0的书并保存
query = "SELECT title, price, rating FROM books WHERE rating = 5.0"
df = pd.read_sql(query, engine)
df.to_csv('data/cleaned/raw/rating_5_books.csv', index=False)
print("评分为5.0的书已保存到 data/cleaned/raw/rating_5_books.csv")

# 3. 读取所有书并保存
query2 = "SELECT title, price, rating FROM books"
df2 = pd.read_sql(query2, engine)
df2.to_csv('data/cleaned/raw/all_books.csv', index=False)
print("所有书籍数据已保存到 data/cleaned/raw/all_books.csv")
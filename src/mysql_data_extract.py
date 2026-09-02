import pymysql
import pandas as pd
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))# 获取项目根目录：__file__为当前py文件路径

# --连接本地MySQL 
# 远程部署时替换host为服务器IP；密码改为安装MySQL时设置的真实密码
conn = pymysql.connect(
    host="127.0.0.1",          # 本地数据库地址
    user="root",               # MySQL用户名
    password="此处填写用户密码",   # MySQL登录密码，连接报错优先核对
    database="credit_risk_db", # 数据所在库名
    charset="utf8mb4"          # 统一字符集防乱码
)
# --全维度多表联合查询SQL
sql ="""
SELECT
    pi.age, pi.income, pi.home_ownership, pi.emp_length, pi.default_on_file, pi.cred_hist_length,
    lr.loan_grade, lr.loan_intent, lr.loan_amnt, lr.loan_int_rate, lr.loan_percent_income,
    ol.loan_status, ol.overdue_times
FROM person_info pi
JOIN loan_record lr ON pi.person_id = lr.person_id
JOIN overdue_label ol ON pi.person_id = ol.person_id
"""
# pd.read_sql执行SQL并自动转DataFrame
df_raw = pd.read_sql(sql, conn)
# 释放连接资源
conn.close()
print(df_raw)
# 导出本地csv
# 后续清洗、绘图直接读csv，避免重复查询数据库
raw_out = os.path.join(BASE_DIR, "data", "mysql_extract_data.csv")
df_raw.to_csv(raw_out, index=False)#输出csv
print("MySQL取数完成，数据集行数：", df_raw.shape[0])
print("字段列表：", list(df_raw.columns))
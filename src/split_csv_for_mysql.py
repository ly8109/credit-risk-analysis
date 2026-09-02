# 导入pandas库，负责读取原始数据集、拆分多张子业务表
import pandas as pd
import os
# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 读取Kaggle信贷原始宽表，所有客户、贷款、逾期数据都在这张表中
csv_path = os.path.join(BASE_DIR, "data", "credit_risk_dataset.csv")
df = pd.read_csv(csv_path)
# -- 拆分客户基础信息表
#静态客户资质字段：年龄、年收入、房屋所有权、工作年限、历史违约、信用记录长度
df["person_id"] = range(1, len(df)+1)#设置id列方便查询
df_person = df[["person_id","person_age", "person_income", "person_home_ownership",
                "person_emp_length", "cb_person_default_on_file","cb_person_cred_hist_length"]].copy()
# -- 重命名为数据库表字段名（与SQL表结构一致）
df_person.rename(columns={
    "person_income": "income",
    "person_emp_length": "emp_length",
    "person_home_ownership": "home_ownership",
    "person_age": "age",
    "cb_person_default_on_file": "default_on_file",
    "cb_person_cred_hist_length": "cred_hist_length",
}, inplace=True)

# --拆分借贷产品信息表
# 每笔贷款的产品属性：id,等级、意图、金额、利率、贷款收入占比
df_loan = df[["person_id","loan_grade", "loan_intent", "loan_amnt",
              "loan_int_rate", "loan_percent_income"]].copy()

# -- 拆分逾期标签表 
# 提取核心好坏客户标签：loan_status 0=正常还款 1=逾期
df_overdue = df[["person_id","loan_status"]].copy().reset_index(drop=True)
# 简易模拟历史逾期次数：逾期客户记1次，正常客户0次，弥补数据集无历史逾期字段缺陷
df_overdue["overdue_times"] = df_overdue["loan_status"]

# --导出拆分后的CSV文件 

person_path = os.path.join(BASE_DIR, "data", "person_info.csv")
loan_path = os.path.join(BASE_DIR, "data", "loan_record.csv")
overdue_path = os.path.join(BASE_DIR, "data", "overdue_label.csv")
# index=False：不导出pandas自动生成的行索引，防止导入MySQL多出一列无效数据
df_person.to_csv(person_path, index=False)
df_loan.to_csv(loan_path, index=False)
df_overdue.to_csv(overdue_path, index=False)
#导入库
import pandas as pd
import numpy as np
import os
# --1.读取数据
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(BASE_DIR, "data", "mysql_extract_data.csv")# 自动拼接路径
df = pd.read_csv(csv_path)
print("原始数据行数：", df.shape[0])

# --2.缺失值处理

# 年收入、工作年限、利率、信用历史长度：连续数值缺失用中位数填充，中位数不受极端值干扰
for col in ["income", "emp_length", "loan_int_rate", "cred_hist_length"]:#循环遍历
    df[col] = df[col].fillna(df[col].median())
# 贷款等级、贷款意图等分类字段缺失：用众数（出现频率最高值）填充
for col in ["loan_grade", "loan_intent", "home_ownership", "default_on_file"]:
    df[col] = df[col].fillna(df[col].mode()[0])
# 年龄、贷款金额是风控核心准入字段，缺失则样本失去分析价值，直接删除
df = df.dropna(subset=["age", "loan_amnt", "loan_percent_income"])#默认存在缺失则删除整行
print("缺失值处理后行数：", df.shape[0])

# --3.  3σ异常值过滤  统计3σ原则：超出 均值±3倍标准差 视为业务异常值
def filter_3sigma(series): #自定义函数 series传入字段名
    mean, std = np.mean(series), np.std(series)
    lower, upper = mean - 3 * std, mean + 3 * std
    return series.between(lower, upper) #返回字段数据在最低最高值之间的数据

# 年龄异常（如 >100岁）、收入异常高、贷款金额异常，属于数据录入错误
mask_age = filter_3sigma(df["age"])
mask_income = filter_3sigma(df["income"])
mask_loan = filter_3sigma(df["loan_amnt"])
df = df[mask_age & mask_income & mask_loan].copy()#三行同时正常则输出这一行，否则删除
print("3σ异常过滤后行数：", df.shape[0])

# --4.风控特征工程梳理 
# 原始数据集已提供 loan_percent_income（债务收入占比dti）= 贷款金额/年收入，
df["dti"] = df["loan_percent_income"]

# --客户分层特征工程 

#  4.1基于DTI债务收入比的风险分层
bins = [0, 0.3, 0.5, 999]           # 0~0.3低负债，0.3~0.5中等，>0.5高负债
labels = ["低风险", "中风险", "高风险"]
df["risk_level"] = pd.cut(df["dti"], bins=bins, labels=labels)

#  4.2基于工作年限的就业稳定性分层
def emp_level(x):
    if x < 2:
        return "短期就业(<2年)"
    elif x <= 10:
        return "中期就业(2-10年)"
    else:
        return "长期稳定(>10年)"
df["emp_stability"] = df["emp_length"].apply(emp_level)

#  4.3基于信用记录长度的信用历史分层
def cred_level(x):
    if x < 3:
        return "短信用历史(<3年)"
    elif x <= 10:
        return "中信用历史(3-10年)"
    else:
        return "长信用历史(>10年)"
df["cred_history"] = df["cred_hist_length"].apply(cred_level)

# --5.分组聚合指标
# 按贷款等级聚合：各等级违约率
group_grade = df.groupby("loan_grade")["loan_status"].agg(["mean", "count"]).reset_index()
# 按历史违约聚合：历史违约与否的坏账率
group_default = df.groupby("default_on_file")["loan_status"].mean().reset_index()
# 按就业稳定性聚合
group_emp = df.groupby("emp_stability")["loan_status"].mean().reset_index()
# 按信用历史分层聚合
group_cred = df.groupby("cred_history")["loan_status"].mean().reset_index()

# --6.输出清洗后标准数据集
out_csv = os.path.join(BASE_DIR, "data", "clean_risk_data.csv")
df.to_csv(out_csv, index=False)
print("数据清洗完成,输出 clean_risk_data.csv，样本量：", df.shape[0])

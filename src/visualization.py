#导入库
import pandas as pd
import matplotlib.pyplot as plt
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))#获取根目录

# 自动创建图表输出目录
CHART_FOLDER = os.path.join(BASE_DIR, "charts")
os.makedirs(CHART_FOLDER, exist_ok=True)

# 设置中文字体，解决中文乱码
plt.rcParams["font.sans-serif"] = ["SimHei"]
# 修复负号显示
plt.rcParams["axes.unicode_minus"] = False

# 读取清洗后标准数据集
clean_data_path = os.path.join(BASE_DIR, "data", "clean_risk_data.csv")
df = pd.read_csv(clean_data_path)

# --图1：不同风险等级逾期率（柱状图）
plt.figure(figsize=(8,5))
risk_overdue = df.groupby("risk_level")["loan_status"].mean()
plt.bar(risk_overdue.index,risk_overdue.values,color=["blue","red","pink"])
plt.title("不同风险等级客户逾期率对比")
plt.xlabel("风险等级")
plt.ylabel("逾期率")
for i, v in enumerate(risk_overdue.values):
    plt.text(i, v, f"{v:.2%}", ha="center", va="bottom")
plt.tight_layout()
chart_path = os.path.join(BASE_DIR, "charts", "1_risk_overdue_bar.png")
plt.savefig(chart_path, dpi=150, bbox_inches="tight")
plt.close()
plt.show()
# --图2：贷款等级与逾期率（柱状图）

plt.figure(figsize=(9, 5))
grade_overdue = df.groupby("loan_grade")["loan_status"].mean().sort_index()
plt.bar(grade_overdue.index, grade_overdue.values, color="#3498db")
plt.title("贷款等级(loan_grade)与逾期率")
plt.xlabel("贷款等级 A~G")
plt.ylabel("逾期率")
for i, v in enumerate(grade_overdue.values):
    plt.text(i, v, f"{v:.2%}", ha="center", va="bottom")
plt.tight_layout()
chart_path = os.path.join(BASE_DIR, "charts", "2_loan_grade_bar.png")
plt.savefig(chart_path, dpi=150, bbox_inches="tight")
plt.close()

#--图3：历史违约与否坏账率（对比柱状图）
plt.figure(figsize=(7, 5))
default_overdue = df.groupby("default_on_file")["loan_status"].mean().reindex(["N", "Y"])
plt.bar(default_overdue.index, default_overdue.values,
        color=["#27ae60", "#e74c3c"])
plt.title("历史违约记录与坏账率")
plt.xlabel("历史违约 (N=无违约, Y=曾违约)")
plt.ylabel("坏账率")
for i, v in enumerate(default_overdue.values):
    plt.text(i, v, f"{v:.2%}", ha="center", va="bottom")
plt.tight_layout()
chart_path = os.path.join(BASE_DIR, "charts", "3_default_on_file_bar.png")
plt.savefig(chart_path, dpi=150, bbox_inches="tight")
plt.close()

# --图4：就业稳定性与坏账率
plt.figure(figsize=(9, 5))
emp_bad = df.groupby("emp_stability", observed=True)["loan_status"].mean()
emp_bad = emp_bad.reindex(["短期就业(<2年)", "中期就业(2-10年)", "长期稳定(>10年)"])
plt.bar(emp_bad.index, emp_bad.values, color=["#e67e22", "#9b59b6", "#27ae60"])
plt.title("工作年限分层与坏账率")
plt.xlabel("就业稳定性分层")
plt.ylabel("坏账率")
for i, v in enumerate(emp_bad.values):
    plt.text(i, v, f"{v:.2%}", ha="center", va="bottom")
plt.tight_layout()
chart_path = os.path.join(BASE_DIR, "charts", "4_emp_stability_bar.png")
plt.savefig(chart_path, dpi=150, bbox_inches="tight")
plt.close()

# --图5：信用历史分层与坏账率（柱状图）
plt.figure(figsize=(9, 5))
cred_bad = df.groupby("cred_history", observed=True)["loan_status"].mean()
cred_bad = cred_bad.reindex(["短信用历史(<3年)", "中信用历史(3-10年)", "长信用历史(>10年)"])
plt.bar(cred_bad.index, cred_bad.values, color=["#e74c3c", "#f2b851", "#61b863"])
plt.title("信用记录长度分层与坏账率")
plt.xlabel("信用历史分层")
plt.ylabel("坏账率")
for i, v in enumerate(cred_bad.values):
    plt.text(i, v, f"{v:.2%}", ha="center", va="bottom")
plt.tight_layout()
chart_path = os.path.join(BASE_DIR, "charts", "5_cred_history_bar.png")
plt.savefig(chart_path, dpi=150, bbox_inches="tight")
plt.close()

# 图6：DTI债务收入比分布（直方图）
plt.figure(figsize=(8, 5))
plt.hist(df["dti"], bins=30, alpha=0.7, color="#2c3e50")
plt.title("客户债务收入比DTI分布")
plt.xlabel("DTI（loan_percent_income）")
plt.ylabel("频数")
plt.tight_layout()
chart_path = os.path.join(BASE_DIR, "charts", "6_dti_hist.png")
plt.savefig(chart_path, dpi=150, bbox_inches="tight")
plt.close()

# --图7：客户风险分层占比（饼图）
plt.figure(figsize=(7, 7))
risk_cnt = df["risk_level"].value_counts().reindex(["低风险", "中风险", "高风险"])
plt.pie(risk_cnt.values, labels=risk_cnt.index, autopct="%1.1f%%",
        colors=["#61b863", "#f2b851", "#e64c3c"], startangle=90)
plt.title("客户风险分层占比")
plt.tight_layout()
chart_path = os.path.join(BASE_DIR, "charts", "7_risk_pie.png")
plt.savefig(chart_path, dpi=150, bbox_inches="tight")
plt.close()

print("全部绘图完成，共7张图保存至charts文件夹")
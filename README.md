# 信贷客户风险数据分析项目（Credit Risk Dataset）

## 一、项目简介

复刻银行/消费金融公司风控分析师完整工作链路：基于 Kaggle **Credit Risk Dataset**（公开信贷数据集），完成 MySQL 分层建表 ETL、数据库自动化取数、数据清洗与风控特征衍生、可视化风险洞察、输出可落地的信贷分层准入策略，覆盖风控核心技术与业务流程。



## 二、数据集字段清单（共 12 个字段）

|字段名|中文含义|类型|
|-|-|-|
|person\_age|借款人年龄|数值型|
|person\_income|借款人年收入|数值型|
|person\_home\_ownership|房屋所有权（RENT/OWN/MORTGAGE/OTHER）|分类型|
|person\_emp\_length|工作年限（年）|数值型|
|loan\_intent|贷款意图（PERSONAL/EDUCATION/MEDICAL等）|分类型|
|loan\_grade|贷款等级（A\~G，A最优）|分类型|
|loan\_amnt|贷款金额|数值型|
|loan\_int\_rate|贷款年化利率|数值型|
|loan\_status|贷款状态（0=非违约，1=违约，标签列）|二分类|
|loan\_percent\_income|收入占比 = 贷款金额/年收入（即DTI）|数值型|
|cb\_person\_default\_on\_file|历史违约记录（Y=曾违约，N=无）|分类型|
|cb\_person\_cred\_hist\_length|信用记录长度（年）|数值型|

## 三、技术栈

MySQL、Python（Pandas / NumPy / Matplotlib）、pymysql

## 四、项目完整流程

1. **MySQL 建表**：按第三范式设计3 张业务表（person\_info 客户基础表 / loan\_record 贷款记录表  / overdue\_label 逾期标签表），主键+外键保证数据一致性；编写多表 JOIN、分层聚合 SQL 实现业务报表取数。
2. **Python 取数**：pymysql 自动连接 MySQL，执行全维度联查拉取完整样本，导出本地csv。
3. **数据清洗与特征工程**：中位数/众数缺失值填充、3σ 统计规则异常过滤；直接采用 loan\_percent\_income 作为 DTI；按贷款等级、工作年限、信用历史长度、DTI 阈值四方面分层。
4. **可视化洞察**：7 张风控图表输出至 charts/，直观对比年龄、贷款等级、历史违约、就业稳定性、信用历史、负债水平客群风险差异。
5. **量化统计与落地**：输出客户风险分层明细表，提炼可落地的信贷准入规则，完成"数据计算→业务落地"闭环。

## 五、核心数据发现

1. 贷款等级越低（G 级），违约率越高，等级可作为准入与定价的核心依据；
2. 历史有违约记录（Y）客群坏账率显著高于无违约客群，应收紧再贷审批；
3. 工作年限越短、信用历史越短，坏账率越高，"信用空窗期"客群是重点风控对象；
4. 30 岁以下且 DTI>0.5 的年轻高负债客群逾期率显著高于全量基准，可作为贷前拦截规则。

## 六、仓库文件说明

|文件|说明|
|-|-|
|credit\_risk\_dataset.csv|Kaggle 原始宽表（自行下载放入本目录）|
|split\_csv\_for\_mysql.py|原始宽表按三范式拆分为 3 张子表 CSV|
|analysis.sql|MySQL 建表语句 + 5 条业务分层统计查询|
|mysql\_data\_extract.py|Python 连接数据库自动化提取全量业务数据|
|data\_process.py|数据清洗、异常过滤、风控特征衍生、客户分层|
|visualization.py|风控可视化绘图，图表统一输出 charts/|
|result\_summary.py|业务结论统计 + 风险分层明细导出|
|charts/|全部分析可视化图表|
|risk\_strategy\_result.csv|客户风险分层业务交付明细表|

## 七、运行步骤

\# 1. 安装依赖
pip install pandas numpy matplotlib pymysql

# 2\. 拆分数据（需先把 credit\\\_risk\\\_dataset.csv 放入本目录）

python split\\\_csv\\\_for\\\_mysql.py

# 3\. 在 MySQL 中执行 analysis.sql 建表，并导入 person\\\_info/loan\\\_record/overdue\\\_label 三张CSV



# 4\. python连接mysql取数

mysql\\\_data\\\_extract.py

# 5\. 清洗+特征工程

data\\\_process.py

# 6\. 可视化

python visualization.py

# 7\. 业务统计与明细导出

&#x20;result\\\_summary.py


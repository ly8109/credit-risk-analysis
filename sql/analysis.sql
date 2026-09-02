-- 创建数据库
CREATE DATABASE credit_risk_db CHARSET utf8mb4;
USE credit_risk_db;
-- 表1：客户基础信息表 person_info
-- 客户信息字段
CREATE TABLE person_info (
    person_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '客户唯一自增主键',
    age INT COMMENT '借款人年龄（person_age）',
    income DECIMAL(12,2) COMMENT '借款人年收入（person_income）',
    home_ownership VARCHAR(10) COMMENT '房屋所有权：RENT租赁/OWN自有/MORTGAGE按揭/OTHER其他',
    emp_length FLOAT COMMENT '工作年限（person_emp_length）',
    default_on_file CHAR(1) COMMENT '历史违约记录（cb_person_default_on_file）：Y已违约/N无违约',
    cred_hist_length INT COMMENT '信用记录长度年数（cb_person_cred_hist_length）'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='客户基础信息表';

-- 表2：借贷记录表 loan_record 
-- 每笔贷款的产品维度信息
CREATE TABLE loan_record (
    loan_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '单笔贷款唯一自增主键',
    person_id INT COMMENT '关联客户主键',
    loan_grade CHAR(1) COMMENT '贷款等级（loan_grade）：A~G，A最优G最差',
    loan_intent VARCHAR(20) COMMENT '贷款意图（loan_intent）：PERSONAL/EDUCATION/MEDICAL等',
    loan_amnt DECIMAL(12,2) COMMENT '贷款申请金额（loan_amnt）',
    loan_int_rate FLOAT COMMENT '贷款年化利率（loan_int_rate）',
    loan_percent_income FLOAT COMMENT '贷款收入比（loan_percent_income）= 贷款金额/年收入，即债务收入比DTI',
    FOREIGN KEY (person_id) REFERENCES person_info(person_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='借贷记录表';

-- 表3：逾期标签表 overdue_label 
-- 风控建模核心标签：loan_status 0=非违约 1=违约
CREATE TABLE overdue_label (
    label_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '标签记录自增主键',
    person_id INT COMMENT '关联客户唯一ID',
    loan_status TINYINT COMMENT '贷款状态（loan_status）：0=非违约 1=违约',
    overdue_times INT DEFAULT 0 COMMENT '历史累计逾期次数（模拟字段）',
    FOREIGN KEY (person_id) REFERENCES person_info(person_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='逾期标签表';


-- 业务查询1：全维度联查 多表联合查询
SELECT
    pi.person_id,pi.age, pi.income, pi.home_ownership, pi.emp_length, pi.default_on_file, pi.cred_hist_length,
    lr.loan_grade, lr.loan_intent, lr.loan_amnt, lr.loan_int_rate, lr.loan_percent_income,
    ol.loan_status
FROM person_info pi
JOIN loan_record lr ON pi.person_id = lr.person_id
JOIN overdue_label ol ON pi.person_id = ol.person_id;

-- 查询2：分贷款等级统计逾期率
-- 信用等级A~G与违约率关系，评估产品定价与准入依据
SELECT
    lr.loan_grade,
    COUNT(*) AS total_cnt,                 -- 该等级样本量
    SUM(ol.loan_status) AS overdue_cnt,    -- 该等级违约人数
    ROUND(SUM(ol.loan_status)/COUNT(*), 3) AS overdue_rate  -- 违约率
FROM loan_record lr
JOIN overdue_label ol ON lr.person_id = ol.person_id
GROUP BY lr.loan_grade
ORDER BY lr.loan_grade;

-- 查询3：按历史违约记录对比坏账率 
-- 历史曾违约客户与新客户风险差异，是否应收紧再贷政策
SELECT
    pi.default_on_file,
    COUNT(*) AS total_cnt,
    ROUND(AVG(ol.loan_status), 3) AS bad_debt_rate   -- 平均坏账率
FROM person_info pi
JOIN overdue_label ol ON pi.person_id = ol.person_id
GROUP BY pi.default_on_file;

-- 查询4：按工作年限分层统计坏账率
SELECT
    CASE
        WHEN pi.emp_length < 2 THEN '短期就业(<2年)'
        WHEN pi.emp_length BETWEEN 2 AND 10 THEN '中期就业(2-10年)'
        ELSE '长期稳定(>10年)'
    END AS emp_group,
    COUNT(*) AS total_cnt,
    ROUND(AVG(ol.loan_status), 3) AS bad_debt_rate
FROM person_info pi
JOIN overdue_label ol ON pi.person_id = ol.person_id
GROUP BY emp_group;

-- 查询5：按信用记录长度分层统计坏账率 
SELECT
    CASE
        WHEN pi.cred_hist_length < 3 THEN '短信用历史(<3年)'
        WHEN pi.cred_hist_length BETWEEN 3 AND 10 THEN '中信用历史(3-10年)'
        ELSE '长信用历史(>10年)'
    END AS cred_group,
    COUNT(*) AS total_cnt,
    ROUND(AVG(ol.loan_status), 3) AS bad_debt_rate
FROM person_info pi
JOIN overdue_label ol ON pi.person_id = ol.person_id
GROUP BY cred_group;
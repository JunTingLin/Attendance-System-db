import os
import random
from datetime import datetime, timedelta
import string
from faker import Faker

# 初始化 Faker，設定為台灣繁體中文
fake = Faker('zh_TW')

# ==================== 輔助函數 ====================

# 確保目標目錄存在
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# 生成SQL檔案函數
def write_sql_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

# 生成密碼
def generate_password():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

# 根據服務月數計算特休假時數的函數
def calculate_annual_leave_hours(months_of_service):
    for rule in annual_leave_rules:
        if rule['min_months'] <= months_of_service and (rule['max_months'] is None or months_of_service < rule['max_months']):
            return rule['hours']
    return 0  # 預設值，正常不會執行到這裡

# ==================== 初始化設定 ====================

# 創建目錄
ensure_dir('company_data_sql')

# ==================== 基礎資料定義 ====================

# 建立特休假規則對照表
annual_leave_rules = [
    {'min_months': 0, 'max_months': 6, 'hours': 0},           # 未滿半年：無特休
    {'min_months': 6, 'max_months': 12, 'hours': 24},         # 半年以上未滿一年：3天 (24小時)
    {'min_months': 12, 'max_months': 24, 'hours': 56},        # 一年以上未滿兩年：7天 (56小時)
    {'min_months': 24, 'max_months': 36, 'hours': 80},        # 兩年以上未滿三年：10天 (80小時)
    {'min_months': 36, 'max_months': 60, 'hours': 112},       # 三年以上未滿五年：14天 (112小時)
    {'min_months': 60, 'max_months': 120, 'hours': 120},      # 五年以上未滿十年：15天 (120小時)
    {'min_months': 120, 'max_months': 240, 'hours': 160},     # 十年以上未滿二十年：20天 (160小時)
    {'min_months': 240, 'max_months': None, 'hours': 192},    # 二十年以上：24天 (192小時)
]

# 定義部門階層關係和職位對應
department_hierarchy = {
    # 格式: department_id: {parent_id, [child_ids]}
    1: {'parent': None, 'children': [2, 6]},  # 營運組織
    2: {'parent': 1, 'children': [3, 4, 5]},  # 晶圓廠營運處
    3: {'parent': 2, 'children': []},         # 晶圓一廠
    4: {'parent': 2, 'children': []},         # 晶圓二廠
    5: {'parent': 2, 'children': []},         # 晶圓三廠
    6: {'parent': 1, 'children': [7, 8]},     # 製程整合處
    7: {'parent': 6, 'children': []},         # 製程整合一科
    8: {'parent': 6, 'children': []},         # 製程整合二科
    
    9: {'parent': None, 'children': [10, 13]},  # 研發組織
    10: {'parent': 9, 'children': [11, 12]},    # 先進製程研發處
    11: {'parent': 10, 'children': []},         # 先進製程研發一科
    12: {'parent': 10, 'children': []},         # 先進製程研發二科
    13: {'parent': 9, 'children': [14, 15]},    # 元件研發處
    14: {'parent': 13, 'children': []},         # 元件研發一科
    15: {'parent': 13, 'children': []},         # 元件研發二科
    
    16: {'parent': None, 'children': [17, 20]},  # 業務組織
    17: {'parent': 16, 'children': [18, 19]},    # 客戶服務處
    18: {'parent': 17, 'children': []},          # 客戶服務一科
    19: {'parent': 17, 'children': []},          # 客戶服務二科
    20: {'parent': 16, 'children': [21, 22]},    # 業務發展處
    21: {'parent': 20, 'children': []},          # 業務發展一科
    22: {'parent': 20, 'children': []},          # 業務發展二科
    
    23: {'parent': None, 'children': [24, 27, 30]},  # 行政組織
    24: {'parent': 23, 'children': [25, 26]},        # 人力資源處
    25: {'parent': 24, 'children': []},              # 人資規劃科
    26: {'parent': 24, 'children': []},              # 人才發展科
    27: {'parent': 23, 'children': [28, 29]},        # 財務處
    28: {'parent': 27, 'children': []},              # 會計科
    29: {'parent': 27, 'children': []},              # 財務規劃科
    30: {'parent': 23, 'children': [31, 32]},        # 法務處
    31: {'parent': 30, 'children': []},              # 法務一科
    32: {'parent': 30, 'children': []},              # 法務二科
    
    33: {'parent': None, 'children': [34, 37]},      # 資訊技術組織
    34: {'parent': 33, 'children': [35, 36, 37]},    # 資訊系統處
    35: {'parent': 34, 'children': []},              # 企業系統科
    36: {'parent': 34, 'children': []},              # 製造系統科
    37: {'parent': 34, 'children': []},              # 資訊安全科
    38: {'parent': 33, 'children': [39, 40]},        # 基礎設施處
    39: {'parent': 38, 'children': []},              # 網路管理科
    40: {'parent': 38, 'children': []}               # 伺服器管理科
}

# 建立部門類別映射，方便後續使用
department_categories = {
    'operations': [1, 2, 3, 4, 5, 6, 7, 8],                  # 營運組織及下屬部門
    'research': [9, 10, 11, 12, 13, 14, 15],                 # 研發組織及下屬部門
    'business': [16, 17, 18, 19, 20, 21, 22],                # 業務組織及下屬部門
    'administration': [23, 24, 25, 26, 27, 28, 29, 30, 31, 32], # 行政組織及下屬部門
    'it': [33, 34, 35, 36, 37, 38, 39, 40]                   # 資訊技術組織及下屬部門
}

# 建立部門層級映射
department_levels = {
    'organization': [1, 9, 16, 23, 33],                      # 組織層級
    'division': [2, 6, 10, 13, 17, 20, 24, 27, 30, 34, 38],  # 處級
    'section': [3, 4, 5, 7, 8, 11, 12, 14, 15, 18, 19, 21, 22, 25, 26, 28, 29, 31, 32, 35, 36, 37, 39, 40] # 科級
}

# 建立部門代碼映射
department_codes = {
    1: 'OP000', 2: 'OP100', 3: 'OP110', 4: 'OP120', 5: 'OP130', 6: 'OP200', 7: 'OP210', 8: 'OP220',
    9: 'RD000', 10: 'RD100', 11: 'RD110', 12: 'RD120', 13: 'RD200', 14: 'RD210', 15: 'RD220',
    16: 'SA000', 17: 'SA100', 18: 'SA110', 19: 'SA120', 20: 'SA200', 21: 'SA210', 22: 'SA220',
    23: 'AD000', 24: 'AD100', 25: 'AD110', 26: 'AD120', 27: 'AD200', 28: 'AD210', 29: 'AD220',
    30: 'AD300', 31: 'AD310', 32: 'AD320',
    33: 'IT000', 34: 'IT100', 35: 'IT110', 36: 'IT120', 37: 'IT130', 38: 'IT200', 39: 'IT210', 40: 'IT220'
}

# 建立部門層級與對應職位的映射
level_position_mapping = {
    'organization': 4,  # 組織層級 - 組織長
    'division': 6,      # 處級 - 處長
    'section': 9        # 科級 - 科長
}

# 建立職位類別映射，方便後續使用
position_categories = {
    'engineer': [12, 13, 14, 15, 16],  # 工程師職級
    'technician': [17, 18, 19],        # 技術人員職級
    'admin': [20, 21, 22, 23],         # 行政職級
    'researcher': [24, 25, 26, 27],    # 研究職級
    'special': [28, 29, 30]            # 特殊職位
}

# 自動生成部門對應的管理職位
dept_position_mapping = {}

# 根據部門層級自動設置對應的管理職位
for dept_id in range(1, 41):
    if dept_id in department_levels['organization']:
        dept_position_mapping[dept_id] = level_position_mapping['organization']
    elif dept_id in department_levels['division']:
        dept_position_mapping[dept_id] = level_position_mapping['division']
    else:  # 科級
        dept_position_mapping[dept_id] = level_position_mapping['section']

# 定義哪些職位應視為管理職 (position_level <= 11 的都是管理職)
manager_positions = [i for i in range(1, 12)]  # 1到11為管理職

# ==================== 生成基礎資料 SQL ====================

# 1. 生成部門資料
department_sql = """
-- 插入台積電多層級部門資料
INSERT INTO `t_department` (`department_name`, `department_code`) VALUES 
-- 營運組織
('營運組織', 'OP000'),
('晶圓廠營運處', 'OP100'),
('晶圓一廠', 'OP110'),
('晶圓二廠', 'OP120'),
('晶圓三廠', 'OP130'),
('製程整合處', 'OP200'),
('製程整合一科', 'OP210'),
('製程整合二科', 'OP220'),

-- 研發組織
('研發組織', 'RD000'),
('先進製程研發處', 'RD100'),
('先進製程研發一科', 'RD110'),
('先進製程研發二科', 'RD120'),
('元件研發處', 'RD200'),
('元件研發一科', 'RD210'),
('元件研發二科', 'RD220'),

-- 業務組織
('業務組織', 'SA000'),
('客戶服務處', 'SA100'),
('客戶服務一科', 'SA110'),
('客戶服務二科', 'SA120'),
('業務發展處', 'SA200'),
('業務發展一科', 'SA210'),
('業務發展二科', 'SA220'),

-- 行政組織
('行政組織', 'AD000'),
('人力資源處', 'AD100'),
('人資規劃科', 'AD110'),
('人才發展科', 'AD120'),
('財務處', 'AD200'),
('會計科', 'AD210'),
('財務規劃科', 'AD220'),
('法務處', 'AD300'),
('法務一科', 'AD310'),
('法務二科', 'AD320'),

-- 資訊技術組織
('資訊技術組織', 'IT000'),
('資訊系統處', 'IT100'),
('企業系統科', 'IT110'),
('製造系統科', 'IT120'),
('資訊安全科', 'IT130'),
('基礎設施處', 'IT200'),
('網路管理科', 'IT210'),
('伺服器管理科', 'IT220');
"""
write_sql_file('company_data_sql/t_department.sql', department_sql)

# 2. 生成角色資料
role_sql = """
-- 插入角色資料
INSERT INTO `t_role` (`name`) VALUES
('EMPLOYEE'),
('MANAGER');
"""
write_sql_file('company_data_sql/t_role.sql', role_sql)

# 3. 寫入職位資料
position_sql = """
-- 插入職位資料
INSERT INTO `t_position` (`position_name`, `position_level`) VALUES 
-- 高階管理層
('執行長', 1),
('總經理', 2),
('副總經理', 3),

-- 組織主管
('組織長', 4),
('副組織長', 5),

-- 處級主管
('處長', 6),
('副處長', 7),
('資深經理', 8),

-- 科級主管
('科長', 9),
('副科長', 10),
('經理', 11),

-- 工程師職級
('首席工程師', 12),
('資深工程師', 13),
('工程師', 14),
('助理工程師', 15),
('實習工程師', 16),

-- 技術人員職級
('資深技術員', 17),
('技術員', 18),
('助理技術員', 19),

-- 行政職級
('資深專員', 12),
('專員', 13),
('助理專員', 14),
('行政人員', 15),

-- 研究職級
('首席研究員', 12),
('資深研究員', 13),
('研究員', 14),
('助理研究員', 15),

-- 特殊職位
('顧問', 8),
('專案經理', 11),
('專案協調員', 13);
"""
write_sql_file('company_data_sql/t_position.sql', position_sql)

# 4. 生成請假類型資料
leave_type_sql = """
-- 插入請假類型資料
INSERT INTO `t_leave_type` (`leave_type_id`, `leave_type_name`, `attachment_required`) VALUES
(1, '特休假', 0),
(2, '病假', 1),
(3, '事假', 0);
"""
write_sql_file('company_data_sql/t_leave_type.sql', leave_type_sql)

# 5. 生成請假規則資料
leave_rules_sql = """
-- 插入請假規則資料 (根據勞動基準法規定)
INSERT INTO `t_leave_rules` (`leave_type_id`, `months_of_service_min`, `months_of_service_max`, `hours_entitled`) VALUES
-- 特休假規則 (月資轉換為年)
(1, 0, 6, 0),                   -- 未滿半年：無特休
(1, 6, 12, 24),                 -- 半年以上未滿一年：3天 (24小時)
(1, 12, 24, 56),                -- 一年以上未滿兩年：7天 (56小時)
(1, 24, 36, 80),                -- 兩年以上未滿三年：10天 (80小時)
(1, 36, 60, 112),               -- 三年以上未滿五年：14天 (112小時)
(1, 60, 120, 120),              -- 五年以上未滿十年：15天 (120小時)
(1, 120, 240, 160),             -- 十年以上未滿二十年：20天 (160小時)
(1, 240, NULL, 192),            -- 二十年以上：24天 (192小時)

-- 病假規則
(2, 0, NULL, 240),              -- 所有員工：30天 (240小時)

-- 事假規則
(3, 0, NULL, 112);              -- 所有員工：14天 (112小時)
"""
write_sql_file('company_data_sql/t_leave_rules.sql', leave_rules_sql)

# ==================== 生成員工資料 ====================

# 儲存所有員工資料
employees = []

# 儲存部門主管對應表
supervisor_map = {}

# 儲存所有員工角色資料
employee_roles = []

# 管理員工ID列表，用於後續設置審核人
manager_ids = []

# 為每個部門建立一名主管
for dept_id, position_id in dept_position_mapping.items():
    hire_date = datetime(random.randint(2010, 2020), random.randint(1, 12), random.randint(1, 28))
    months_of_service = (datetime.now() - hire_date).days // 30
    
    employee_id = len(employees) + 1
    dept_code = department_codes[dept_id]
    employee_code = f"TSM{dept_code}{employee_id:04d}"
    
    employees.append({
        'employee_id': employee_id,
        'employee_code': employee_code,
        'employee_name': fake.name(),
        'password': generate_password(),
        'department_id': dept_id,
        'position_id': position_id,
        'supervisor_id': None,  # 暫時為None，後面會更新
        'hire_date': hire_date.strftime('%Y-%m-%d'),
        'months_of_service': months_of_service
    })
    
    # 添加到主管映射
    supervisor_map[dept_id] = employee_id
    
    # 添加到管理員工ID列表
    manager_ids.append(employee_id)
    
    # 添加角色 - 主管同時有EMPLOYEE和MANAGER兩個角色
    employee_roles.append({
        'employee_id': employee_id,
        'role_id': 1  # EMPLOYEE角色
    })
    employee_roles.append({
        'employee_id': employee_id,
        'role_id': 2  # MANAGER角色
    })

# 更新主管的supervisor_id
for i, emp in enumerate(employees):
    dept_id = emp['department_id']
    parent_dept_id = department_hierarchy[dept_id]['parent']
    
    if parent_dept_id is not None:
        # 將此部門主管的supervisor設為上級部門的主管
        employees[i]['supervisor_id'] = supervisor_map[parent_dept_id]

# 為每個部門生成普通員工
for dept_id in range(1, 41):
    # 根據部門層級決定員工數量
    if dept_id in department_levels['organization']:  # 組織層級
        num_employees = random.randint(1, 3)  # 組織層級下屬較少
    elif dept_id in department_levels['division']:  # 處級
        num_employees = random.randint(2, 5)  # 處級下屬適中
    else:  # 科級
        num_employees = random.randint(5, 15)  # 科級下屬較多
    
    for i in range(num_employees):
        employee_id = len(employees) + 1
        dept_code = department_codes[dept_id]
        employee_code = f"TSM{dept_code}{employee_id:04d}"
        
        # 設置入職日期和服務月數
        hire_date = datetime(random.randint(2015, 2022), random.randint(1, 12), random.randint(1, 28))
        months_of_service = (datetime.now() - hire_date).days // 30
        
        # 根據部門類別決定職位類別
        if dept_id in department_categories['operations']:  # 營運相關
            possible_categories = ['engineer', 'technician']
        elif dept_id in department_categories['research']:  # 研發相關
            possible_categories = ['engineer', 'researcher']
        elif dept_id in department_categories['business']:  # 業務相關
            possible_categories = ['admin', 'special']
        elif dept_id in department_categories['administration']:  # 行政相關
            possible_categories = ['admin']
        else:  # 資訊相關
            possible_categories = ['engineer', 'special']
        
        # 隨機選擇一個職位類別，然後從該類別中選擇具體職位
        category = random.choice(possible_categories)
        position_id = random.choice(position_categories[category])
        
        employees.append({
            'employee_id': employee_id,
            'employee_code': employee_code,
            'employee_name': fake.name(),
            'password': generate_password(),
            'department_id': dept_id,
            'position_id': position_id,
            'supervisor_id': supervisor_map[dept_id],  # 部門主管作為直接上級
            'hire_date': hire_date.strftime('%Y-%m-%d'),
            'months_of_service': months_of_service
        })
        
        # 添加角色 - 普通員工只有EMPLOYEE角色
        employee_roles.append({
            'employee_id': employee_id,
            'role_id': 1  # EMPLOYEE角色
        })

# ==================== 生成假期資料 ====================

# 生成員工假期餘額
employee_leave_balances = []
current_year = datetime.now().year

for employee in employees:
    employee_id = employee['employee_id']
    months_of_service = employee['months_of_service']
    
    # 特休假計算 - 使用函數計算
    annual_leave_hours = calculate_annual_leave_hours(months_of_service)
    
    # 特休假 - 初始設定為未使用
    employee_leave_balances.append({
        'employee_id': employee_id,
        'leave_type_id': 1,  # 特休假
        'year': current_year,
        'total_hours': annual_leave_hours,
        'used_hours': 0,
        'remaining_hours': annual_leave_hours
    })
    
    # 病假 (30天，半薪) - 初始設定為未使用
    sick_leave_total = 240  # 30天
    employee_leave_balances.append({
        'employee_id': employee_id,
        'leave_type_id': 2,  # 病假
        'year': current_year,
        'total_hours': sick_leave_total,
        'used_hours': 0,
        'remaining_hours': sick_leave_total
    })
    
    # 事假 (14天，無薪) - 初始設定為未使用
    personal_leave_total = 112  # 14天
    employee_leave_balances.append({
        'employee_id': employee_id,
        'leave_type_id': 3,  # 事假
        'year': current_year,
        'total_hours': personal_leave_total,
        'used_hours': 0,
        'remaining_hours': personal_leave_total
    })

# 生成請假單
leave_applications = []
status_options = ['待審核', '已核准', '已拒絕']

# 請假機率控制 - 大約30%的員工有請假記錄
employees_with_leave = random.sample(employees, int(len(employees) * 0.3))

for employee in employees_with_leave:
    employee_id = employee['employee_id']
    department_id = employee['department_id']
    
    # 獲取該員工的主管ID
    supervisor_id = employee['supervisor_id'] if employee['supervisor_id'] else random.choice(manager_ids)
    
    # 為該員工生成1-3張請假單
    num_applications = random.randint(1, 3)
    
    # 尋找該員工的假期餘額記錄
    employee_balances = {}
    for balance in employee_leave_balances:
        if balance['employee_id'] == employee_id:
            employee_balances[balance['leave_type_id']] = balance
    
    # 尋找同部門的員工作為代理人
    same_dept_employees = [e for e in employees if e['department_id'] == department_id and e['employee_id'] != employee_id]
    # 如果同部門沒有其他員工，則不生成請假單
    if not same_dept_employees:
        continue
    
    for i in range(num_applications):
        # 設置請假類型 - 確保員工有足夠的時數可以請
        available_leave_types = []
        for leave_type_id in range(1, 4):
            if leave_type_id in employee_balances and employee_balances[leave_type_id]['remaining_hours'] > 0:
                available_leave_types.append(leave_type_id)
        
        # 如果沒有可用的假期類型，跳過此次循環
        if not available_leave_types:
            continue
            
        leave_type_id = random.choice(available_leave_types)
        
        # 計算可請的最大時數 (不超過剩餘時數)
        max_hours_to_take = min(40, employee_balances[leave_type_id]['remaining_hours'])
        if max_hours_to_take <= 0:
            continue
            
        # 設置請假時間 (半天、一天或多天)
        possible_hours = [4, 8]  # 半天或一天
        if max_hours_to_take >= 16:
            possible_hours.extend([16, 24])  # 加入兩天、三天選項
        if max_hours_to_take >= 32:
            possible_hours.append(32)  # 加入四天選項
        if max_hours_to_take >= 40:
            possible_hours.append(40)  # 加入五天選項
            
        leave_hours = random.choice([h for h in possible_hours if h <= max_hours_to_take])
        
        # 設置請假日期 (過去 1-180 天內)
        days_ago = random.randint(1, 180)
        start_date = datetime.now() - timedelta(days=days_ago)
        # 調整到工作日 (週一到週五)
        while start_date.weekday() >= 5:  # 5=週六, 6=週日
            start_date = start_date - timedelta(days=1)
            
        # 調整時間為國定上班時間內 (8:00 到 17:00)
        start_hour = random.choice([8, 9, 10, 13, 14, 15])
        start_date = start_date.replace(hour=start_hour, minute=0, second=0, microsecond=0)
        
        # 計算結束時間
        end_date = start_date + timedelta(hours=leave_hours)
        
        # 確保結束時間不超過下班時間 (17:00)
        if end_date.hour > 17 or (end_date.hour == 17 and end_date.minute > 0):
            # 如果超過，則調整開始時間，使結束時間不超過 17:00
            start_date = start_date.replace(hour=max(8, 17 - leave_hours))
            end_date = start_date + timedelta(hours=leave_hours)

        # 設置申請時間 (請假開始前 1-14 天)
        application_datetime = start_date - timedelta(days=random.randint(1, 14))
        
        # 設置請假狀態 (90%已核准，5%待審核，5%被拒絕)
        status_chance = random.random()
        if status_chance < 0.9:
            status = '已核准'
        elif status_chance < 0.95:
            status = '待審核'
        else:
            status = '已拒絕'
        
        # 設置審核時間 (申請後 4-48 小時內)
        if status == '待審核':
            approval_datetime = None
            approval_reason = ""
        else:
            hours_to_approve = random.randint(4, 48)
            approval_datetime = application_datetime + timedelta(hours=hours_to_approve)
            
            # 設置審核理由
            if status == '已核准':
                approval_reason = random.choice([
                    "符合請假規定，准予請假。", 
                    "已安排人力支援，同意請假。",
                    "已確認請假時間無重要工作，准予請假。"
                ])
            else:  # 已拒絕
                approval_reason = random.choice([
                    "人力不足，請改期請假。",
                    "提交資料不完整，請重新申請。",
                    "與重要工作時間衝突，請協調後重新申請。",
                    "假期餘額不足，無法核准。"
                ])
        
        # 從同部門員工中隨機選擇代理人
        proxy_employee_id = random.choice(same_dept_employees)['employee_id']
        
        # 添加附件 (20%機率有附件)
        has_attachment = random.random() < 0.2
        file_path = f"/uploads/leave/{employee_id}_{leave_type_id}_{days_ago}.pdf" if has_attachment else None
        file_name = f"請假證明_{leave_type_id}_{days_ago}.pdf" if has_attachment else None
        
        # 添加請假理由
        reasons_by_type = {
            1: [  # 特休
                "休假規劃", 
                "旅遊計畫", 
                "個人休息", 
                "家庭活動", 
                "休假"
            ],
            2: [  # 病假
                "身體不適", 
                "感冒發燒", 
                "就醫看診", 
                "牙科治療", 
                "身體不舒服需要休息"
            ],
            3: [  # 事假
                "個人事務處理", 
                "家庭事務", 
                "參加親友婚禮", 
                "處理私人事務", 
                "臨時有事需處理"
            ]
        }
        
        reason = random.choice(reasons_by_type.get(leave_type_id, ["個人因素請假"]))
        
        leave_applications.append({
            'employee_id': employee_id,
            'leave_type_id': leave_type_id,
            'start_datetime': start_date.strftime('%Y-%m-%d %H:%M:%S'),
            'end_datetime': end_date.strftime('%Y-%m-%d %H:%M:%S'),
            'leave_hours': leave_hours,
            'reason': reason,
            'proxy_employee_id': proxy_employee_id,
            'status': status,
            'application_datetime': application_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'approver_employee_id': supervisor_id,
            'approval_reason': approval_reason,
            'approval_datetime': approval_datetime.strftime('%Y-%m-%d %H:%M:%S') if approval_datetime else None,
            'file_path': file_path,
            'file_name': file_name
        })
        
        # 更新該員工的假期使用情況
        if status == '已核准':
            employee_balances[leave_type_id]['used_hours'] += leave_hours
            employee_balances[leave_type_id]['remaining_hours'] -= leave_hours

# ==================== 生成最終 SQL 檔案 ====================

# 寫入員工資料
employee_sql = "-- 插入員工資料\nINSERT INTO `t_employee` (`employee_id`, `employee_code`, `employee_name`, `password`, `department_id`, `position_id`, `supervisor_id`, `hire_date`, `months_of_service`) VALUES\n"
for i, emp in enumerate(employees):
    supervisor_id = emp['supervisor_id'] if emp['supervisor_id'] else "NULL"
    employee_sql += f"({emp['employee_id']}, '{emp['employee_code']}', '{emp['employee_name']}', '{emp['password']}', {emp['department_id']}, {emp['position_id']}, {supervisor_id}, '{emp['hire_date']}', {emp['months_of_service']})"
    if i < len(employees) - 1:
        employee_sql += ",\n"
    else:
        employee_sql += ";"
write_sql_file('company_data_sql/t_employee.sql', employee_sql)

# 寫入員工角色資料
employee_role_sql = "-- 插入員工角色資料\nINSERT INTO `t_employee_role` (`employee_id`, `role_id`) VALUES\n"
for i, role in enumerate(employee_roles):
    employee_role_sql += f"({role['employee_id']}, {role['role_id']})"
    if i < len(employee_roles) - 1:
        employee_role_sql += ",\n"
    else:
        employee_role_sql += ";"
write_sql_file('company_data_sql/t_employee_role.sql', employee_role_sql)

# 寫入員工假期餘額資料
employee_leave_balance_sql = "-- 插入員工假期餘額資料\nINSERT INTO `t_employee_leave_balance` (`employee_id`, `leave_type_id`, `year`, `total_hours`, `used_hours`, `remaining_hours`) VALUES\n"
for i, balance in enumerate(employee_leave_balances):
    employee_leave_balance_sql += f"({balance['employee_id']}, {balance['leave_type_id']}, {balance['year']}, {balance['total_hours']}, {balance['used_hours']}, {balance['remaining_hours']})"
    if i < len(employee_leave_balances) - 1:
        employee_leave_balance_sql += ",\n"
    else:
        employee_leave_balance_sql += ";"
write_sql_file('company_data_sql/t_employee_leave_balance.sql', employee_leave_balance_sql)

# 寫入請假單資料
leave_application_sql = "-- 插入請假單資料\nINSERT INTO `t_leave_application` (`employee_id`, `leave_type_id`, `start_datetime`, `end_datetime`, `leave_hours`, `reason`, `proxy_employee_id`, `status`, `application_datetime`, `approver_employee_id`, `approval_reason`, `approval_datetime`, `file_path`, `file_name`) VALUES\n"
for i, app in enumerate(leave_applications):
    file_path = f"'{app['file_path']}'" if app['file_path'] else "NULL"
    file_name = f"'{app['file_name']}'" if app['file_name'] else "NULL"
    approval_datetime = f"'{app['approval_datetime']}'" if app['approval_datetime'] else "NULL"
    leave_application_sql += f"({app['employee_id']}, {app['leave_type_id']}, '{app['start_datetime']}', '{app['end_datetime']}', {app['leave_hours']}, '{app['reason']}', {app['proxy_employee_id']}, '{app['status']}', '{app['application_datetime']}', {app['approver_employee_id']}, '{app['approval_reason']}', {approval_datetime}, {file_path}, {file_name})"
    if i < len(leave_applications) - 1:
        leave_application_sql += ",\n"
    else:
        leave_application_sql += ";"
write_sql_file('company_data_sql/t_leave_application.sql', leave_application_sql)

print("初始化資料生成完成！")


    
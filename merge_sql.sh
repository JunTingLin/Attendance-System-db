#!/bin/bash

# 建立目標檔案並加入標頭
echo "-- =============================================
-- 公司資料匯入腳本
-- 按照資料表依賴關係順序執行
-- =============================================
" > company_data.sql

# 按照依賴順序合併檔案
cat << EOF >> company_data.sql

-- =============================================
-- 部門資料
-- =============================================
EOF

cat company_data_sql/t_department.sql >> company_data.sql

cat << EOF >> company_data.sql

-- =============================================
-- 職位資料
-- =============================================
EOF

cat company_data_sql/t_position.sql >> company_data.sql

cat << EOF >> company_data.sql

-- =============================================
-- 角色資料
-- =============================================
EOF

cat company_data_sql/t_role.sql >> company_data.sql

cat << EOF >> company_data.sql

-- =============================================
-- 請假類型資料
-- =============================================
EOF

cat company_data_sql/t_leave_type.sql >> company_data.sql

cat << EOF >> company_data.sql

-- =============================================
-- 員工資料
-- =============================================
EOF

cat company_data_sql/t_employee.sql >> company_data.sql

cat << EOF >> company_data.sql

-- =============================================
-- 員工角色關聯
-- =============================================
EOF

cat company_data_sql/t_employee_role.sql >> company_data.sql

cat << EOF >> company_data.sql

-- =============================================
-- 請假規則
-- =============================================
EOF

cat company_data_sql/t_leave_rules.sql >> company_data.sql

cat << EOF >> company_data.sql

-- =============================================
-- 員工請假餘額
-- =============================================
EOF

cat company_data_sql/t_employee_leave_balance.sql >> company_data.sql

cat << EOF >> company_data.sql

-- =============================================
-- 請假申請
-- =============================================
EOF

cat company_data_sql/t_leave_application.sql >> company_data.sql

echo "SQL 檔案已成功合併到 company_data.sql"
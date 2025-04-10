CREATE DATABASE IF NOT EXISTS `Attendance_System`
CHARACTER SET utf8mb4
COLLATE utf8mb4_zh_0900_as_cs;
USE Attendance_System;


CREATE TABLE `t_department`  (
  `department_id` int NOT NULL AUTO_INCREMENT,
  `department_name` varchar(100) NOT NULL COMMENT '部門名稱',
  `department_code` varchar(20) NOT NULL COMMENT '部門代碼',
  PRIMARY KEY (`department_id`)
);

CREATE TABLE `t_employee`  (
  `employee_id` int NOT NULL AUTO_INCREMENT COMMENT '員工ID (自動增加)',
  `employee_code` varchar(50) NOT NULL COMMENT '員工編號(登入帳號)',
  `employee_name` varchar(50) NOT NULL COMMENT '員工姓名',
  `password` varchar(100) NOT NULL COMMENT '登入密碼',
  `department_id` int NOT NULL COMMENT '部門ID',
  `position_id` int NOT NULL COMMENT '職位ID',
  `supervisor_id` int NULL COMMENT '上級主管ID，最高層主管為NULL',
  `hire_date` date NOT NULL COMMENT '入職日期',
  `months_of_service` int NOT NULL COMMENT '服務月資(月)',
  PRIMARY KEY (`employee_id`)
);

CREATE TABLE `t_employee_leave_balance`  (
  `balance_id` int NOT NULL AUTO_INCREMENT COMMENT '餘額記錄唯一識別碼',
  `employee_id` int NOT NULL COMMENT '員工ID',
  `leave_type_id` int NOT NULL COMMENT '假別ID',
  `year` INT NOT NULL COMMENT '年度',
  `total_hours` int NOT NULL COMMENT '總額度(小時)',
  `used_hours` int NOT NULL COMMENT '已使用額度(小時)',
  `remaining_hours` int NOT NULL COMMENT '剩餘額度(小時)',
  PRIMARY KEY (`balance_id`)
);

CREATE TABLE `t_employee_role`  (
  `employee_role_id` int NOT NULL AUTO_INCREMENT,
  `employee_id` int NOT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`employee_role_id`)
);

CREATE TABLE `t_leave_application`  (
  `application_id` int NOT NULL AUTO_INCREMENT,
  `employee_id` int NOT NULL COMMENT '申請人ID',
  `leave_type_id` int NOT NULL COMMENT '假別ID',
  `start_datetime` datetime NOT NULL COMMENT '請假開始時間',
  `end_datetime` datetime NOT NULL COMMENT '請假結束時間',
  `leave_hours` int NOT NULL COMMENT '請假時數',
  `reason` varchar(500) NOT NULL COMMENT '請假事由',
  `proxy_employee_id` int NOT NULL COMMENT '代理人ID',
  `status` varchar(20) NOT NULL COMMENT '申請狀態(待審核、已核准、已拒絕)',
  `application_datetime` datetime NOT NULL COMMENT '申請日期時間',
  `approver_employee_id` int NOT NULL COMMENT '審核人ID',
  `approval_reason` varchar(500) NOT NULL COMMENT '審核理由',
  `approval_datetime` datetime NOT NULL COMMENT '審核日期時間',
  `file_path` varchar(500) NULL COMMENT '檔案儲存路徑(url)',
  `file_name` varchar(255) NULL COMMENT '檔案名稱',
  PRIMARY KEY (`application_id`)
);

CREATE TABLE `t_leave_rules`  (
  `rule_id` int NOT NULL AUTO_INCREMENT,
  `leave_type_id` int NOT NULL COMMENT '假別ID (連接到t_leave_type)',
  `months_of_service_min` int NOT NULL COMMENT '月資下限(含)',
  `months_of_service_max` int NULL COMMENT '月資上限(不含)，NULL表示無上限',
  `hours_entitled` int NOT NULL COMMENT '該年資區間對應的假期時數',
  PRIMARY KEY (`rule_id`)
);

CREATE TABLE `t_leave_type`  (
  `leave_type_id` int NOT NULL AUTO_INCREMENT COMMENT '假別唯一識別碼',
  `leave_type_name` varchar(50) NOT NULL COMMENT '假別名稱(特休、病假、事假)',
  `attachment_required` tinyint(1) NOT NULL COMMENT '是否需要附件',
  PRIMARY KEY (`leave_type_id`)
);

CREATE TABLE `t_position`  (
  `position_id` int NOT NULL AUTO_INCREMENT,
  `position_name` varchar(100) NOT NULL COMMENT '職位名稱(處長,副處長,科長, 軟體程師等)',
  `position_level` int NOT NULL COMMENT '職位層級(數字越小層級越高)',
  PRIMARY KEY (`position_id`)
);

CREATE TABLE `t_role`  (
  `role_id` int NOT NULL AUTO_INCREMENT COMMENT '角色ID',
  `name` varchar(50) NOT NULL COMMENT '角色名稱（例如：EMPLOYEE、MANAGER）',
  PRIMARY KEY (`role_id`)
);

ALTER TABLE `t_employee` ADD CONSTRAINT `fk_supervisor_id` FOREIGN KEY (`supervisor_id`) REFERENCES `t_employee` (`employee_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE `t_employee` ADD CONSTRAINT `fk_department_id` FOREIGN KEY (`department_id`) REFERENCES `t_department` (`department_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE `t_employee` ADD CONSTRAINT `fk_position_id` FOREIGN KEY (`position_id`) REFERENCES `t_position` (`position_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE `t_employee_leave_balance` ADD CONSTRAINT `fk_t_employee_leave_balance_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `t_employee` (`employee_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE `t_employee_leave_balance` ADD CONSTRAINT `fk_t_employee_leave_balance_leave_type_id` FOREIGN KEY (`leave_type_id`) REFERENCES `t_leave_type` (`leave_type_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE `t_employee_role` ADD CONSTRAINT `fk_t_employee_role_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `t_employee` (`employee_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE `t_employee_role` ADD CONSTRAINT `fk_role_id` FOREIGN KEY (`role_id`) REFERENCES `t_role` (`role_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE `t_leave_application` ADD CONSTRAINT `fk_t_leave_application_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `t_employee` (`employee_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE `t_leave_application` ADD CONSTRAINT `fk_t_leave_application_leave_type_id` FOREIGN KEY (`leave_type_id`) REFERENCES `t_leave_type` (`leave_type_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE `t_leave_application` ADD CONSTRAINT `fk_proxy_employee_id` FOREIGN KEY (`proxy_employee_id`) REFERENCES `t_employee` (`employee_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE `t_leave_application` ADD CONSTRAINT `fk_approver_employee_id` FOREIGN KEY (`approver_employee_id`) REFERENCES `t_employee` (`employee_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE `t_leave_rules` ADD CONSTRAINT `fk_t_leave _rules_leave_type_id` FOREIGN KEY (`leave_type_id`) REFERENCES `t_leave_type` (`leave_type_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;


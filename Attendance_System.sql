/*
 Navicat Premium Data Transfer

 Source Server         : docker
 Source Server Type    : MySQL
 Source Server Version : 80041
 Source Host           : localhost:3307
 Source Schema         : Attendance_System

 Target Server Type    : MySQL
 Target Server Version : 80041
 File Encoding         : 65001

 Date: 13/04/2025 17:08:02
*/

CREATE DATABASE IF NOT EXISTS `Attendance_System`
CHARACTER SET utf8mb4
COLLATE utf8mb4_zh_0900_as_cs;
USE Attendance_System;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_department
-- ----------------------------
DROP TABLE IF EXISTS `t_department`;
CREATE TABLE `t_department`  (
  `department_id` int NOT NULL AUTO_INCREMENT,
  `department_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_zh_0900_as_cs NOT NULL,
  `department_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_zh_0900_as_cs NOT NULL,
  PRIMARY KEY (`department_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_zh_0900_as_cs ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for t_employee
-- ----------------------------
DROP TABLE IF EXISTS `t_employee`;
CREATE TABLE `t_employee`  (
  `employee_id` int NOT NULL AUTO_INCREMENT COMMENT '員工ID (自動增加)',
  `employee_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_zh_0900_as_cs NOT NULL,
  `employee_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_zh_0900_as_cs NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_zh_0900_as_cs NOT NULL,
  `department_id` int NOT NULL COMMENT '部門ID',
  `position_id` int NOT NULL COMMENT '職位ID',
  `supervisor_id` int NULL DEFAULT NULL COMMENT '上級主管ID，最高層主管為NULL',
  `hire_date` date NOT NULL,
  `months_of_service` int NOT NULL COMMENT '服務月資(月)',
  PRIMARY KEY (`employee_id`) USING BTREE,
  INDEX `fk_supervisor_id`(`supervisor_id` ASC) USING BTREE,
  INDEX `fk_department_id`(`department_id` ASC) USING BTREE,
  INDEX `fk_position_id`(`position_id` ASC) USING BTREE,
  CONSTRAINT `fk_department_id` FOREIGN KEY (`department_id`) REFERENCES `t_department` (`department_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_position_id` FOREIGN KEY (`position_id`) REFERENCES `t_position` (`position_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_supervisor_id` FOREIGN KEY (`supervisor_id`) REFERENCES `t_employee` (`employee_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_zh_0900_as_cs ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for t_employee_leave_balance
-- ----------------------------
DROP TABLE IF EXISTS `t_employee_leave_balance`;
CREATE TABLE `t_employee_leave_balance`  (
  `balance_id` int NOT NULL AUTO_INCREMENT COMMENT '餘額記錄唯一識別碼',
  `employee_id` int NOT NULL COMMENT '員工ID',
  `leave_type_id` int NOT NULL COMMENT '假別ID',
  `year` int NOT NULL COMMENT '年度',
  `total_hours` int NOT NULL COMMENT '總額度(小時)',
  `used_hours` int NOT NULL COMMENT '已使用額度(小時)',
  `remaining_hours` int NOT NULL COMMENT '剩餘額度(小時)',
  PRIMARY KEY (`balance_id`) USING BTREE,
  INDEX `fk_t_employee_leave_balance_employee_id`(`employee_id` ASC) USING BTREE,
  INDEX `fk_t_employee_leave_balance_leave_type_id`(`leave_type_id` ASC) USING BTREE,
  CONSTRAINT `fk_t_employee_leave_balance_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `t_employee` (`employee_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_t_employee_leave_balance_leave_type_id` FOREIGN KEY (`leave_type_id`) REFERENCES `t_leave_type` (`leave_type_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_zh_0900_as_cs ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for t_employee_role
-- ----------------------------
DROP TABLE IF EXISTS `t_employee_role`;
CREATE TABLE `t_employee_role`  (
  `employee_role_id` int NOT NULL AUTO_INCREMENT,
  `employee_id` int NOT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`employee_role_id`) USING BTREE,
  INDEX `fk_t_employee_role_employee_id`(`employee_id` ASC) USING BTREE,
  INDEX `fk_role_id`(`role_id` ASC) USING BTREE,
  CONSTRAINT `fk_role_id` FOREIGN KEY (`role_id`) REFERENCES `t_role` (`role_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_t_employee_role_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `t_employee` (`employee_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_zh_0900_as_cs ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for t_leave_application
-- ----------------------------
DROP TABLE IF EXISTS `t_leave_application`;
CREATE TABLE `t_leave_application`  (
  `application_id` int NOT NULL AUTO_INCREMENT,
  `employee_id` int NOT NULL COMMENT '申請人ID',
  `leave_type_id` int NOT NULL COMMENT '假別ID',
  `start_datetime` datetime NOT NULL COMMENT '請假開始時間',
  `end_datetime` datetime NOT NULL COMMENT '請假結束時間',
  `leave_hours` int NOT NULL COMMENT '請假時數',
  `reason` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_zh_0900_as_cs NOT NULL,
  `proxy_employee_id` int NOT NULL COMMENT '代理人ID',
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_zh_0900_as_cs NOT NULL,
  `application_datetime` datetime NOT NULL COMMENT '申請日期時間',
  `approver_employee_id` int NULL DEFAULT NULL COMMENT '審核人ID',
  `approval_reason` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_zh_0900_as_cs NULL DEFAULT NULL,
  `approval_datetime` datetime NULL DEFAULT NULL COMMENT '審核日期時間',
  `file_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_zh_0900_as_cs NULL DEFAULT NULL,
  `file_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_zh_0900_as_cs NULL DEFAULT NULL COMMENT '檔案名稱',
  PRIMARY KEY (`application_id`) USING BTREE,
  INDEX `fk_t_leave_application_employee_id`(`employee_id` ASC) USING BTREE,
  INDEX `fk_t_leave_application_leave_type_id`(`leave_type_id` ASC) USING BTREE,
  INDEX `fk_proxy_employee_id`(`proxy_employee_id` ASC) USING BTREE,
  INDEX `fk_approver_employee_id`(`approver_employee_id` ASC) USING BTREE,
  CONSTRAINT `fk_approver_employee_id` FOREIGN KEY (`approver_employee_id`) REFERENCES `t_employee` (`employee_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_proxy_employee_id` FOREIGN KEY (`proxy_employee_id`) REFERENCES `t_employee` (`employee_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_t_leave_application_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `t_employee` (`employee_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_t_leave_application_leave_type_id` FOREIGN KEY (`leave_type_id`) REFERENCES `t_leave_type` (`leave_type_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_zh_0900_as_cs ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for t_leave_rules
-- ----------------------------
DROP TABLE IF EXISTS `t_leave_rules`;
CREATE TABLE `t_leave_rules`  (
  `rule_id` int NOT NULL AUTO_INCREMENT,
  `leave_type_id` int NOT NULL COMMENT '假別ID (連接到t_leave_type)',
  `months_of_service_min` int NOT NULL COMMENT '月資下限(含)',
  `months_of_service_max` int NULL DEFAULT NULL COMMENT '月資上限(不含)，NULL表示無上限',
  `hours_entitled` int NOT NULL COMMENT '該年資區間對應的假期時數',
  PRIMARY KEY (`rule_id`) USING BTREE,
  INDEX `fk_t_leave _rules_leave_type_id`(`leave_type_id` ASC) USING BTREE,
  CONSTRAINT `fk_t_leave _rules_leave_type_id` FOREIGN KEY (`leave_type_id`) REFERENCES `t_leave_type` (`leave_type_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_zh_0900_as_cs ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for t_leave_type
-- ----------------------------
DROP TABLE IF EXISTS `t_leave_type`;
CREATE TABLE `t_leave_type`  (
  `leave_type_id` int NOT NULL AUTO_INCREMENT COMMENT '假別唯一識別碼',
  `leave_type_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_zh_0900_as_cs NOT NULL,
  `attachment_required` tinyint(1) NOT NULL COMMENT '是否需要附件',
  PRIMARY KEY (`leave_type_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_zh_0900_as_cs ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for t_position
-- ----------------------------
DROP TABLE IF EXISTS `t_position`;
CREATE TABLE `t_position`  (
  `position_id` int NOT NULL AUTO_INCREMENT,
  `position_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_zh_0900_as_cs NOT NULL,
  `position_level` int NOT NULL COMMENT '職位層級(數字越小層級越高)',
  PRIMARY KEY (`position_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_zh_0900_as_cs ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for t_role
-- ----------------------------
DROP TABLE IF EXISTS `t_role`;
CREATE TABLE `t_role`  (
  `role_id` int NOT NULL AUTO_INCREMENT COMMENT '角色ID',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_zh_0900_as_cs NOT NULL,
  PRIMARY KEY (`role_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_zh_0900_as_cs ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;

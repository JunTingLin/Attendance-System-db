# Attendance-System-db
TSMC Cloud Native

## 專案檔
- **docker-compose.yml**  
  MySQL Docker 容器的設定：
  - **環境變數**：  
    - `MYSQL_ROOT_PASSWORD`：設定 root 使用者密碼（`root123`）。
    - `MYSQL_DATABASE`：自動建立的資料庫名稱`Attendance_System`。
    - `MYSQL_USER` 與 `MYSQL_PASSWORD`：用來建立應用程式使用者，設定為 `user` 與 `user123`。
  - **持久卷設定**：  
    使用 named volume `mysql_data`，將容器內的 `/var/lib/mysql` 資料夾掛載。
  - **SQL 初始化**：  
    將根目錄下的 `Attendance_System.sql` 掛載到 `/docker-entrypoint-initdb.d/`，容器在首次啟動時會自動執行該 SQL 腳本建立資料庫與資料表。

- **Attendance_System.sql**  
  用於建立實際資料表、定義外部鍵約束以及各種資料表間的關聯。可直接匯入 MySQL 使用。

- **Attendance_System_with_data.sql**  
除了建立資料表外，還包假資料。可直接匯入 MySQL 使用，亦會在容器初始化時自動執行。

- **Diagram 1.png**  
  ERD 圖檔，資料庫的大致設計架構。部分例如「一對多」等詳細關聯關係在圖中未有特別標示，僅作為整體參考。

- **Attendance-System.ndm2**  
  ERD 的工作檔案，需使用 [Navicat Premium](https://www.navicat.com/en/products/navicat-premium) 開啟編輯。後續進一步調整 ERD 才需使用。

## 如何使用
### 1. 前置作業
- 確認已安裝 [Docker](https://www.docker.com/) 與 [Docker Compose](https://docs.docker.com/compose/)。
- clone 此專案，確保所有檔案皆位於專案根目錄中。

### 2. 啟動 MySQL 容器
在專案根目錄下，開啟終端機或命令提示字元，執行以下指令：
```bash
docker-compose up -d
```

執行後，Docker Compose 將依照 docker-compose.yml 的配置啟動 MySQL 容器：

+ 容器會自動執行 Attendance_System.sql 腳本以初始化資料庫。
+ 資料將儲存在名為 mysql_data 的持久卷中。
+ 考量到可能像我一樣本機3306被占用，可以在[env](./.env)去配置MYSQL_HOST_PORT，目前是3307


### 3. 連線與驗證
+ 連線資訊
你可以使用任何 MySQL 客戶端（例如 Navicat、MySQL Workbench、命令列工具）連線：

    + Host：localhost

    + Port：依照上述設定

    + 使用者：user

    + 密碼：user123

    + 資料庫：Attendance_System

+ 管理員使用者
若需要進行管理操作，請使用 root 帳戶：

    + 使用者：root

    + 密碼：root123

# 台積電請假系統資料初始化說明

本文件說明 `init_data.py` 腳本生成的初始化資料結構和規則。

## 資料結構概述

腳本生成以下 SQL 檔案：
- `t_department.sql` - 部門資料
- `t_role.sql` - 角色資料
- `t_position.sql` - 職位資料
- `t_leave_type.sql` - 請假類型資料
- `t_leave_rules.sql` - 請假規則資料
- `t_employee.sql` - 員工資料
- `t_employee_role.sql` - 員工角色資料
- `t_employee_leave_balance.sql` - 員工假期餘額資料
- `t_leave_application.sql` - 請假單資料

## 部門結構

部門採用多層級結構，共有 40 個部門，分為以下類別：
- 營運組織 (OP)
- 研發組織 (RD)
- 業務組織 (SA)
- 行政組織 (AD)
- 資訊技術組織 (IT)

部門層級分為：
- 組織層級 (如：營運組織)
- 處級 (如：晶圓廠營運處)
- 科級 (如：晶圓一廠)

部門代碼規則：
- 前兩字母代表部門類別 (OP, RD, SA, AD, IT)
- 後三位數字代表層級和序號

## 職位結構

職位分為多個層級，職位層級數字越小代表職級越高：
- 高階管理層 (1-3)：執行長、總經理、副總經理
- 組織主管 (4-5)：組織長、副組織長
- 處級主管 (6-8)：處長、副處長、資深經理
- 科級主管 (9-11)：科長、副科長、經理
- 一般職位 (12+)：工程師、技術員、專員等

職位類別：
- 工程師職級 (12-16)
- 技術人員職級 (17-19)
- 行政職級 (20-23)
- 研究職級 (24-27)
- 特殊職位 (28-30)

## 角色設定

系統有兩種角色：
- EMPLOYEE：一般員工角色
- MANAGER：管理者角色

所有員工都有 EMPLOYEE 角色，主管同時擁有 MANAGER 角色。

## 請假類型與規則

請假類型：
1. 特休假 (不需附件)
2. 病假 (需附件)
3. 事假 (不需附件)

特休假規則 (根據勞動基準法)：
- 未滿半年：無特休
- 半年以上未滿一年：3天 (24小時)
- 一年以上未滿兩年：7天 (56小時)
- 兩年以上未滿三年：10天 (80小時)
- 三年以上未滿五年：14天 (112小時)
- 五年以上未滿十年：15天 (120小時)
- 十年以上未滿二十年：20天 (160小時)
- 二十年以上：24天 (192小時)

其他假別：
- 病假：30天 (240小時)
- 事假：14天 (112小時)

## 員工資料生成規則

1. 每個部門都有一名主管
2. 部門主管的上級是上層部門的主管
3. 員工數量根據部門層級決定：
   - 組織層級：1-3名員工
   - 處級：2-5名員工
   - 科級：5-15名員工
4. 員工職位根據部門類別分配：
   - 營運相關：工程師、技術人員
   - 研發相關：工程師、研究員
   - 業務相關：行政人員、特殊職位
   - 行政相關：行政人員
   - 資訊相關：工程師、特殊職位

## 請假資料生成規則

1. 約30%的員工有請假記錄
2. 每位有請假記錄的員工生成1-3張請假單
3. 請假狀態分布：
   - 90% 已核准
   - 5% 待審核
   - 5% 已拒絕
4. 請假時間設定在過去1-180天內
5. 請假時長為半天到五天不等
6. 請假時間調整為工作日 (週一到週五) 的上班時間 (8:00-17:00)
7. 申請時間設定為請假開始前1-14天
8. 審核時間設定為申請後4-48小時內
9. 約20%的請假單有附件
10. 代理人從同部門員工中隨機選擇

## 員工編號規則

員工編號格式：TSM + 完整部門代碼 + 四位序號
例如：TSMOP000001, TSMRD1100025

## 密碼生成規則

後來改為Bcrypt hash，`$10$5.skwDVPMxIBe5T3FqeZm.pRb47Fgf4UR3JGATVM6cfyH.5g9YLI2`對應的明碼是`123`
# Data Inventory Dashboard

## Overview

Data Inventory Dashboard is a Python and Flask based monitoring solution used to track, audit, and monitor both Raw Files and Formatted Files across historical market data repositories.

The application automatically scans configured data folders, calculates:

* Dataset availability
* File counts
* Date coverage
* Trading Day summaries
* Dataset status

and stores the results in SQLite databases.

The dashboard provides a centralized inventory view, while Excel reports are generated automatically for operational monitoring.

---

# Features

## Inventory Monitoring

* Formatted Files Monitoring
* Raw Files Monitoring
* Recursive Folder Scanning
* Dataset Health Monitoring
* File Count Validation
* Date Range Coverage Validation
* Trading Day Summary Generation

## Reporting

* Daily Excel Report Generation
* Historical Report Archive
* Latest Inventory Reports
* Inventory Database Refresh

## Dashboard

* Flask Web Dashboard
* Formatted Report View
* Raw Report View
* Dataset Search
* Manual Refresh
* Light Theme
* Dark Theme
* Auto Refresh Support

## Automation

* EXE Deployment Support
* Windows Task Scheduler Integration
* Daily Automated Inventory Scans

---

# Project Structure

```text
FILES DATA LOGES

├── app.py
├── scanner.py
├── scanner_raw.py
│
├── config_formatted.json
├── config_raw.json
│
├── inventory_formatted.db
├── inventory_raw.db
│
├── templates
│   └── index.html
│
├── reports
│   ├── Formatted_Inventory_Report_YYYYMMDD.xlsx
│   └── Raw_Inventory_Report_YYYYMMDD.xlsx
│
├── logs
│   ├── scanner_YYYYMMDD.log
│
├── scanner.exe
├── scanner_raw.exe
├── app.exe
│
├── run_inventory.bat
│
└── README.md
```

---

# Requirements

Python 3.10+

Install required packages:

```bash
pip install flask pandas openpyxl pyinstaller
```

---

# Configuration

## Formatted Files Configuration

Edit:

```text
config_formatted.json
```

Example:

```json
{
  "root_folder": "H:/DATA/FOLDERS/DATA PROJECTS/FORMATTED FILES",
  "datasets": []
}
```

---

## Raw Files Configuration

Edit:

```text
config_raw.json
```

Example:

```json
{
  "root_folder": "G:/Ganesh/NEW RAW FILES",
  "datasets": []
}
```

---

# Database

## Formatted Inventory Database

```text
inventory_formatted.db
```

Table:

```text
inventory
```

Columns:

```text
folder1
folder2
folder3
file_name
full_path
from_date
to_date
file_count
status
last_updated
```

---

## Raw Inventory Database

```text
inventory_raw.db
```

Table:

```text
inventory
```

Columns:

```text
folder1
folder2
folder3
file_name
full_path
from_date
to_date
file_count
status
last_updated
```

---

# Running Scanners

## Formatted Files Scanner

```bash
python scanner.py
```

This will:

* Scan configured formatted datasets
* Update inventory_formatted.db
* Generate Excel reports
* Update latest inventory report

---

## Raw Files Scanner

```bash
python scanner_raw.py
```

This will:

* Scan configured raw datasets
* Update inventory_raw.db
* Generate Excel reports
* Update latest inventory report

---

# Running Dashboard

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

Dashboard provides:

* Formatted Report View
* Raw Report View
* Search Functionality
* Refresh Functionality
* Theme Switching

---

# Excel Reports

## Formatted Report

Latest:

```text
G:\Ganesh\Data_Inventory_Formatted.xlsx
```

Historical:

```text
reports\Formatted_Inventory_Report_YYYYMMDD.xlsx
```

---

## Raw Report

Latest:

```text
G:\Ganesh\Data_Inventory_Raw.xlsx
```

Historical:

```text
reports\Raw_Inventory_Report_YYYYMMDD.xlsx
```

---

# Trading Days Summary

The application automatically generates:

```text
TRADING DAYS_OLD
TRADING DAYS_NEW
```

Examples:

```text
TD_OLD_19970401_20170331
TD_NEW_20170401_YYYYMMDD
```

These are displayed in both reports and dashboard views.

---

# Building EXE Files

## Scanner EXE

```bash
pyinstaller --onefile scanner.py
```

## Raw Scanner EXE

```bash
pyinstaller --onefile scanner_raw.py
```

## Dashboard EXE

```bash
pyinstaller ^
--onefile ^
--add-data "templates;templates" ^
app.py
```

Generated files:

```text
scanner.exe
scanner_raw.exe
app.exe
```

---

# Automated Daily Execution

## Batch File

File:

```text
run_inventory.bat
```

Contents:

```bat
@echo off

cd /d "G:\Ganesh\FILES DATA LOGES\dist"

scanner.exe
scanner_raw.exe

exit
```

---

## Windows Task Scheduler

Task Name:

```text
Daily Inventory Scan
```

Trigger:

```text
Daily
09:00 AM
```

Action:

```text
run_inventory.bat
```

Purpose:

* Execute scanner.exe
* Execute scanner_raw.exe
* Refresh databases
* Generate reports automatically

---

# Logs

Location:

```text
logs\
```

Example:

```text
scanner_YYYYMMDD.log
```

Contains:

* Scan Start
* Dataset Processing
* File Counts
* Date Ranges
* Report Generation
* Database Updates
* Errors and Exceptions

---

# Dashboard Features

## Formatted Report

Displays:

* Folder Structure
* File Naming Pattern
* Date Coverage
* File Count
* Status

## Raw Report

Displays:

* Folder Structure
* File Naming Pattern
* Date Coverage
* File Count
* Status

---

# Technologies Used

* Python
* Flask
* SQLite
* Pandas
* OpenPyXL
* PyInstaller
* Windows Task Scheduler

---

# Author

Ganesh

---

# Version

Version: 1.0

Status: Production Ready

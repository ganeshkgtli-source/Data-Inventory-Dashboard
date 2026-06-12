# Data Inventory Dashboard

## Overview

Data Inventory Dashboard is a Python + Flask based monitoring system used to track and audit historical market data repositories.

The application scans configured data folders, calculates:

* Dataset availability
* File counts
* Date coverage
* Trading day ranges
* Dataset status

and stores the results in SQLite.

The dashboard provides a real-time inventory view while Excel reports are generated automatically.

---

## Features

* Automated folder scanning
* SQLite inventory database
* Flask dashboard
* Excel report generation
* Historical report archive
* Latest dashboard Excel export
* Trading Days Summary
* Automatic daily execution using Windows Task Scheduler
* Recursive file discovery
* Dataset health monitoring

---

## Project Structure

```text
FILES DATA LOGES

├── app.py
├── scanner.py
├── config.json
├── inventory.db
│
├── templates
│   └── index.html
│
├── reports
│   ├── Inventory_Report_YYYYMMDD.xlsx
│
├── logs
│   ├── scanner_YYYYMMDD.log
│
└── Data_Inventory_Dashboard.xlsx
```

---

## Requirements

Python 3.10+

Install dependencies:

```bash
pip install flask pandas openpyxl
```

---

## Configuration

Edit:

```text
config.json
```

Example:

```json
{
    "root_folder": "H:/DATA/FOLDERS/DATA PROJECTS/FORMATTED FILES",
    "datasets": [
        {
            "folder1": "01_BSE_CM",
            "folder2": "BSE_CM_INDICES",
            "folder3": "1_MIN_EOD",
            "file_pattern": "*.csv"
        }
    ]
}
```

---

## Running Scanner

```bash
python scanner.py
```

This will:

* Scan all configured folders
* Update inventory.db
* Generate daily Excel report
* Update Data_Inventory_Dashboard.xlsx

---

## Running Dashboard

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## Automated Daily Execution

Use Windows Task Scheduler:

Trigger:

```text
Daily
09:00 AM
```

Action:

```text
DataInventoryScanner.exe
```

or

```text
python scanner.py
```

---

## Generated Outputs

### Database

```text
inventory.db
```

### Latest Dashboard Excel

```text
G:\Ganesh\Data_Inventory_Dashboard.xlsx
```

### Historical Reports

```text
reports\Inventory_Report_YYYYMMDD.xlsx
```

### Logs

```text
logs\scanner_YYYYMMDD.log
```

---

## Technologies

* Python
* Flask
* SQLite
* Pandas
* OpenPyXL

---

## Author

Ganesh

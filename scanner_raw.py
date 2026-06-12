import os
import re
import json
import sqlite3
import logging
from pathlib import Path
from datetime import datetime

import pandas as pd

# ============================================================
# PATHS
# ============================================================

import sys

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parent

CONFIG_FILE = BASE_DIR / "config_raw.json"
DATABASE_FILE = BASE_DIR / "inventory_raw.db"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"

REPORTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# ============================================================
# LOGGING
# ============================================================

log_file = LOGS_DIR / f"scanner_{datetime.now():%Y%m%d}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# ============================================================
# DATABASE
# ============================================================

def create_database():
    conn = sqlite3.connect(DATABASE_FILE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS inventory
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    folder1 TEXT,
    folder2 TEXT,
    folder3 TEXT,

    file_name TEXT,

    full_path TEXT,

    from_date TEXT,
    to_date TEXT,

    file_count INTEGER,
    status TEXT,

    last_updated TEXT
)
    """)

    conn.commit()
    conn.close()

# ============================================================
# LOAD CONFIG
# ============================================================

def load_config():

    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Config file not found: {CONFIG_FILE}"
        )

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ============================================================
# EXTRACT DATE
# ============================================================

def extract_date(filename: str):

    matches = re.findall(r'(\d{8})', filename)

    valid_dates = []

    for value in matches:

        try:
            datetime.strptime(value, "%Y%m%d")
            valid_dates.append(value)

        except Exception:
            pass

    return valid_dates

# ============================================================
# SCAN DATASET
# ============================================================

def scan_dataset(root_folder, dataset):

    folder1 = dataset["folder1"]
    folder2 = dataset["folder2"]
    folder3 = dataset.get("folder3", "")

    physical_folder = dataset.get(
        "physical_folder",
        folder3
    )

    file_pattern = dataset.get(
        "file_pattern",
        "*.csv"
    )

    logger.info(
        f"Scanning: {folder1}/{folder2}/{physical_folder}"
    )

    folder_path = (
        Path(root_folder)
        / folder1
        / folder2
    )

    if physical_folder:
        folder_path = folder_path / physical_folder

    logger.info(
        f"Scanning Path: {folder_path}"
    )

    if not folder_path.exists():

        logger.warning(
            f"Folder not found: {folder_path}"
        )

        return {
            "folder1": folder1,
            "folder2": folder2,
            "folder3": folder3,

            "file_name": dataset.get(
                "file_name_pattern",
                ""
            ),

            "full_path": str(folder_path),

            "from_date": "",
            "to_date": "",

            "file_count": 0,

            "status": "NO FILES"
        }

    files = list(
        folder_path.rglob(file_pattern)
    )

    all_dates = []

    for file in files:

        extracted = extract_date(
            file.name
        )

        if extracted:
            all_dates.extend(extracted)

    all_dates = sorted(
        set(all_dates)
    )

    from_date = (
        all_dates[0]
        if all_dates else ""
    )

    to_date = (
        all_dates[-1]
        if all_dates else ""
    )

    # -----------------------------------------
    # Fixed date override
    # -----------------------------------------

    if dataset.get("from_date_fixed"):

        from_date = dataset[
            "from_date_fixed"
        ]

    if dataset.get("to_date_fixed"):

        to_date = dataset[
            "to_date_fixed"
        ]

    result = {

        "folder1": folder1,
        "folder2": folder2,
        "folder3": folder3,

        "file_name": dataset.get(
            "file_name_pattern",
            ""
        ),

        "full_path": str(folder_path),

        "from_date": from_date,
        "to_date": to_date,

        "file_count": len(files),

        "status": (
            "AVAILABLE"
            if len(files) > 0
            else "NO FILES"
        )
    }

    logger.info(
        f"{folder2}/{folder3} | "
        f"Files={len(files)} | "
        f"From={from_date} | "
        f"To={to_date}"
    )

    return result
# ============================================================
# SAVE TO SQLITE
# ============================================================

def save_to_database(df):

    conn = sqlite3.connect(DATABASE_FILE)

    conn.execute("DELETE FROM inventory")

    df.to_sql(
        "inventory",
        conn,
        if_exists="append",
        index=False
    )

    conn.commit()
    conn.close()

# ============================================================
# SAVE EXCEL
# ============================================================

def save_excel(df):

    daily_excel_file = (
        REPORTS_DIR
        / f"Raw_Inventory_Report_{datetime.now():%Y%m%d}.xlsx"
    )

    latest_excel_file = Path(
        r"G:\Ganesh\Data_Inventory_Raw.xlsx"
    )

    excel_df = df.copy()

    # ==========================================
    # RENAME COLUMNS
    # ==========================================

    excel_df = excel_df.rename(
        columns={
            "folder1": "01_FOLDER NAME",
            "folder2": "02_FOLDER NAME",
            "folder3": "03_FOLDER NAME",

            "file_name": "04_FILE NAME",

            "from_date": "FROM DATE",
            "to_date": "TO DATE",

            "file_count": "NO OF FILES",

            "status": "STATUS",

            "last_updated": "LAST UPDATED"
        }
    )

    # ==========================================
    # KEEP ONLY REQUIRED COLUMNS
    # ==========================================

    excel_df = excel_df[
        [
            "01_FOLDER NAME",
            "02_FOLDER NAME",
            "03_FOLDER NAME",
            "04_FILE NAME",
            "FROM DATE",
            "TO DATE",
            "NO OF FILES",
            "STATUS",
            "LAST UPDATED"
        ]
    ]

    # ==========================================
    # DATE FORMAT
    # ==========================================

    for col in ["FROM DATE", "TO DATE"]:

        excel_df[col] = pd.to_datetime(
            excel_df[col],
            format="%Y%m%d",
            errors="coerce"
        ).dt.strftime("%d-%m-%Y")

    # ==========================================
    # DAILY REPORT
    # ==========================================

    with pd.ExcelWriter(
        daily_excel_file,
        engine="openpyxl"
    ) as writer:

        excel_df.to_excel(
            writer,
            index=False,
            sheet_name="Inventory"
        )

    logger.info(
        f"Daily Report Created: {daily_excel_file}"
    )

    # ==========================================
    # LATEST REPORT
    # ==========================================

    try:

        with pd.ExcelWriter(
            latest_excel_file,
            engine="openpyxl"
        ) as writer:

            excel_df.to_excel(
                writer,
                index=False,
                sheet_name="Inventory"
            )

        logger.info(
            f"Latest Report Updated: {latest_excel_file}"
        )

    except PermissionError:

        logger.warning(
            f"{latest_excel_file} is open."
        )
# ============================================================
# MAIN
# ============================================================

def main():

    logger.info("=" * 80)
    logger.info("STARTING INVENTORY SCAN")
    logger.info("=" * 80)

    create_database()

    config = load_config()

    root_folder = config["root_folder"]

    datasets = config["datasets"]

    results = []

    for dataset in datasets:

        try:

            result = scan_dataset(
                root_folder,
                dataset
            )

            results.append(result)

        except Exception as e:

            logger.exception(
                f"Error scanning dataset: {e}"
            )

    df = pd.DataFrame(results)

    # ==========================================
    # TRADING DAYS SUMMARY
    # ==========================================

    old_files = df.loc[
        df["to_date"] == "20170331",
        "file_count"
    ].sum()

    new_files = df.loc[
        df["to_date"] != "20170331",
        "file_count"
].sum()

    trading_days = pd.DataFrame([
    {
        "folder1": "TRADING DAYS_OLD",
        "folder2": "",
        "folder3": "",

        "file_name":
            "TD_OLD_19970401_20170331",

        "full_path": "",

        "from_date": "19970401",
        "to_date": "20170331",

        "file_count": old_files,

        "status": "AVAILABLE"
    },

    {
        "folder1": "TRADING DAYS_NEW",
        "folder2": "",
        "folder3": "",

        "file_name":
            f"TD_NEW_20170401_{datetime.now():%Y%m%d}",

        "full_path": "",

        "from_date": "20170401",

        "to_date":
            datetime.now().strftime(
                "%Y%m%d"
            ),

        "file_count": new_files,

        "status": "AVAILABLE"
    }
])
    df = pd.concat(
        [trading_days, df],
        ignore_index=True
    )

    df["last_updated"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    save_to_database(df)

    try:

        save_excel(df)

    except PermissionError:

        logger.warning(
            "Excel file is open. Database updated successfully."
        )

    except Exception as e:

        logger.exception(
            f"Excel generation failed: {e}"
        )

    logger.info("=" * 80)
    logger.info("SCAN COMPLETED")
    logger.info("=" * 80)

    print()
    print(df)
    print()

# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
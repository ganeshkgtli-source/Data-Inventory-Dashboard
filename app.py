from flask import Flask, render_template
import sqlite3
from pathlib import Path
from datetime import datetime
import subprocess

# ============================================================
# APP CONFIG
# ============================================================

app = Flask(__name__)

import sys

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parent
FORMATTED_DB = BASE_DIR / "inventory_formatted.db"
RAW_DB = BASE_DIR / "inventory_raw.db"
# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection(db_file):

    conn = sqlite3.connect(db_file)

    conn.row_factory = sqlite3.Row

    return conn

# def run_scanners():

#     try:

#         subprocess.run(
#             ["python", "scanner.py"],
#             cwd=BASE_DIR,
#             timeout=300
#         )

#         subprocess.run(
#             ["python", "scanner_raw.py"],
#             cwd=BASE_DIR,
#             timeout=300
#         )

#     except Exception as e:

#         print(e)

# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def index():
     

    try:

        print("BASE_DIR =", BASE_DIR)
        print("FORMATTED_DB =", FORMATTED_DB)
        print("DB EXISTS =", FORMATTED_DB.exists())

        conn = get_connection(
    FORMATTED_DB
)

        rows = conn.execute(
            """
            SELECT *
            FROM inventory
            ORDER BY folder1, folder2, folder3
            """
        ).fetchall()
        formatted_rows = []

        for row in rows:

            row_dict = dict(row)

            try:
                if row_dict["from_date"]:
                    row_dict["from_date"] = datetime.strptime(
                        row_dict["from_date"],
                        "%Y%m%d"
                    ).strftime("%d-%m-%Y")
            except:
                pass

            try:
                if row_dict["to_date"]:
                    row_dict["to_date"] = datetime.strptime(
                        row_dict["to_date"],
                        "%Y%m%d"
                    ).strftime("%d-%m-%Y")
            except:
                pass

            formatted_rows.append(row_dict)

        total_datasets = len(rows)

        total_files = sum(
    row["file_count"] or 0
    for row in rows
    if not str(row["folder1"]).startswith("TRADING DAYS")
)

        last_updated = "-"

        if rows:
            last_updated = rows[0]["last_updated"]

            try:
                last_updated = datetime.strptime(
                    last_updated,
                    "%Y-%m-%d %H:%M:%S"
                ).strftime("%d-%m-%Y %I:%M:%S %p")
            except:
                pass

        conn.close()
        next_run = "Every Day 09:00 AM"

        return render_template(
        "index.html",
        data=formatted_rows,
        total_datasets=total_datasets,
        total_files=total_files,
        last_updated=last_updated,
        next_run=next_run,
        report_type="FORMATTED"
    )

    except Exception as e:

        return f"""
        <h2>Database Error</h2>
        <pre>{str(e)}</pre>

        <br><br>

        Make sure:

        <ul>
            <li>scanner.py has been executed</li>
            <li>inventory.db exists</li>
            <li>inventory table exists</li>
        </ul>
        """

# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return {
        "status": "success",
        "application": "Data Inventory Dashboard"
    }

@app.route("/scan_formatted")
def scan_formatted():

    subprocess.run(
        ["python", "scanner.py"],
        cwd=BASE_DIR
    )

    return """
    <script>
        window.location='/';
    </script>
    """
@app.route("/scan_raw")
def scan_raw():

    subprocess.run(
        ["python", "scanner_raw.py"],
        cwd=BASE_DIR
    )

    return """
    <script>
        window.location='/raw';
    </script>
    """

@app.route("/raw")
def raw():

    try:
        print("BASE_DIR =", BASE_DIR)
        print("RAW_DB =", RAW_DB)
        print("DB EXISTS =", RAW_DB.exists())
        conn = get_connection(
            RAW_DB
        )

        rows = conn.execute(
            """
            SELECT *
            FROM inventory
            ORDER BY folder1, folder2, folder3
            """
        ).fetchall()

        formatted_rows = []

        for row in rows:

            row_dict = dict(row)

            try:
                if row_dict["from_date"]:
                    row_dict["from_date"] = datetime.strptime(
                        row_dict["from_date"],
                        "%Y%m%d"
                    ).strftime("%d-%m-%Y")
            except:
                pass

            try:
                if row_dict["to_date"]:
                    row_dict["to_date"] = datetime.strptime(
                        row_dict["to_date"],
                        "%Y%m%d"
                    ).strftime("%d-%m-%Y")
            except:
                pass

            formatted_rows.append(row_dict)

        total_datasets = len(rows)

        total_files = sum(
            row["file_count"] or 0
            for row in rows
        )

        last_updated = "-"

        if rows:

            last_updated = rows[0]["last_updated"]

            try:

                last_updated = datetime.strptime(
                    last_updated,
                    "%Y-%m-%d %H:%M:%S"
                ).strftime("%d-%m-%Y %I:%M:%S %p")

            except:
                pass

        conn.close()

        return render_template(
            "index.html",
            data=formatted_rows,
            total_datasets=total_datasets,
            total_files=total_files,
            last_updated=last_updated,
            next_run="Every Day 09:05 AM",
            report_type="RAW"
        )

    except Exception as e:

        return str(e)
# ============================================================
# RUN APP
# ============================================================
 
    return """
    <script>
        window.location='/';
    </script>
    """

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
from pathlib import Path
import re

# ============================================================
# FOLDER TO CHECK
# ============================================================

FOLDER = Path(
    r"G:\Ganesh\NEW RAW FILES\03_NSE_CM\STOCK RAW FILES\EOD"
)

# ============================================================
# DATE RANGE
# ============================================================

START_DATE = "19970401"
END_DATE = "20170331"

# ============================================================
# COUNT FILES
# ============================================================

count = 0

for file in FOLDER.rglob("*.csv"):

    match = re.search(r"(\d{8})", file.name)

    if not match:
        continue

    file_date = match.group(1)

    if START_DATE <= file_date <= END_DATE:
        count += 1

print()
print("=" * 60)
print("FOLDER :", FOLDER)
print("FROM   :", START_DATE)
print("TO     :", END_DATE)
print("COUNT  :", count)
print("=" * 60)
print()
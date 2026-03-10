"""
temporal_analysis.py
--------------------
Counts messages per day and per month in a WhatsApp chat export,
then reports the busiest day and month.
"""

import re
import os
import sys
from collections import defaultdict
from datetime import datetime

MSG_PATTERN = re.compile(r"^\[(\d{2}/\d{2}/\d{2}), .*?\] [^:]+: (.*)")


def analyze_file(filepath: str, output_dir: str = "output") -> None:
    """Parse a chat file and write a temporal activity report."""
    os.makedirs(output_dir, exist_ok=True)

    daily: dict[str, int] = defaultdict(int)
    monthly: dict[str, int] = defaultdict(int)

    with open(filepath, encoding="utf-8") as f:
        for line in f:
            m = MSG_PATTERN.match(line.strip())
            if not m:
                continue
            date = datetime.strptime(m.group(1), "%d/%m/%y")
            daily[date.strftime("%Y-%m-%d")] += 1
            monthly[date.strftime("%Y-%m")] += 1

    if not daily:
        print(f"No messages found in {filepath}")
        return

    busiest_day = max(daily, key=daily.__getitem__)
    busiest_month = max(monthly, key=monthly.__getitem__)

    base_name = os.path.splitext(os.path.basename(filepath))[0]
    report_path = os.path.join(output_dir, f"temporal_{base_name}.txt")

    with open(report_path, "w", encoding="utf-8") as out:
        out.write("📅 TEMPORAL ACTIVITY REPORT\n")
        out.write("=" * 35 + "\n\n")
        out.write(f"File           : {filepath}\n\n")
        out.write(f"Busiest day    : {busiest_day} ({daily[busiest_day]} messages)\n")
        out.write(f"Busiest month  : {busiest_month} ({monthly[busiest_month]} messages)\n")

    print(f"Report saved → {report_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python temporal_analysis.py <file1.txt> [file2.txt ...]")
        sys.exit(1)

    for path in sys.argv[1:]:
        analyze_file(path)

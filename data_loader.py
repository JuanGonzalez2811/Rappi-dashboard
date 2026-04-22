import csv
import glob
import os
from datetime import datetime
import re


DATA_DIR = os.path.expanduser("~/Downloads/Archivo")


def parse_timestamp(ts_str):
    # "Sun Feb 01 2026 06:11:20 GMT-0500 (hora estándar de Colombia)"
    ts_str = re.sub(r"\s*\(.*\)", "", ts_str).strip()
    # "Sun Feb 01 2026 06:11:20 GMT-0500"
    ts_str = re.sub(r"\s+GMT[+-]\d{4}$", "", ts_str).strip()
    # "Sun Feb 01 2026 06:11:20"
    return datetime.strptime(ts_str, "%a %b %d %Y %H:%M:%S")


def load_all_data():
    files = glob.glob(os.path.join(DATA_DIR, "AVAILABILITY-data*.csv"))
    records = []

    for filepath in files:
        try:
            with open(filepath, encoding="utf-8") as f:
                rows = list(csv.reader(f))
        except Exception:
            continue

        if len(rows) < 2:
            continue

        header = rows[0]
        for data_row in rows[1:]:
            metric = data_row[1] if len(data_row) > 1 else "unknown"
            for col_idx in range(4, len(header)):
                if col_idx >= len(data_row):
                    continue
                ts_str = header[col_idx]
                val_str = data_row[col_idx]
                if not ts_str or not val_str:
                    continue
                try:
                    ts = parse_timestamp(ts_str)
                    val = float(val_str)
                    records.append({"timestamp": ts, "metric": metric, "value": val})
                except (ValueError, TypeError):
                    continue

    records.sort(key=lambda x: x["timestamp"])
    return records


def records_to_summary(records):
    if not records:
        return {}

    values = [r["value"] for r in records]
    timestamps = [r["timestamp"] for r in records]

    # By hour of day
    by_hour = {}
    for r in records:
        h = r["timestamp"].hour
        by_hour.setdefault(h, []).append(r["value"])
    avg_by_hour = {h: sum(v) / len(v) for h, v in by_hour.items()}

    # By day
    by_day = {}
    for r in records:
        d = r["timestamp"].date().isoformat()
        by_day.setdefault(d, []).append(r["value"])
    avg_by_day = {d: sum(v) / len(v) for d, v in by_day.items()}

    # By weekday
    by_weekday = {}
    weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for r in records:
        wd = weekday_names[r["timestamp"].weekday()]
        by_weekday.setdefault(wd, []).append(r["value"])
    avg_by_weekday = {wd: sum(v) / len(v) for wd, v in by_weekday.items()}

    peak_hour = max(avg_by_hour, key=avg_by_hour.get)
    lowest_hour = min(avg_by_hour, key=avg_by_hour.get)

    return {
        "total_records": len(records),
        "date_range": f"{min(timestamps).strftime('%Y-%m-%d')} to {max(timestamps).strftime('%Y-%m-%d')}",
        "overall_avg": sum(values) / len(values),
        "overall_max": max(values),
        "overall_min": min(values),
        "peak_hour": peak_hour,
        "peak_hour_avg": avg_by_hour[peak_hour],
        "lowest_hour": lowest_hour,
        "lowest_hour_avg": avg_by_hour[lowest_hour],
        "avg_by_hour": avg_by_hour,
        "avg_by_day": avg_by_day,
        "avg_by_weekday": avg_by_weekday,
        "days_covered": len(by_day),
    }

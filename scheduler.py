"""
Pinterest Print-On-Demand Publishing Scheduler & Queue Manager
==============================================================
Manages scheduled queue of pins across multi-account network:
  - Generates realistic publication timestamps spaced at safe drip intervals (every 2-3 hours).
  - Matches each design to target account, board, and HTML template.
  - Keeps track of published, pending, and scheduled pins in 'publishing_schedule.json'.
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

from niche_router import detect_niche
import seo_engine

SCHEDULE_FILE = ROOT_DIR / "publishing_schedule.json"
DESIGNS_FOLDER = Path(r"C:\Users\KIZMO STORE\Downloads\New folder (27)")

def build_schedule(
    interval_hours: int = 3,
    start_time: Optional[datetime] = None
) -> Dict[str, Any]:
    """
    Builds or updates the complete publication schedule for all 69 designs.
    """
    if start_time is None:
        # Start 15 minutes from now
        start_time = datetime.now() + timedelta(minutes=15)

    # 1. Load existing schedule if present
    existing_items = {}
    if SCHEDULE_FILE.exists():
        try:
            with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data.get("queue", []):
                    existing_items[item["filename"]] = item
        except Exception:
            existing_items = {}

    # 2. Scan all local designs
    all_files = sorted([f for f in os.listdir(DESIGNS_FOLDER) if f.endswith(".png")])
    
    queue = []
    current_time = start_time

    for filename in all_files:
        # If already published or scheduled, preserve state
        if filename in existing_items and existing_items[filename].get("status") == "published":
            queue.append(existing_items[filename])
            continue

        niche_info = detect_niche(filename)
        clean_name = Path(filename).stem
        cdn_url = f"https://raw.githubusercontent.com/hamouda1/My-t-shirt-designs/main/designs/{urllib_quote(filename)}"

        pin_title = seo_engine.generate_pin_title(clean_name, niche_info["niche"])
        pin_desc = seo_engine.generate_pin_description(niche_info["niche"], niche_info["board_name"], niche_info["account"])
        alt_text = seo_engine.generate_alt_text(clean_name, niche_info["niche"], niche_info["recommended_template"])

        scheduled_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

        item = {
            "id": f"pin_{int(current_time.timestamp())}_{niche_info['niche']}",
            "filename": filename,
            "status": "pending",
            "scheduled_time": scheduled_time_str,
            "niche": niche_info["niche"],
            "account": niche_info["account"],
            "board_id": niche_info["board_id"],
            "board_name": niche_info["board_name"],
            "template": niche_info["recommended_template"],
            "palette": niche_info.get("default_palette", "terracotta"),
            "category_label": niche_info["category_label"],
            "title": pin_title,
            "description": pin_desc,
            "alt_text": alt_text,
            "cdn_url": cdn_url,
            "published_at": None,
            "pin_id": None,
            "pin_url": None
        }

        queue.append(item)
        current_time += timedelta(hours=interval_hours)

    schedule_data = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "interval_hours": interval_hours,
        "total_designs": len(queue),
        "pending_count": sum(1 for x in queue if x["status"] == "pending"),
        "published_count": sum(1 for x in queue if x["status"] == "published"),
        "queue": queue
    }

    with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump(schedule_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Schedule built with {len(queue)} items ({schedule_data['pending_count']} pending, {schedule_data['published_count']} published)")
    return schedule_data

def urllib_quote(s: str) -> str:
    import urllib.parse
    return urllib.parse.quote(s)

if __name__ == "__main__":
    schedule = build_schedule(interval_hours=3)
    print(f"Schedule written to: {SCHEDULE_FILE}")
    print("\nSample Next 3 Scheduled Pins:")
    for item in [x for x in schedule["queue"] if x["status"] == "pending"][:3]:
        print(f" - [{item['scheduled_time']}] Account: {item['account']} | Board: {item['board_name']}")
        print(f"   Design: {item['filename'][:40]}...")

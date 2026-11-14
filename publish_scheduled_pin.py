"""
Scheduled Pin Runner for Pinterest POD Automation
=================================================
Fetches the next scheduled pending pin from 'publishing_schedule.json',
executes the official Zazzle RealView rendering and HTML Pin generation,
publishes live to Pinterest, and updates queue state.
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

from zazzle_pinterest_pipeline import ZazzlePinterestPipeline
from scheduler import SCHEDULE_FILE

def publish_next(force_next: bool = False) -> Optional[Dict[str, Any]]:
    if not SCHEDULE_FILE.exists():
        print(f"❌ Schedule file not found at: {SCHEDULE_FILE}")
        return None

    with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    queue = data.get("queue", [])
    now = datetime.now()

    # Find candidate
    target_item = None
    for item in queue:
        if item.get("status") == "pending":
            if force_next:
                target_item = item
                break
            else:
                sched_dt = datetime.strptime(item["scheduled_time"], "%Y-%m-%d %H:%M:%S")
                if sched_dt <= now:
                    target_item = item
                    break

    if not target_item:
        print("ℹ️ No pending pins due for publishing at this time.")
        return None

    print("\n" + "=" * 70)
    print(f"🚀 EXECUTING SCHEDULED PIN: {target_item['filename']}")
    print(f"   Target Account : {target_item['account']}")
    print(f"   Target Board   : {target_item['board_name']} (ID: {target_item['board_id']})")
    print(f"   Scheduled Time : {target_item['scheduled_time']}")
    print("=" * 70)

    pipeline = ZazzlePinterestPipeline()
    res = pipeline.process_design(
        artwork_filename_or_path=target_item["filename"],
        cdn_url=target_item["cdn_url"],
        dry_run=False
    )

    if res.get("status") == "success":
        target_item["status"] = "published"
        target_item["published_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        target_item["pin_id"] = res.get("pin_id")
        target_item["pin_url"] = res.get("pin_url")
        target_item["zazzle_link"] = res.get("zazzle_link")

        # Update schedule file
        data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["pending_count"] = sum(1 for x in queue if x["status"] == "pending")
        data["published_count"] = sum(1 for x in queue if x["status"] == "published")

        with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print("\n✅ Successfully updated publishing_schedule.json!")
        return res
    else:
        print(f"❌ Failed publishing scheduled pin: {res}")
        return None

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run scheduled Pinterest POD publisher")
    parser.add_argument("--force", action="store_true", help="Publish the next pending pin immediately regardless of scheduled time")
    args = parser.parse_args()

    publish_next(force_next=args.force)

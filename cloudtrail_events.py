#!/usr/bin/env python3
"""Read-only recent CloudTrail event lookup for OpsPulse."""
import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
import boto3


def fetch_events(region: str, hours: int, profile: str | None = None, limit: int = 100) -> list[dict]:
    session = boto3.Session(profile_name=profile, region_name=region) if profile else boto3.Session(region_name=region)
    ct = session.client("cloudtrail")
    start = datetime.now(timezone.utc) - timedelta(hours=hours)
    paginator = ct.get_paginator("lookup_events")
    events = []
    for page in paginator.paginate(StartTime=start, PaginationConfig={"MaxItems": limit}):
        for item in page.get("Events", []):
            events.append({
                "event_time": item.get("EventTime").isoformat() if item.get("EventTime") else None,
                "event_name": item.get("EventName"),
                "username": item.get("Username"),
                "source": item.get("EventSource"),
                "resources": item.get("Resources", []),
            })
    return events[:limit]


def main() -> None:
    parser = argparse.ArgumentParser(description="Export recent CloudTrail lookup events (read-only).")
    parser.add_argument("--region", default="ap-south-1")
    parser.add_argument("--hours", type=int, default=24)
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--profile", help="Optional AWS CLI profile name")
    parser.add_argument("--output", help="Optional output JSON file")
    args = parser.parse_args()
    if args.hours <= 0 or args.limit <= 0:
        parser.error("--hours and --limit must be positive")
    report = {
        "project": "OpsPulse",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "region": args.region,
        "window_hours": args.hours,
        "events": fetch_events(args.region, args.hours, args.profile, args.limit),
    }
    rendered = json.dumps(report, indent=2, default=str)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()

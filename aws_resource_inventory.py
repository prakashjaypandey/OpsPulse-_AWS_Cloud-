#!/usr/bin/env python3
"""Read-only EC2 inventory exporter for OpsPulse."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import boto3


def collect_instances(region: str, profile: str | None = None) -> list[dict]:
    session = boto3.Session(profile_name=profile, region_name=region) if profile else boto3.Session(region_name=region)
    ec2 = session.client("ec2")
    rows = []
    paginator = ec2.get_paginator("describe_instances")
    for page in paginator.paginate():
        for reservation in page.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                tags = {t["Key"]: t.get("Value", "") for t in instance.get("Tags", [])}
                rows.append({
                    "instance_id": instance.get("InstanceId"),
                    "name": tags.get("Name", ""),
                    "state": instance.get("State", {}).get("Name"),
                    "instance_type": instance.get("InstanceType"),
                    "availability_zone": instance.get("Placement", {}).get("AvailabilityZone"),
                    "private_ip": instance.get("PrivateIpAddress"),
                    "public_ip": instance.get("PublicIpAddress"),
                    "launch_time": instance.get("LaunchTime").isoformat() if instance.get("LaunchTime") else None,
                })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a read-only EC2 inventory as JSON.")
    parser.add_argument("--region", default="ap-south-1")
    parser.add_argument("--profile", help="Optional AWS CLI profile name")
    parser.add_argument("--output", help="Optional output JSON file")
    args = parser.parse_args()
    report = {
        "project": "OpsPulse",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "region": args.region,
        "resource_type": "EC2",
        "instances": collect_instances(args.region, args.profile),
    }
    rendered = json.dumps(report, indent=2, default=str)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()

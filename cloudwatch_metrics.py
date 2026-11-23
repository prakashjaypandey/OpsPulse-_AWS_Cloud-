#!/usr/bin/env python3
"""Read-only CloudWatch CPU metric query for one EC2 instance."""
import argparse
import json
from datetime import datetime, timedelta, timezone
import boto3


def fetch_cpu(region: str, instance_id: str, hours: int, profile: str | None = None) -> dict:
    session = boto3.Session(profile_name=profile, region_name=region) if profile else boto3.Session(region_name=region)
    cw = session.client("cloudwatch")
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    response = cw.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName="CPUUtilization",
        Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
        StartTime=start,
        EndTime=end,
        Period=300,
        Statistics=["Average", "Maximum"],
        Unit="Percent",
    )
    datapoints = sorted(response.get("Datapoints", []), key=lambda d: d["Timestamp"])
    return {
        "project": "OpsPulse",
        "metric": "CPUUtilization",
        "instance_id": instance_id,
        "region": region,
        "window_hours": hours,
        "datapoints": [
            {
                "timestamp_utc": dp["Timestamp"].isoformat(),
                "average_percent": dp.get("Average"),
                "maximum_percent": dp.get("Maximum"),
            }
            for dp in datapoints
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Retrieve EC2 CPU metrics from CloudWatch (read-only).")
    parser.add_argument("--region", default="ap-south-1")
    parser.add_argument("--instance-id", required=True)
    parser.add_argument("--hours", type=int, default=6)
    parser.add_argument("--profile", help="Optional AWS CLI profile name")
    args = parser.parse_args()
    if args.hours <= 0:
        parser.error("--hours must be a positive integer")
    print(json.dumps(fetch_cpu(args.region, args.instance_id, args.hours, args.profile), indent=2, default=str))


if __name__ == "__main__":
    main()

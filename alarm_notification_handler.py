"""Minimal AWS Lambda handler for CloudWatch alarm events forwarded by SNS.

This example logs a concise alarm summary. It does not send a notification itself.
Configure SNS/Lambda subscriptions and permissions separately after reviewing.
"""
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    records = event.get("Records", [])
    handled = 0
    for record in records:
        sns = record.get("Sns", {})
        message = sns.get("Message", "")
        try:
            payload = json.loads(message) if isinstance(message, str) else message
        except json.JSONDecodeError:
            payload = {"message": message}
        summary = {
            "subject": sns.get("Subject"),
            "alarm_name": payload.get("AlarmName") if isinstance(payload, dict) else None,
            "new_state": payload.get("NewStateValue") if isinstance(payload, dict) else None,
            "reason": payload.get("NewStateReason") if isinstance(payload, dict) else None,
        }
        logger.info("OpsPulse alarm event: %s", json.dumps(summary))
        handled += 1
    return {"status": "processed", "records_handled": handled}

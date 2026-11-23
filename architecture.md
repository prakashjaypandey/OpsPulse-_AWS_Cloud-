# OpsPulse Architecture

## Scope
OpsPulse is a cloud operations monitoring starter kit. The current scripts are read-only collectors for EC2 inventory, CloudWatch CPU metrics, and CloudTrail event metadata. Dashboard, alarm, and Lambda files are examples, not deployed resources.

## Logical flow
1. EC2 emits default service metrics to CloudWatch.
2. CloudTrail records AWS API activity (assuming trails and event history are available).
3. Read-only Python scripts query AWS APIs and emit JSON reports.
4. CloudWatch dashboard widgets visualize infrastructure metrics.
5. CloudWatch alarms can notify through an SNS topic; a Lambda handler is included as a basic event example.

## Data boundaries
- No collector creates, modifies, or deletes cloud resources.
- Exported reports may contain account or infrastructure details. Review and redact before publishing.
- Memory and filesystem metrics may require CloudWatch Agent or custom metric publishing.

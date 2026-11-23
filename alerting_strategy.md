# Alerting Strategy

## Example thresholds (not universal recommendations)
| Signal | Example threshold | Evaluation | Suggested response |
|---|---:|---|---|
| EC2 CPU average | > 80% | 2 consecutive 5-minute periods | Check workload, processes, and scaling needs |
| EC2 status check failed | >= 1 | 1 period | Investigate instance/system health immediately |

## Alert design principles
- Use sustained thresholds and missing-data policies appropriate to the workload.
- Avoid paging for low-severity conditions.
- Add descriptive alarm names and runbook links.
- Test notification paths before relying on them.
- Track alarm noise and tune thresholds.

## Escalation example
Alarm → SNS notification → operator triage → inspect metrics/logs/events → mitigate → document outcome.

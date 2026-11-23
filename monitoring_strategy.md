# Monitoring Strategy

## Monitoring domains
- **Availability:** EC2 status checks and instance states.
- **Performance:** CPU utilization, network throughput; memory and filesystem only when an agent or custom metrics are configured.
- **Activity:** CloudTrail API event metadata for reviewing changes.
- **Alerting:** alarms on sustained thresholds rather than single noisy data points.

## Suggested review cadence
- Review active alarms and instance health daily during a learning/test deployment.
- Investigate repeated spikes against application logs and deployment history.
- Reassess thresholds as workload behavior becomes understood.

## Important metric caveats
EC2 basic metrics do not include guest memory or filesystem utilization by default in all setups. Install and configure CloudWatch Agent for those metrics. Metric availability, periods, and dimensions depend on the resource and service configuration.

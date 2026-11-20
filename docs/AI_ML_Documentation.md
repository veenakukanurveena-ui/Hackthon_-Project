# AI/ML Module Documentation

## 1. Overview

The AI/ML module is responsible for analyzing privacy-filtered infrastructure telemetry and identifying abnormal system behaviour.

It helps the platform detect infrastructure problems, identify possible contributing factors, correlate related incidents, and provide actionable recommendations.

### Main Responsibilities

- Anomaly detection using Isolation Forest.
- Feature engineering from telemetry data.
- Severity classification of detected issues.
- Incident correlation.
- Rule-based root cause assistance.
- Automated recommendation generation.
- Model explanation and evaluation.

### Input Data

The AI/ML module receives approved telemetry metadata, such as:

- CPU usage
- Memory usage
- Disk usage
- Network latency
- Packet loss percentage
- Failed login count
- Server ID
- Timestamp

### Output

The module produces:

- Anomaly status
- Severity level
- Explanation of contributing metrics
- Possible root causes
- Recommended actions
- Correlated incidents
-
---
name: Reporting pipeline
kind: Event ingestion for BI
badge: Primary developer
period: 2024 – 2026
stack: Python · Pydantic · Lambda · EventBridge · SQS · SNS · Firehose · S3 (Parquet) · Glue · Athena · Terraform · Serverless Framework · GitHub Actions · CircleCI
---

Captures business events from various producers and channels them into a data lake consumed by the business-intelligence team. Main operations: validation, PII redaction, transformation and storage.

### Impact

Expanded support to additional event types and modernised the reporting pipeline by replacing
home-grown logic and services with specialised tools and native components: Pydantic, FastAPI,
AWS EventBridge, Datadog and, later, Dynatrace.

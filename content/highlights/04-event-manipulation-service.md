---
name: Cross-cloud event routing
kind: AWS ⇄ Azure
badge: Primary developer
period: 2024 – 2026
stack: Python · Pydantic · Lambda (arm64) · EventBridge · CloudEvents · Typer · Serverless Framework · GitHub Actions · Datadog · Dynatrace
---

Routing pipeline that bridges business events between AWS and Azure: appointment, consent, organisation, payment and session events flow in both directions between AWS EventBridge and the business systems that run on Azure, across four regions.

### Impact

Expanded support to additional event types and modernised the routing pipeline by replacing home-grown logic with specialised tools and native components: Pydantic, W3C trace context, AWS EventBridge, Datadog and, later, Dynatrace. Moved outbound delivery off Solace to an Azure RDP endpoint.

# kb-network Overview

`kb-network` serves as the centralized database aggregator, status portal, and alert manager for the local network. It collects system health statistics from hosts running the `kb-network-agent` client.

---

## Capabilities

- **Telemetry Aggregator**: Receives heartbeat posts containing CPU, RAM, and Disk metrics.
- **Service Monitoring**: Maps active services on each host, including Docker container states, active Postgres/MySQL/SQLite database servers, and Ollama version metrics.
- **Task Logging**: Centralizes automation logs dispatched by host cron tasks or backup routines.
- **Alert Dispatcher**: Monitors usage limits. If a host's CPU or memory usage exceeds 90% or heartbeats cease, it inserts an alert row and triggers a Gotify push notification.
- **Server CLI**: Commands to initialize databases, verify status, and start the FastAPI dashboard daemon.
- **Desktop client**: Embedded web application to monitor host status graphs, service logs, and active alert lists.

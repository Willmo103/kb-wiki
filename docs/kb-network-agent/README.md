# kb-network-agent Overview

`kb-network-agent` is the telemetry collector client that runs on monitored network servers. It collects local operating system metrics, active database states, Docker daemon configurations, and dispatches periodic heartbeats to the central `kb-network` server.

---

## Architecture & Logic

- **Service Collector Loop**:
  Runs continuously in the background, checking local resource health and service containers at regular intervals (default: 60 seconds).
- **Subsystem Telemetry**:
  - *OS Metrics*: CPU cores, CPU usage percentage, total/free RAM (using `psutil`).
  - *Disk Metrics*: Space, usage percentage, path identifiers for partitions.
  - *Docker Daemon*: Connects to local Docker socket (`docker.from_env()`) to verify active daemon versions, container names, and states (running, exited).
  - *Ollama Daemon*: Checks if Ollama is running locally and queries active model lists.
  - *Databases*: Tests local connections to Postgres, MySQL, or SQLite nodes to verify database responsiveness.
- **Heartbeat Payload**:
  Compiles all gathered service health logs into a unified JSON structure and dispatches a POST request to the `kb-network` server's telemetry endpoint.

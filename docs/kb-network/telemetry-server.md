# kb-network Telemetry Server & Database

`kb-network` registers incoming system heartbeats and metrics inside the central `kb-core` SQLite database.

---

## 1. Database Schema

The database `~/.kb/kb.db` implements the following telemetry-specific tables:

### `network_hosts`
Stores the metadata and last-known status of registered hosts on the network.
- `hostname` (Text, Primary Key)
- `ip_address` (Text)
- `mac_address` (Text)
- `user` (Text)
- `os_name` (Text)
- `os_version` (Text)
- `cpu_percent` (Float)
- `cpu_cores` (Integer)
- `ram_total` (Integer)
- `ram_used` (Integer)
- `ram_free` (Integer)
- `last_heartbeat` (Text, ISO 8601 string)
- `api_token` (Text)
- `port` (Integer)
- `status` (Text)

### `network_telemetry_history`
Maintains historical utilization samples for graphing and metrics.
- `id` (Integer, Primary Key)
- `hostname` (Text)
- `cpu_percent` (Float)
- `ram_percent` (Float)
- `disk_percent` (Float)
- `timestamp` (Text)

### `network_services`
Lists active Docker, Ollama, and Database servers detected on registered hosts.
- `id` (Integer, Primary Key)
- `hostname` (Text)
- `service_type` (Text - E.g. `docker`, `ollama`, `database`)
- `name` (Text)
- `status` (Text)
- `details` (Text, JSON string detailing container parameters or versions)

### `network_tasks_log`
Logs automated cron tasks and runner execution logs.
- `id` (Integer, Primary Key)
- `hostname` (Text)
- `task_name` (Text)
- `status` (Text)
- `logs` (Text)
- `timestamp` (Text)

### `network_alerts`
Logs system alert triggers when resources cross warning limits.
- `id` (Integer, Primary Key)
- `hostname` (Text)
- `message` (Text)
- `severity` (Text)
- `timestamp` (Text)

---

## 2. API Endpoints

- **`POST /api/telemetry`**:
  Receives host status metrics. If resource thresholds (CPU > 90% or RAM > 90%) are exceeded, it inserts an alert and notifies Gotify.
- **`POST /api/tasks/log`**:
  Logs runner/script execution status and outputs.
- **`GET /`**:
  Renders dashboard view of active hosts and service health tables.

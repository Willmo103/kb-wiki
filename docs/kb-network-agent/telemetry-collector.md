# kb-network-agent Telemetry & CLI Reference

The agent command line script manages registering the agent client, configuring local credentials, and running the background loop.

---

## 1. CLI Commands

### `agent`
Starts the periodic heartbeat collection loop in the foreground.
- **Usage**:
  ```bash
  uv run kb-network-agent agent [--interval 60] [--server http://central-net.local]
  ```
- **Options**:
  - `--interval`: Metric sample check frequency in seconds (default is `60`).
  - `--server`: Central `kb-network` API server address.

### Daemon Control: `start` / `stop` / `status`
Runs the agent in the background as a windowless process under Windows, recording the process ID to `~/.kb/network_agent.pid`.
- **Usage**:
  ```bash
  uv run kb-network-agent start
  uv run kb-network-agent stop
  uv run kb-network-agent status
  ```

---

## 2. Configuration & Authentication

The agent reads configurations from `~/.kb/configs/kb-network-agent.json`.
- **JSON keys**:
  - `server_url`: Address of central `kb-network` listener.
  - `api_token`: API authorization key.
  - `hostname`: Identifier for the local host node.
  - `monitored_databases`: Array of database configurations to check.
- **Database Checking Configuration**:
  ```json
  {
    "monitored_databases": [
      {
        "type": "postgresql",
        "connection_string": "postgresql://user:pass@localhost:5432/dbname"
      },
      {
        "type": "sqlite",
        "path": "/var/lib/app.db"
      }
    ]
  }
  ```
- If a connection test fails, the database is flagged as "offline" in the services report sent to the server.

# Architecture

## Overview

NETAUTOLAB follows a layered, modular architecture:

```
CLI / API Layer
     │
Core Services (Config, Logging, Security)
     │
Connection Manager
     │
Driver Layer (Cisco, Huawei, Ruckus, Cambium)
     │
Services (Backup, Diagnostics, Templates, Inventory, Reports, AI)
```

## Module Descriptions

### `app/core/`
Central configuration (`config.py`) using Pydantic Settings, structured logging (`logging.py`), and security utilities.

### `app/discovery/`
USB detection (`usb.py`) supports Linux, Windows, and Android/Termux.
Device identification (`identification.py`) uses regex patterns to detect vendor, model, MAC, firmware.

### `app/connections/`
`manager.py` handles the connection cascade: SSH → Telnet → Error.

### `app/drivers/`
Abstract base (`base.py`) defines `BaseDeviceDriver` interface.
Each vendor implements: `connect()`, `execute_command()`, `get_device_info()`, `get_running_config()`, `get_interfaces()`.

### `app/drivers/cisco/simulator.py`
Full simulation of a Cisco IOS device. Enables development and testing without physical hardware.

### `app/backups/`
Saves configs in a structured path: `backups/Vendor/Model/Hostname/Timestamp/`.
`diff.py` provides config comparison (unified diff).

### `app/diagnostics/health.py`
Computes a 0-100 health score from CPU, memory, uptime, interface errors.

### `app/inventory/`
SQLite-backed device inventory. No passwords stored.

### `app/ai/`
Provider-agnostic AI layer. Mock mode for development. Pluggable to Ollama, LM Studio, or any OpenAI-compatible API.

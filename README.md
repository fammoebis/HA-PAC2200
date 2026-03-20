# PAC2200 Home Assistant Integration

V1.3

Custom integration for Siemens SENTRON PAC2200 energy meters via Modbus TCP.

## Features

- ✅ Auto-discovery (network scan)
- ✅ Device validation (PAC2200 detection)
- ✅ Energy Dashboard support
- ✅ Robust reconnect/backoff logic
- ✅ Multiple device support

## Installation (HACS)

1. Open HACS
2. Add custom repository:
   https://github.com/fammoebis/HA-PAC2200.git
3. Install "PAC2200"
4. Restart Home Assistant

## Setup

Go to:
Settings → Devices & Services → Add Integration → PAC2200

## Requirements

- PAC2200 reachable via Modbus TCP (port 502)
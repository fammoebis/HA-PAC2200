A custom HACS integration for the Siemens SENTRON PAC2200 using Modbus TCP.

## Features
- Modbus TCP support
- UI configuration (Config Flow)
- Multiple sensors (Voltage, Current, Power)
- Easy HACS installation

## Installation (HACS)
1. Open HACS
2. Add custom repository:
   https://github.com/YOUR_USERNAME/pac2200-hacs
3. Select category: Integration
4. Install and restart Home Assistant

## Configuration
After installation:
- Go to Settings → Devices & Services
- Add "PAC2200"
- Enter:
  - Host (IP address)
  - Port (default: 502)
  - Slave ID (default: 1)

## Supported Sensors
- Voltage L1
- Current L1
- Active Power
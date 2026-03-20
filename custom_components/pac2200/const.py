DOMAIN = "pac2200"

DEFAULT_PORT = 502
SCAN_TIMEOUT = 0.3

SENSORS = {
    "import_energy": {
        "name": "Import Energie",
        "unit": "kWh",
        "address": 0x0000,
        "type": "uint32"
    },
    "export_energy": {
        "name": "Export Energie",
        "unit": "kWh",
        "address": 0x0002,
        "type": "uint32"
    },
    "active_power": {
        "name": "Wirkleistung",
        "unit": "W",
        "address": 0x0004,
        "type": "int32"
    }
}
DOMAIN = "pac2200"

DEFAULT_PORT = 502

SENSORS = {
    "import_energy": {
        "name": "Import Energie",
        "address": 801,
        "unit": "kWh",
        "type": "float64",
        "scale": 0.001,
        "device_class": "energy",
        "state_class": "total_increasing"
    },
    "export_energy": {
        "name": "Export Energie",
        "address": 809,
        "unit": "kWh",
        "type": "float64",
        "scale": 0.001,
        "device_class": "energy",
        "state_class": "total_increasing"
    },
    "active_power": {
        "name": "Wirkleistung",
        "address": 65,
        "unit": "W",
        "type": "float32",
        "scale": 1,
        "device_class": "power",
        "state_class": "measurement"
    }
}
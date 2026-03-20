DOMAIN = "pac2200"

DEFAULT_PORT = 502

SENSORS = {
    "import_energy": {
        "name": "Import Energie",
        "address": 342,
        "unit": "kWh",
        "signed": False,
        "scale": 1000,
        "device_class": "energy",
        "state_class": "total_increasing"
    },
    "export_energy": {
        "name": "Export Energie",
        "address": 344,
        "unit": "kWh",
        "signed": False,
        "scale": 1000,
        "device_class": "energy",
        "state_class": "total_increasing"
    },
    "active_power": {
        "name": "Wirkleistung",
        "address": 52,
        "unit": "W",
        "signed": True,
        "scale": 1,
        "device_class": "power",
        "state_class": "measurement"
    }
}
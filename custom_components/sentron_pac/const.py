DOMAIN = "sentron_pac"

DEFAULT_PORT = 502
DEFAULT_SLAVE = 1
SCAN_INTERVAL = 10

REGISTERS = {
    "energy_in": {"address": 801, "type": "float64", "scale": 0.001},
    "energy_out": {"address": 809, "type": "float64", "scale": 0.001},
    "power": {"address": 65, "type": "float32", "scale": 1.0},
}
import logging
from homeassistant.components.sensor import (
    SensorEntity, 
    SensorDeviceClass, 
    SensorStateClass
)
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
from datetime import timedelta
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    client = hass.data[DOMAIN][entry.entry_id]
    slave = entry.data.get("slave", 1)

    # Liste der Sensoren basierend auf deiner YAML-Vorlage
    sensor_definitions = [
        {"name": "Bezogene Gesamtwirkenergie Grid", "addr": 801, "type": "float64", "unit": "kWh", "class": SensorDeviceClass.ENERGY, "state": SensorStateClass.TOTAL_INCREASING, "scale": 0.001},
        {"name": "Abgegebene Gesamtwirkenergie Grid", "addr": 809, "type": "float64", "unit": "kWh", "class": SensorDeviceClass.ENERGY, "state": SensorStateClass.TOTAL_INCREASING, "scale": 0.001},
        {"name": "Wirkleistung Grid", "addr": 65, "type": "float32", "unit": "W", "class": SensorDeviceClass.POWER, "state": SensorStateClass.MEASUREMENT, "scale": 1.0},
    ]

    sensors = []
    for sd in sensor_definitions:
        sensors.append(PacSensor(client, slave, sd, entry.entry_id))
    
    async_add_entities(sensors, True)

class PacSensor(SensorEntity):
    def __init__(self, client, slave, config, entry_id):
        self._client = client
        self._slave = slave
        self._config = config
        self._attr_name = config["name"]
        self._attr_unique_id = f"sentron_{entry_id}_{config['addr']}"
        self._attr_native_unit_of_measurement = config["unit"]
        self._attr_device_class = config["class"]
        self._attr_state_class = config["state"]

    def update(self):
        """Liest die Register vom PAC2200."""
        try:
            # float32 = 2 Register, float64 = 4 Register
            count = 4 if self._config["type"] == "float64" else 2
            result = self._client.read_input_registers(self._config["addr"], count, slave=self._slave)

            if result.isError():
                _LOGGER.warning(f"Fehler beim Lesen von Register {self._config['addr']}")
                return

            decoder = BinaryPayloadDecoder.fromRegisters(
                result.registers, 
                byteorder=Endian.BIG, 
                wordorder=Endian.BIG
            )

            if self._config["type"] == "float64":
                val = decoder.decode_64bit_float()
            else:
                val = decoder.decode_32bit_float()

            self._attr_native_value = round(val * self._config["scale"], 2)
        except Exception as e:
            _LOGGER.error(f"Fehler beim Update von {self._attr_name}: {e}")
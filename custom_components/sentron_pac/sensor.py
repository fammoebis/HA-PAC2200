from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, REGISTERS

SENSORS = {
    "energy_in": {
        "name": "Bezogene Energie",
        "unit": "kWh",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
    },
    "energy_out": {
        "name": "Abgegebene Energie",
        "unit": "kWh",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
    },
    "power": {
        "name": "Leistung",
        "unit": "W",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
    },
}


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    entities = [
        PacSensor(coordinator, entry.entry_id, key)
        for key in SENSORS
    ]

    async_add_entities(entities)


class PacSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry_id, key):
        super().__init__(coordinator)

        self._key = key
        config = SENSORS[key]

        self._attr_name = config["name"]
        self._attr_unique_id = f"{entry_id}_{key}"
        self._attr_native_unit_of_measurement = config["unit"]
        self._attr_device_class = config["device_class"]
        self._attr_state_class = config["state_class"]

    @property
    def native_value(self):
        value = self.coordinator.data.get(self._key)

        if value is None:
            return None

        scale = REGISTERS[self._key]["scale"]
        return round(value * scale, 2)
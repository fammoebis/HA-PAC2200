from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN, SENSORS

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        Pac2200Sensor(coordinator, name, unit)
        for name, _, unit in SENSORS
    ]

    async_add_entities(entities)


class Pac2200Sensor(SensorEntity):
    def __init__(self, coordinator, name, unit):
        self.coordinator = coordinator
        self._name = name
        self._unit = unit

    @property
    def name(self):
        return self._name

    @property
    def native_unit_of_measurement(self):
        return self._unit

    @property
    def state(self):
        return self.coordinator.data.get(self._name)

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.host)},
            name="Siemens PAC2200",
            manufacturer="Siemens",
            model="PAC2200",
        )

    async def async_update(self):
        await self.coordinator.async_request_refresh()
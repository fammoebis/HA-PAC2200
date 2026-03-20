from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfEnergy, UnitOfPower
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        Pac2200Sensor(coordinator, "energy_import"),
        Pac2200Sensor(coordinator, "energy_export"),
        Pac2200Sensor(coordinator, "power"),
    ])


class Pac2200Sensor(SensorEntity):
    def __init__(self, coordinator, sensor_type):
        self.coordinator = coordinator
        self.sensor_type = sensor_type

    @property
    def name(self):
        return {
            "energy_import": "Grid Energy Import",
            "energy_export": "Grid Energy Export",
            "power": "Grid Power",
        }[self.sensor_type]

    @property
    def native_value(self):
        return self.coordinator.data.get(self.sensor_type)

    @property
    def native_unit_of_measurement(self):
        return UnitOfEnergy.KILO_WATT_HOUR if "energy" in self.sensor_type else UnitOfPower.WATT

    @property
    def device_class(self):
        return "energy" if "energy" in self.sensor_type else "power"

    @property
    def state_class(self):
        return "total_increasing" if "energy" in self.sensor_type else "measurement"

    @property
    def unique_id(self):
        return f"pac2200_{self.sensor_type}"

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, "pac2200")},
            name="PAC2200 Grid Meter",
            manufacturer="Siemens",
            model="PAC2200",
        )
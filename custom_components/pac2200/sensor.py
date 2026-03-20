from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN, SENSORS

async def async_setup_entry(hass, entry, async_add_entities):
    client = hass.data[DOMAIN][entry.entry_id]

    async def async_update_data():
        data = {}
        for key, cfg in SENSORS.items():
            val = await hass.async_add_executor_job(client.read_value, cfg["address"], cfg["type"])
            data[key] = (val * cfg["scale"]) if val is not None else None
        return data

    coordinator = DataUpdateCoordinator(
        hass, logger=None, name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(seconds=10),
    )
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([PAC2200Sensor(coordinator, entry, k, v) for k, v in SENSORS.items()])

class PAC2200Sensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry, key, cfg):
        super().__init__(coordinator)
        self._key = key
        self._attr_name = cfg["name"]
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_native_unit_of_measurement = cfg["unit"]
        self._attr_device_class = cfg.get("device_class")
        self._attr_state_class = cfg.get("state_class")
        self._attr_has_entity_name = True
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="PAC2200",
            manufacturer="Siemens"
        )

    @property
    def native_value(self):
        return self.coordinator.data.get(self._key)
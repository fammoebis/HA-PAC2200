import logging
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, SENSORS

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    client = hass.data[DOMAIN][entry.entry_id]

    async def async_update_data():
        data = {}
        for key, cfg in SENSORS.items():
            val = await hass.async_add_executor_job(
                client.read_value,
                cfg["address"],
                cfg["type"]
            )

            if val is not None:
                val = val * cfg["scale"]

            data[key] = val

        return data

    coordinator = DataUpdateCoordinator(
        hass,
        logger=_LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(seconds=10),
    )

    await coordinator.async_config_entry_first_refresh()

    async_add_entities([
        PAC2200Sensor(coordinator, entry, key, cfg)
        for key, cfg in SENSORS.items()
    ])


class PAC2200Sensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry, key, cfg):
        super().__init__(coordinator)

        self._key = key
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_name = cfg["name"]

        self._attr_native_unit_of_measurement = cfg["unit"]
        self._attr_device_class = cfg.get("device_class")
        self._attr_state_class = cfg.get("state_class")

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Siemens PAC2200",
            manufacturer="Siemens",
            model="PAC2200"
        )

    @property
    def native_value(self):
        return self.coordinator.data.get(self._key)
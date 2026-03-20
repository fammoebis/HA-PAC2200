from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from datetime import timedelta
import logging

from .const import DOMAIN, SENSORS
from .modbus_controller import PAC2200Client

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data["host"]
    port = entry.data["port"]

    client = PAC2200Client(host, port)

    async def async_update_data():
        data = {}

        for key, cfg in SENSORS.items():
            try:
                value = await hass.async_add_executor_job(
                    client.read_value,
                    cfg["address"],
                    cfg["type"],
                    1
                )

                if value is not None:
                    value = value * cfg["scale"]

                data[key] = value

            except Exception as e:
                _LOGGER.error(f"Fehler bei {key}: {e}")
                data[key] = None

        return data

    coordinator = DataUpdateCoordinator(
        hass,
        logger=_LOGGER,
        name="pac2200",
        update_method=async_update_data,
        update_interval=timedelta(seconds=10),
    )

    await coordinator.async_config_entry_first_refresh()

    entities = [
        PAC2200Sensor(coordinator, entry, key, cfg)
        for key, cfg in SENSORS.items()
    ]

    async_add_entities(entities)

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = client

async def async_unload_entry(hass, entry):
    client = hass.data[DOMAIN].pop(entry.entry_id)
    client.close()
    return True

class PAC2200Sensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry, key, cfg):
        super().__init__(coordinator)

        self.entry = entry
        self.key = key

        self._attr_name = cfg["name"]
        self._attr_unique_id = f"pac2200_{entry.entry_id}_{key}"
        self._attr_native_unit_of_measurement = cfg["unit"]

        self._attr_device_class = cfg["device_class"]
        self._attr_state_class = cfg["state_class"]

        self._attr_has_entity_name = True

        # 🎨 Icons
        if key == "import_energy":
            self._attr_icon = "mdi:transmission-tower-import"
        elif key == "export_energy":
            self._attr_icon = "mdi:transmission-tower-export"
        elif key == "active_power":
            self._attr_icon = "mdi:lightning-bolt"
        else:
            self._attr_icon = "mdi:flash"

    @property
    def native_value(self):
        return self.coordinator.data.get(self.key)

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self.entry.entry_id)},
            name="SENTRON PAC2200",
            manufacturer="Siemens",
            model="PAC2200",
            configuration_url=f"http://{self.entry.data['host']}"
        )
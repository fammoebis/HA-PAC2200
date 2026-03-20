import logging
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity

from .const import DOMAIN, SENSORS

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Setup der Sensoren basierend auf dem Config Entry."""
    client = hass.data[DOMAIN][entry.entry_id]

    async def async_update_data():
        """Zentrale Funktion zum Abrufen der Daten vom PAC2200."""
        data = {}
        for key, cfg in SENSORS.items():
            try:
                # Modbus-Abfrage in einem Executor-Thread ausführen (da synchron)
                value = await hass.async_add_executor_job(
                    client.read_value,
                    cfg["address"],
                    cfg["type"],
                    1 # Unit ID (Standard ist meist 1)
                )

                if value is not None:
                    data[key] = value * cfg["scale"]
                else:
                    _LOGGER.warning(f"Konnte Wert für {key} an Adresse {cfg['address']} nicht lesen")
                    data[key] = None

            except Exception as e:
                _LOGGER.error(f"Fehler beim Lesen von {key}: {e}")
                data[key] = None
        return data

    # Coordinator initialisieren (Poll-Intervall: 10 Sek)
    coordinator = DataUpdateCoordinator(
        hass,
        logger=_LOGGER,
        name=f"{DOMAIN}_{entry.entry_id}",
        update_method=async_update_data,
        update_interval=timedelta(seconds=10),
    )

    # Ersten Abruf erzwingen
    await coordinator.async_config_entry_first_refresh()

    entities = [
        PAC2200Sensor(coordinator, entry, key, cfg)
        for key, cfg in SENSORS.items()
    ]
    async_add_entities(entities)

class PAC2200Sensor(CoordinatorEntity, SensorEntity):
    """Repräsentation eines PAC2200 Register-Werts als Sensor."""

    def __init__(self, coordinator, entry, key, cfg):
        super().__init__(coordinator)
        self.entry = entry
        self.key = key
        
        self._attr_name = cfg["name"]
        self._attr_unique_id = f"pac2200_{entry.entry_id}_{key}"
        self._attr_native_unit_of_measurement = cfg["unit"]
        self._attr_device_class = cfg.get("device_class")
        self._attr_state_class = cfg.get("state_class")
        self._attr_has_entity_name = True

        # Icon-Zuweisung
        icons = {
            "import_energy": "mdi:transmission-tower-import",
            "export_energy": "mdi:transmission-tower-export",
            "active_power": "mdi:lightning-bolt"
        }
        self._attr_icon = icons.get(key, "mdi:flash")

    @property
    def native_value(self):
        """Gibt den aktuellen Status vom Coordinator zurück."""
        return self.coordinator.data.get(self.key)

    @property
    def device_info(self):
        """Verknüpft alle Sensoren zu einem Gerät in der UI."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.entry.entry_id)},
            name="SENTRON PAC2200",
            manufacturer="Siemens",
            model="PAC2200",
            configuration_url=f"http://{self.entry.data['host']}"
        )
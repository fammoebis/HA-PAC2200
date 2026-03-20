import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .modbus_controller import PAC2200Client
from .coordinator import PacDataCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    host = entry.data["host"]
    port = entry.data["port"]
    slave = entry.data["slave"]

    client = PAC2200Client(host, port, slave)

    connected = await hass.async_add_executor_job(client.connect)

    if not connected:
        _LOGGER.error("Keine Verbindung zu %s:%s", host, port)
        return False

    coordinator = PacDataCoordinator(hass, client)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "coordinator": coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    data = hass.data[DOMAIN].pop(entry.entry_id)

    await hass.config_entries.async_unload_platforms(entry, ["sensor"])

    await hass.async_add_executor_job(data["client"].close)

    return True
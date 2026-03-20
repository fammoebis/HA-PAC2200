import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from pymodbus.client import ModbusTcpClient
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Setzt die PAC2200 Integration über die UI auf."""
    host = entry.data["host"]
    port = entry.data["port"]
    
    client = ModbusTcpClient(host, port=port)
    
    # Verbindung beim Start kurz prüfen
    if not client.connect():
        _LOGGER.error(f"Konnte keine Verbindung zu PAC2200 unter {host}:{port} herstellen")
        return False

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = client

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Entfernt die Integration sauber."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    if unload_ok:
        client = hass.data[DOMAIN].pop(entry.entry_id)
        client.close()
    return unload_ok
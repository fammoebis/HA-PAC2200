from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .modbus_controller import PAC2200Client

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    client = PAC2200Client(
        entry.data["host"],
        entry.data["port"]
    )

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = client

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])

    if unload_ok:
        client = hass.data[DOMAIN].pop(entry.entry_id)
        client.close()

    return unload_ok
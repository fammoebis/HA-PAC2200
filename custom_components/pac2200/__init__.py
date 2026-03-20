from homeassistant.config_entries import ConfigEntry

async def async_setup_entry(hass, entry: ConfigEntry):
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
from .const import DOMAIN
from .coordinator import Pac2200Coordinator

async def async_setup_entry(hass, entry):
    coordinator = Pac2200Coordinator(
        hass,
        entry.data["host"],
        entry.data["port"],
        entry.data["slave"],
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass, entry):
    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")
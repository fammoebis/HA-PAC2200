from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .modbus_controller import PAC2200Client

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Setzt die PAC2200 Integration über die UI auf."""
    host = entry.data["host"]
    port = entry.data["port"]
    
    # Client zentral erstellen
    client = PAC2200Client(host, port)
    
    # Client in hass.data speichern, damit sensor.py darauf zugreifen kann
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = client

    # Plattformen (Sensoren) laden
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Entfernt die Integration und schließt die Verbindung."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    
    if unload_ok:
        client = hass.data[DOMAIN].pop(entry.entry_id)
        client.close() # Verbindung sauber trennen
        
    return unload_ok
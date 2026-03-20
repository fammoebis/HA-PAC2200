import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import SCAN_INTERVAL, REGISTERS

_LOGGER = logging.getLogger(__name__)


class PacDataCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, client):
        super().__init__(
            hass,
            _LOGGER,
            name="sentron_pac",
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )
        self.client = client

    async def _async_update_data(self):
        try:
            return await self.hass.async_add_executor_job(self._read_data)
        except Exception as err:
            raise UpdateFailed(f"Fehler beim Lesen: {err}") from err

    def _read_data(self):
        data = {}
        for key, reg in REGISTERS.items():
            value = self.client.read_value(reg["address"], reg["type"])
            data[key] = value
        return data
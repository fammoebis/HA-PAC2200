import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from pymodbus.client import ModbusTcpClient
import struct

from .const import SENSORS

_LOGGER = logging.getLogger(__name__)

class Pac2200Coordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, host, port, slave):
        super().__init__(
            hass,
            logger=_LOGGER,
            name="PAC2200",
            update_interval=timedelta(seconds=10),
        )
        self.host = host
        self.port = port
        self.slave = slave

    def _read_modbus(self):
        data = {}
        client = ModbusTcpClient(self.host, port=self.port)

        if not client.connect():
            _LOGGER.error("Modbus connection failed")
            return data

        for name, address, _ in SENSORS:
            rr = client.read_holding_registers(address, 2, unit=self.slave)
            if not rr.isError():
                data[name] = struct.unpack('>f', struct.pack('>HH', *rr.registers))[0]
            else:
                _LOGGER.warning(f"Read error at {address}")

        client.close()
        return data

    async def _async_update_data(self):
        return await self.hass.async_add_executor_job(self._read_modbus)
import asyncio
import logging
import struct
from datetime import timedelta

from pymodbus.client import AsyncModbusTcpClient
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DEFAULT_SLAVE, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class Pac2200Coordinator(DataUpdateCoordinator):
    def __init__(self, hass, host, port):
        super().__init__(
            hass,
            _LOGGER,
            name=f"PAC2200 ({host})",
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )
        self.host = host
        self.port = port
        self.client = AsyncModbusTcpClient(host, port=port)
        self._retries = 0

    async def _async_update_data(self):
        try:
            if not self.client.connected:
                await self.client.connect()

            data = await self._read_data()

            self._retries = 0
            return data

        except Exception as err:
            self._retries += 1
            delay = min(60, 2 ** self._retries)

            _LOGGER.warning(
                "Modbus error: %s | retry in %ss",
                err,
                delay,
            )

            await asyncio.sleep(delay)
            raise

    async def _read_data(self):
        data = {}

        rr1 = await self.client.read_input_registers(801, 4, slave=DEFAULT_SLAVE)
        rr2 = await self.client.read_input_registers(809, 4, slave=DEFAULT_SLAVE)
        rr3 = await self.client.read_input_registers(65, 2, slave=DEFAULT_SLAVE)

        data["energy_import"] = self._decode_float64(rr1.registers) * 0.001
        data["energy_export"] = self._decode_float64(rr2.registers) * 0.001
        data["power"] = self._decode_float32(rr3.registers)

        return data

    def _decode_float32(self, registers):
        return struct.unpack(">f", struct.pack(">HH", *registers))[0]

    def _decode_float64(self, registers):
        return struct.unpack(">d", struct.pack(">HHHH", *registers))[0]
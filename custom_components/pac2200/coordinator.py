from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pymodbus.client import ModbusTcpClient
import struct

class Pac2200Coordinator(DataUpdateCoordinator):
    def __init__(self, hass, host, port, slave):
        super().__init__(hass, logger=None, name="PAC2200", update_interval=timedelta(seconds=10))
        self.host = host
        self.port = port
        self.slave = slave
        self.client = ModbusTcpClient(host, port=port)

    def _decode_float(self, registers):
        return struct.unpack('>f', struct.pack('>HH', *registers))[0]

    async def _async_update_data(self):
        data = {}
        if not self.client.connect():
            return data

        for name, address, _ in __import__("custom_components.pac2200.const").const.SENSORS:
            rr = self.client.read_holding_registers(address, 2, unit=self.slave)
            if not rr.isError():
                data[name] = self._decode_float(rr.registers)

        self.client.close()
        return data
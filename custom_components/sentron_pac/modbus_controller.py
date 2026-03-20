import logging
import threading
from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

_LOGGER = logging.getLogger(__name__)


class PAC2200Client:
    def __init__(self, host, port, slave):
        self.host = host
        self.port = port
        self.slave = slave
        self.client = ModbusTcpClient(host, port=port)
        self._lock = threading.Lock()

    def connect(self):
        return self.client.connect()

    def close(self):
        self.client.close()

    def read_value(self, address, data_type):
        with self._lock:
            try:
                count = 4 if data_type == "float64" else 2

                result = self.client.read_input_registers(
                    address,
                    count,
                    slave=self.slave
                )

                if result.isError():
                    return None

                decoder = BinaryPayloadDecoder.fromRegisters(
                    result.registers,
                    byteorder=Endian.BIG,
                    wordorder=Endian.BIG
                )

                if data_type == "float64":
                    return decoder.decode_64bit_float()
                return decoder.decode_32bit_float()

            except Exception as e:
                _LOGGER.error("Modbus Fehler: %s", e)
                return None
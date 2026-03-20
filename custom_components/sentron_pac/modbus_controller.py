import logging
import threading
from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

_LOGGER = logging.getLogger(__name__)


class PAC2200Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = ModbusTcpClient(host, port=port)
        self._lock = threading.Lock()

    def connect(self):
        if not self.client.connected:
            return self.client.connect()
        return True

    def read_value(self, address, data_type):
        with self._lock:
            try:
                if not self.connect():
                    _LOGGER.error("Modbus Verbindung fehlgeschlagen")
                    return None

                # ggf. address - 1 testen!
                count = 4 if data_type == "float64" else 2

                result = self.client.read_input_registers(
                    address,
                    count,
                    slave=1
                )

                if result.isError():
                    _LOGGER.error("Modbus Fehler bei Adresse %s", address)
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
                _LOGGER.error("Fehler bei Adresse %s: %s", address, e)
                return None

    def close(self):
        self.client.close()
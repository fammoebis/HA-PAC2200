import logging
from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

_LOGGER = logging.getLogger(__name__)

class PAC2200Client:
    def __init__(self, host, port):
        self.client = ModbusTcpClient(host, port=port)

    def read_value(self, address, data_type):
        try:
            if not self.client.connected and not self.client.connect():
                return None
            
            count = 4 if data_type == "float64" else 2
            result = self.client.read_input_registers(address, count, slave=1)
            
            if result.isError():
                return None

            decoder = BinaryPayloadDecoder.fromRegisters(
                result.registers, byteorder=Endian.BIG, wordorder=Endian.BIG
            )
            return decoder.decode_64bit_float() if data_type == "float64" else decoder.decode_32bit_float()
        except Exception as e:
            _LOGGER.error("Fehler bei Adresse %s: %s", address, e)
            return None

    def close(self):
        self.client.close()
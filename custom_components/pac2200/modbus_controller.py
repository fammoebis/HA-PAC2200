from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian


class PAC2200Client:
    def __init__(self, host, port):
        self.client = ModbusTcpClient(host, port=port)
        self.client.connect()

    def read_value(self, address, data_type="float32", unit=1):
        if not self.client.connected:
            self.client.connect()
            
        # Anzahl Register bestimmen
        if data_type == "float32":
            count = 2
        elif data_type == "float64":
            count = 4
        else:
            return None

        result = self.client.read_input_registers(address, count, unit=unit)

        if result.isError():
            return None

        decoder = BinaryPayloadDecoder.fromRegisters(
            result.registers,
            byteorder=Endian.BIG,
            wordorder=Endian.BIG
        )

        if data_type == "float32":
            return decoder.decode_32bit_float()

        elif data_type == "float64":
            return decoder.decode_64bit_float()

        return None

    def close(self):
        self.client.close()
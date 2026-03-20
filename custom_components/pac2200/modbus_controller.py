from pymodbus.client import ModbusTcpClient


class PAC2200Client:
    def __init__(self, host, port):
        self.client = ModbusTcpClient(host, port=port)

    def read_register(self, address, signed=False):
        result = self.client.read_holding_registers(address, 2)

        if result.isError():
            return None

        high = result.registers[0]
        low = result.registers[1]

        value = (high << 16) | low

        # Signed handling
        if signed and value & 0x80000000:
            value -= 0x100000000

        return value

    def close(self):
        self.client.close()
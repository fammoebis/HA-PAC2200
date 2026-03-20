from pymodbus.client import ModbusTcpClient

class PAC2200Client:
    def __init__(self, host, port):
        self.client = ModbusTcpClient(host, port=port)

    def read_register(self, address, count=2):
        result = self.client.read_holding_registers(address, count)
        if result.isError():
            return None

        # 32-bit aus 2x 16-bit
        value = (result.registers[0] << 16) + result.registers[1]
        return value

    def close(self):
        self.client.close()
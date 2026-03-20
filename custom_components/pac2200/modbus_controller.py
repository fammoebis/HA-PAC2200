from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
import logging

_LOGGER = logging.getLogger(__name__)

class PAC2200Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = ModbusTcpClient(host, port=port)

    def read_value(self, address, data_type="float32", unit=1):
        """Liest Register und dekodiert sie basierend auf dem Typ."""
        if not self.client.connected:
            if not self.client.connect():
                _LOGGER.error(f"Verbindung zu {self.host} fehlgeschlagen")
                return None
            
        # Anzahl der Register (1 Register = 16 Bit)
        count = 4 if data_type == "float64" else 2

        try:
            # PAC2200 nutzt Input Register für Messwerte
            result = self.client.read_input_registers(address, count, slave=unit)
        except Exception as e:
            _LOGGER.error(f"Modbus-Kommunikationsfehler: {e}")
            return None

        if result.isError():
            _LOGGER.debug(f"Fehler beim Lesen von Adresse {address}: {result}")
            return None

        # Siemens PAC nutzt meist Big Endian für Byte und Word
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
        """Schließt die Verbindung."""
        self.client.close()
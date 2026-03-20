import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, DEFAULT_PORT, DEFAULT_SLAVE

class Pac2200ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="PAC2200", data=user_input)

        schema = vol.Schema({
            vol.Required("host"): str,
            vol.Optional("port", default=DEFAULT_PORT): int,
            vol.Optional("slave", default=DEFAULT_SLAVE): int,
        })

        return self.async_show_form(step_id="user", data_schema=schema)


# ==============================
# sensor.py
# ==============================
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN, SENSORS
from pymodbus.client import ModbusTcpClient
import struct

async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data["host"]
    port = entry.data["port"]
    slave = entry.data["slave"]

    sensors = [
        Pac2200Sensor(name, host, port, slave, address, unit)
        for name, address, unit in SENSORS
    ]

    async_add_entities(sensors, True)


class Pac2200Sensor(SensorEntity):
    def __init__(self, name, host, port, slave, address, unit):
        self._name = name
        self._host = host
        self._port = port
        self._slave = slave
        self._address = address
        self._unit = unit
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def native_unit_of_measurement(self):
        return self._unit

    @property
    def state(self):
        return self._state

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self._host)},
            name="Siemens PAC2200",
            manufacturer="Siemens",
            model="PAC2200",
        )

    def update(self):
        client = ModbusTcpClient(self._host, port=self._port)
        rr = client.read_holding_registers(self._address, 2, unit=self._slave)

        if not rr.isError():
            self._state = self._decode_float(rr.registers)

        client.close()

    def _decode_float(self, registers):
        return struct.unpack('>f', struct.pack('>HH', *registers))[0]
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN, SENSORS
from .modbus_controller import PAC2200Client

async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data["host"]
    port = entry.data["port"]

    client = PAC2200Client(host, port)

    sensors = []
    for key, cfg in SENSORS.items():
        sensors.append(PAC2200Sensor(client, key, cfg))

    async_add_entities(sensors, True)


class PAC2200Sensor(SensorEntity):
    def __init__(self, client, key, cfg):
        self.client = client
        self._attr_name = cfg["name"]
        self._attr_native_unit_of_measurement = cfg["unit"]
        self.address = cfg["address"]
        self.key = key
        self._attr_unique_id = f"pac2200_{key}"

    def update(self):
        value = self.client.read_register(self.address)
        self._attr_native_value = value

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, "pac2200")},
            name="SENTRON PAC2200",
            manufacturer="Siemens"
        )
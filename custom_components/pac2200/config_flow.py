import voluptuous as vol
import socket
from homeassistant import config_entries
from .const import DOMAIN, DEFAULT_PORT, SCAN_TIMEOUT

def scan_network():
    found = []
    base = "192.168.1."
    for i in range(1, 255):
        ip = f"{base}{i}"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(SCAN_TIMEOUT)
        if sock.connect_ex((ip, DEFAULT_PORT)) == 0:
            found.append(ip)
        sock.close()
    return found

class Pac2200ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title=f"PAC2200 ({user_input['host']})",
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("host"): str,
                vol.Optional("port", default=502): int
            }),
            description_placeholders={
                "info": "IP eingeben oder vorher Netzwerk scannen"
            }
        )
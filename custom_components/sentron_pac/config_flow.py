import voluptuous as vol
from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv

from pymodbus.client import ModbusTcpClient

from .const import DOMAIN, DEFAULT_PORT, DEFAULT_SLAVE


class SentronConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            try:
                def test_connection():
                    client = ModbusTcpClient(
                        user_input["host"],
                        port=user_input["port"]
                    )
                    return client.connect()

                ok = await self.hass.async_add_executor_job(test_connection)

                if not ok:
                    errors["base"] = "cannot_connect"
                else:
                    return self.async_create_entry(
                        title=f"PAC2200 ({user_input['host']})",
                        data=user_input,
                    )

            except Exception:
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("host"): str,
                vol.Required("port", default=DEFAULT_PORT): cv.port,
                vol.Required("slave", default=DEFAULT_SLAVE): int,
            }),
            errors=errors,
        )
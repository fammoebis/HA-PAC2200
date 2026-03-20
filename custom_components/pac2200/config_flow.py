from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN, DEFAULT_PORT
from .modbus_controller import PAC2200Client


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            client = PAC2200Client(
                user_input["host"],
                user_input["port"]
            )

            ok = await self.hass.async_add_executor_job(client.connect)
            client.close()

            if ok:
                return self.async_create_entry(
                    title=f"PAC2200 ({user_input['host']})",
                    data=user_input
                )

            errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("host"): str,
                vol.Optional("port", default=DEFAULT_PORT): int,
            }),
            errors=errors
        )
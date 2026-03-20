import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, DEFAULT_PORT
from .modbus_controller import PAC2200Client

class Pac2200ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # Validierung: Teste die Verbindung kurz
            client = PAC2200Client(user_input["host"], user_input["port"])
            try:
                # Versuche eine Verbindung aufzubauen (im Executor, da blockierend)
                success = await self.hass.async_add_executor_job(client.client.connect)
                client.close()
                
                if success:
                    return self.async_create_entry(
                        title=f"PAC2200 ({user_input['host']})",
                        data=user_input
                    )
                else:
                    errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("host"): str,
                vol.Required("port", default=DEFAULT_PORT): int,
            }),
            errors=errors
        )
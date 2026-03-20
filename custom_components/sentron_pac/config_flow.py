import voluptuous as vol
from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv
from .const import DOMAIN, DEFAULT_PORT, DEFAULT_SLAVE

class SentronConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Konfigurations-Dialog für PAC2200."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # Erstellt den Eintrag in der UI
            return self.async_create_entry(
                title=f"PAC2200 ({user_input['host']})", 
                data=user_input
            )

        # Das Formular, das dem Nutzer angezeigt wird
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("host"): str,
                vol.Required("port", default=DEFAULT_PORT): int,
                vol.Required("slave", default=DEFAULT_SLAVE): int,
            }),
            errors=errors,
        )
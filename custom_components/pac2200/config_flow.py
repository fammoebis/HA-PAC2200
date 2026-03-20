from homeassistant import config_entries
import voluptuous as vol

class ConfigFlow(config_entries.ConfigFlow, domain="pac2200"):
    VERSION = 1
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Test PAC2200", data=user_input)
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required("host"): str})
        )
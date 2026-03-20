import logging
import voluptuous as vol
from homeassistant import config_entries
from pymodbus.client import ModbusTcpClient

from .const import DOMAIN, DEFAULT_PORT, DEFAULT_SLAVE

_LOGGER = logging.getLogger(__name__)


class SentronConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            host = user_input["host"]

            def test_connection():
                client = ModbusTcpClient(host, port=DEFAULT_PORT, timeout=3)
                try:
                    if not client.connect():
                        return False
                    return True
                finally:
                    client.close()

            try:
                ok = await self.hass.async_add_executor_job(test_connection)

                if not ok:
                    errors["base"] = "cannot_connect"
                else:
                    return self.async_create_entry(
                        title=f"PAC2200 ({host})",
                        data={
                            "host": host,
                            "port": DEFAULT_PORT,
                            "slave": DEFAULT_SLAVE,
                        },
                    )

            except Exception:
                _LOGGER.exception("Config Flow Fehler")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("host"): str,
            }),
            errors=errors,
        )
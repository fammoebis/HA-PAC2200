import asyncio
import ipaddress
import socket
import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN, CONF_HOST, CONF_PORT, DEFAULT_PORT


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()


def get_subnet():
    return ipaddress.ip_network(get_local_ip() + "/24", strict=False)


async def is_pac2200(ip):
    try:
        from pymodbus.client import AsyncModbusTcpClient  # lazy import

        client = AsyncModbusTcpClient(ip, port=502)
        await client.connect()

        rr = await client.read_input_registers(0, 10, slave=1)
        await client.close()

        if not rr or not rr.registers:
            return False

        text = "".join(chr((r >> 8)) + chr(r & 0xFF) for r in rr.registers)
        return "PAC" in text.upper()

    except Exception:
        return False


class Pac2200ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title=f"PAC2200 ({user_input[CONF_HOST]})",
                data=user_input,
            )

        # SAFE scan
        try:
            hosts = await self.scan()
        except Exception:
            hosts = []

        if hosts:
            schema = vol.Schema({
                vol.Required(CONF_HOST): vol.In(hosts),
                vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
            })
        else:
            schema = vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
            })

        return self.async_show_form(step_id="user", data_schema=schema)

    async def scan(self):
        subnet = get_subnet()
        semaphore = asyncio.Semaphore(20)

        async def check(ip):
            async with semaphore:
                ip = str(ip)
                try:
                    reader, writer = await asyncio.open_connection(ip, 502)
                    writer.close()
                    await writer.wait_closed()

                    if await is_pac2200(ip):
                        return ip
                except Exception:
                    return None

        results = await asyncio.gather(*(check(ip) for ip in subnet.hosts()))
        return [r for r in results if r]
"""Config flow for MójDomek integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import MojDomekApiClient
from .const import CONF_API_ID, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_ID): str,
    }
)

OPTIONS_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
            vol.Coerce(int),
            vol.Clamp(min=15, max=1440),
        ),
    }
)


class MojDomekConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MójDomek."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            api_id = user_input[CONF_API_ID]

            await self.async_set_unique_id(api_id)
            self._abort_if_unique_id_configured()

            session = async_get_clientsession(self.hass)
            client = MojDomekApiClient(api_id, session)

            if await client.async_validate_api_id():
                try:
                    data = await client.async_get_data()
                    title = f"MójDomek - {data.get('firstname', '')} {data.get('lastname', '')}"
                    return self.async_create_entry(title=title, data=user_input)
                except Exception:
                    _LOGGER.exception("Unexpected exception")
                    errors["base"] = "unknown"
            else:
                errors["base"] = "invalid_auth"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Return the options flow handler."""
        return MojDomekOptionsFlow(config_entry)


class MojDomekOptionsFlow(config_entries.OptionsFlow):
    """Handle options for MójDomek."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = {**self._config_entry.options}
        options.setdefault(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SCAN_INTERVAL,
                        default=options[CONF_SCAN_INTERVAL],
                    ): OPTIONS_SCHEMA.schema[CONF_SCAN_INTERVAL],
                }
            ),
        )

"""Config flow for the Custom Integrations Statistics integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, SETUP_INTEGRATION

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(SETUP_INTEGRATION): str,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for linkytic."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        # No input
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )
        # Validate input
        await self.async_set_unique_id(DOMAIN + "_" + user_input[SETUP_INTEGRATION])
        self._abort_if_unique_id_configured()
        title = user_input[SETUP_INTEGRATION]
        return self.async_create_entry(title=title, data=user_input)

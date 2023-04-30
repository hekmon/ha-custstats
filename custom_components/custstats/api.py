# pylint: disable=broad-exception-caught
"""The independent API controller for the Custom Integrations Statistics integration."""
from __future__ import annotations

import json
import logging

import aiohttp

from .const import STATS_PAGE, USER_AGENT

_LOGGER = logging.getLogger(__name__)


class StatsAPI:
    """Home Assistant Custom Integrations statistics API Controller."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialize the API controller."""
        self.websession: aiohttp.ClientSession = session

    async def get_stats(self, integration_name: str):
        """Retrieve integration statistics from Home Assistant API."""
        _LOGGER.debug(
            "getting Home Assistant custom integration statistics for '%s'",
            integration_name,
        )
        async with self.websession.get(
            STATS_PAGE, headers={"User-Agent": USER_AGENT}
        ) as resp:
            # Handle response
            if resp.status != 200:
                _LOGGER.error(
                    "Statistics fetching failed with HTTP return code %d", resp.status
                )
                return None
            # Parse payload
            try:
                stats = await resp.json()
            except json.JSONDecodeError as exp:
                _LOGGER.error("Failed to parse statistics JSON payload: %s", exp)
                return None
            try:
                return stats[integration_name]
            except KeyError:
                _LOGGER.error(
                    "Failed to get statistics for custom integration '%s': extension name not found within payload",
                    resp.status,
                )
                return None

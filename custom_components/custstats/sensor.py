"""Sensors for Custom Integrations Statistics integration."""
from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import StatsAPI
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(hours=1)


# config flow setup
async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Modern (thru config entry) sensors setup."""
    _LOGGER.debug("%s: setting up sensor plateform", config_entry.title)
    # Retrieve the API Worker object
    try:
        api = hass.data[DOMAIN][config_entry.entry_id]
    except KeyError:
        _LOGGER.error(
            "%s: can not set up sensors: failed to get the API worker object",
            config_entry.title,
        )
        return
    # Init sensors
    sensors = [IntegrationStats(config_entry.title, config_entry.entry_id, api)]
    # Add the entities to HA
    async_add_entities(sensors, True)


class IntegrationStats(SensorEntity):
    """Integration Statistics Sensor Entity."""

    # Generic properties
    _attr_has_entity_name = True
    _attr_icon = "mdi:chart-timeline-variant"
    # Sensor properties
    _attr_state_class = SensorStateClass.TOTAL
    # _attr_suggested_display_precision = 0

    def __init__(self, inte_name: str, config_id: str, api: StatsAPI) -> None:
        """Initialize the Current Color Sensor."""
        # Generic properties
        self._attr_name = f"{inte_name} installations"
        self._attr_unique_id = f"{DOMAIN}_{config_id}_stats"
        # Sensor entity properties
        self._attr_native_value: int | None = None
        self._attr_extra_state_attributes: dict[str, str] = {}
        # Custom entity properties
        self._inte_name = inte_name
        self._api = api

    async def async_update(self):
        """Update the value of the sensor from the thread object memory cache."""
        # Get stats from cache
        stats = await self._api.get_stats(self._inte_name)
        if stats is None:
            self._attr_available = False
            self._attr_native_value = None
            self._attr_extra_state_attributes = {}
            return
        # Got them
        _LOGGER.debug(
            "stats for '%s' successfully retrieved",
            self._inte_name,
        )
        try:
            total = stats["total"]
            versions = stats["versions"]
        except KeyError:
            _LOGGER.error(
                "Stats for %s retrieved but failed to access known keys",
                self._inte_name,
            )
            self._attr_available = False
            self._attr_native_value = None
            self._attr_extra_state_attributes = {}
            return
        # Handle total
        if not isinstance(total, int):
            _LOGGER.error("Stats total for '%s' should be int", self._inte_name)
            self._attr_available = False
            self._attr_native_value = None
            self._attr_extra_state_attributes = {}
            return
        self._attr_native_value = total
        self._attr_available = True
        # Handle versions (as extended attributes)
        self._attr_extra_state_attributes = {}
        for version, nb_install in versions.items():
            if not isinstance(nb_install, int):
                _LOGGER.error(
                    "Version '%s' install stats for '%s' should be int",
                    version,
                    self._inte_name,
                )
                continue
            self._attr_extra_state_attributes[version] = str(nb_install)

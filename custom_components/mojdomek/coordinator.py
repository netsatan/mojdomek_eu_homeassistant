"""DataUpdateCoordinator for MójDomek."""
from __future__ import annotations

from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import MojDomekApiClient
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL


class MojDomekDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching MójDomek data."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: MojDomekApiClient,
        scan_interval_minutes: int = DEFAULT_SCAN_INTERVAL,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            logger=hass.data[DOMAIN]["logger"],
            name=DOMAIN,
            update_interval=timedelta(minutes=scan_interval_minutes),
        )
        self.client = client

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API."""
        try:
            return await self.client.async_get_data()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

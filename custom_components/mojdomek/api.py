"""API client for MójDomek."""
from __future__ import annotations

import asyncio
from typing import Any

import aiohttp

from .const import API_URL


class MojDomekApiClient:
    """API client for MójDomek."""

    def __init__(self, api_id: str, session: aiohttp.ClientSession) -> None:
        """Initialize the API client."""
        self._api_id = api_id
        self._session = session

    async def async_get_data(self) -> dict[str, Any]:
        """Get data from the API."""
        url = f"{API_URL}?id={self._api_id}"
        
        async with asyncio.timeout(10):
            response = await self._session.get(url)
            response.raise_for_status()
            return await response.json()

    async def async_validate_api_id(self) -> bool:
        """Validate the API ID."""
        try:
            data = await self.async_get_data()
            return data.get("active", False) and len(data.get("locations", [])) > 0
        except Exception:
            return False

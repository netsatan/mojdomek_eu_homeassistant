"""Sensor platform for MójDomek."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricPotential,
    UnitOfLength,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import MojDomekDataUpdateCoordinator


@dataclass(frozen=True)
class MojDomekSensorEntityDescription(SensorEntityDescription):
    """Describes MójDomek sensor entity."""

    value_fn: Callable[[dict[str, Any]], StateType] = None


SENSOR_TYPES: tuple[MojDomekSensorEntityDescription, ...] = (
    MojDomekSensorEntityDescription(
        key="percent",
        name="Tank Level",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("measurement", {}).get("percent"),
    ),
    MojDomekSensorEntityDescription(
        key="cm",
        name="Tank Level (cm)",
        native_unit_of_measurement=UnitOfLength.CENTIMETERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("measurement", {}).get("cm"),
    ),
    MojDomekSensorEntityDescription(
        key="temperature",
        name="Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("measurement", {}).get("temperature"),
    ),
    MojDomekSensorEntityDescription(
        key="volts",
        name="Battery Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("measurement", {}).get("volts"),
    ),
    MojDomekSensorEntityDescription(
        key="batt_level",
        name="Battery Level",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("measurement", {}).get("batt_level"),
    ),
    MojDomekSensorEntityDescription(
        key="rssi",
        name="Signal Strength",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("measurement", {}).get("rssi"),
    ),
    MojDomekSensorEntityDescription(
        key="nextfull",
        name="Predicted Full Date",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda data: data.get("measurement", {}).get("nextfull"),
    ),
    MojDomekSensorEntityDescription(
        key="lastempty",
        name="Last Emptied",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda data: data.get("measurement", {}).get("lastempty"),
    ),
    MojDomekSensorEntityDescription(
        key="datatime",
        name="Last Update",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda data: data.get("measurement", {}).get("datatime"),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up MójDomek sensors from a config entry."""
    coordinator: MojDomekDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    if coordinator.data and "locations" in coordinator.data:
        for location in coordinator.data["locations"]:
            for description in SENSOR_TYPES:
                entities.append(
                    MojDomekSensor(
                        coordinator=coordinator,
                        description=description,
                        location=location,
                    )
                )

    async_add_entities(entities)


class MojDomekSensor(CoordinatorEntity[MojDomekDataUpdateCoordinator], SensorEntity):
    """Representation of a MójDomek sensor."""

    entity_description: MojDomekSensorEntityDescription

    def __init__(
        self,
        coordinator: MojDomekDataUpdateCoordinator,
        description: MojDomekSensorEntityDescription,
        location: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._location_id = location["id"]
        self._location_name = location["name"]
        
        self._attr_unique_id = f"{self._location_id}_{description.key}"
        self._attr_name = f"{self._location_name} {description.name}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, self._location_id)},
            "name": self._location_name,
            "manufacturer": "MójDomek.eu",
            "model": location.get("mainboard", "Unknown"),
            "sw_version": location.get("software", "Unknown"),
        }

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if not self.coordinator.data or "locations" not in self.coordinator.data:
            return None

        for location in self.coordinator.data["locations"]:
            if location["id"] == self._location_id:
                return self.entity_description.value_fn(location)

        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional state attributes."""
        if not self.coordinator.data or "locations" not in self.coordinator.data:
            return None

        for location in self.coordinator.data["locations"]:
            if location["id"] == self._location_id:
                return {
                    "location_id": location["id"],
                    "max_capacity": location.get("max"),
                    "alarm_level": location.get("alarm"),
                    "direction": location.get("direction"),
                    "tank_type": location.get("tanktype"),
                    "address": location.get("address", {}).get("address"),
                    "town": location.get("address", {}).get("town"),
                }

        return None

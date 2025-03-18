from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.core import callback
from homeassistant.components.unifi.controller import UniFiController

SENSOR_TYPES = [
    SensorEntityDescription(
        key="WLAN password",
        entity_category=EntityCategory.DIAGNOSTIC,
        name="WiFi Password",
    )
]

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up UniFi WLAN password sensor."""
    controller = hass.data["unifi"][entry.entry_id]
    sensors = []

    for wlan_id, wlan in controller.api.wlans.items():
        if wlan.x_passphrase is not None:
            sensors.append(UniFiPasswordSensor(controller, wlan_id, wlan))

    async_add_entities(sensors)

class UniFiPasswordSensor(CoordinatorEntity, SensorEntity):
    """Representation of a UniFi WLAN password sensor."""

    def __init__(self, controller: UniFiController, wlan_id: str, wlan):
        """Initialize the password sensor."""
        super().__init__(controller.coordinator)
        self.controller = controller
        self.wlan_id = wlan_id
        self._attr_unique_id = f"password-{wlan_id}"
        self._attr_name = f"Password {wlan.name}"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def state(self):
        """Return the current password state."""
        return self.controller.api.wlans[self.wlan_id].x_passphrase

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the controller."""
        self.async_write_ha_state()

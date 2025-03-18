"""
Custom component to restore the WLAN password sensor in the UniFi integration.
"""

DOMAIN = "unifi_password_sensor"

async def async_setup(hass, config):
    """Set up the UniFi Password Sensor component."""
    return True

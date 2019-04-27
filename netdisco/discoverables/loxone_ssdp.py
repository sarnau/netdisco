"""Discover Loxone Miniserver devices."""
from . import SSDPDiscoverable


class Discoverable(SSDPDiscoverable):
    """Add support for discovering Loxone Miniserver."""

    def get_entries(self):
        """Get all the Loxone Miniserver uPnP entries."""
        return self.find_by_device_description({
            "manufacturer": "Loxone Electronics GmbH",
        })

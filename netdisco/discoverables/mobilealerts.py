"""Discover Mobile Alerts devices."""
from . import BaseDiscoverable


class Discoverable(BaseDiscoverable):
    """Add support for discovering a Mobile Alerts gateways."""

    def __init__(self, netdis):
        """Initialize the Mobile Alerts discovery."""
        self._netdis = netdis

    def get_entries(self):
        """Get all the Mobile Alerts details."""
        return self._netdis.mobilealerts.entries

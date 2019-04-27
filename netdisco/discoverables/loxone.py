"""Discover Loxone Miniserver."""
from . import BaseDiscoverable


class Discoverable(BaseDiscoverable):
    """Add support for discovering a Loxone Miniserver."""

    def __init__(self, netdis):
        """Initialize the Loxone Miniserver discovery."""
        self._netdis = netdis

    def get_entries(self):
        """Get all the Loxone Miniserver details."""
        return self._netdis.loxone.entries
